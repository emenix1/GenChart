from flask import render_template, redirect, url_for, flash
from carcass import db, app
from carcass.config import Employee, Vacation, some_process, count_duty, exp_data, find_substitute
from carcass.forms import AddNewEmployeeForm, VacationForm, UpdateEmployeeForm
from carcass.generator_logic import start_process

duty_chart = None
data_for_save: dict | None = None
count_def_pos = {}
subs = None


@app.route('/')
@app.route('/home')
def homepage():
    if duty_chart:
        render_template('home.html', data=data_for_save)
    else:
        return redirect(url_for('generate_chart'))


@app.route('/genchart')
def generate_chart():
    global data_for_save, duty_chart, subs
    duties, data_for_save = start_process()
    day_chart = some_process(duties)
    subs = find_substitute(day_chart)

    return render_template('home.html', data=day_chart, subs=subs)


@app.route('/save_data')
def save_data():
    if data_for_save:
        for i in data_for_save:
            name, skills = i.name, i.skills
            exp_data(name, ','.join(skills))
        return redirect(url_for('homepage'))
        flash('Готово')
    else:
        return redirect(url_for('homepage'))


@app.route('/team')
def show_team():
    team = Employee.query.all()
    return render_template('team.html', data=team)


@app.route('/addteam', methods=['GET', 'POST'])
def register_employee():
    form = AddNewEmployeeForm()
    if form.validate_on_submit():
        new_emp = Employee(name=form.name.data, skills=form.skills.data, workdays=form.workdays.data,
                           workshifts=form.workshifts.data, meal_break=form.meal_break.data, status=form.status.data)
        try:
            db.session.add(new_emp)
            db.session.commit()
            return redirect(url_for('show_team'))
        except:
            db.session.rollback()
            flash('Возможно работник уже добавлен')
            return redirect(url_for('register_employee'))
    return render_template("add_employee.html", form=form)


@app.route('/remove_empl/<int:id>')
def remove_employee(id):
    employee = Employee.query.get(id)
    if employee:
        employee.delete()
    else:
        flash('Not found')
    return redirect(url_for('show_team'))


@app.route('/edit_empl/<int:id>', methods=['GET', 'POST'])
def edit_employee(id):
    employee = Employee.query.filter_by(id=id).first()
    form = UpdateEmployeeForm()
    if employee:
        if form.validate_on_submit():
            employee.update(form.skills.data, form.workdays.data,
                            form.workshifts.data, form.status.data)
            return redirect(url_for('show_team'))
    else:
        flash('Такого unita нет')
        return redirect(url_for('show_team'))
    return render_template('edit_employee.html', form=form)


@app.route('/confirm/<int:id>', methods=['GET', 'POST'])
def confirmation_process(id):
    return render_template('confirmation.html', id=id)


@app.route('/vacation', methods=['GET', 'POST'])
def register_vacation():
    form = VacationForm()
    vac_data = Vacation.query.all()
    emp_data = Employee.query.all()
    if form.validate_on_submit():

        name = form.name.data
        start = form.start.data
        end = form.end.data
        employee = Employee.query.filter_by(name=name).first()
        if not employee:
            flash(f"{name} не найден!\nЗаполните форму ниже для добавления")
            return redirect(url_for('register_employee'))
        existing = Vacation.query.filter_by(employee_id=employee.id).first()
        if existing:
            existing.start = start
            existing.end = end
            db.session.commit()
            flash('Запись обновлена')
            return redirect(url_for('show_team'))
        else:
            vacation = Vacation(name=name, start=start,
                                end=end, employee_id=employee.id)
            db.session.add(vacation)
            db.session.commit()
            flash('Отпуск успешно добавлен')
            return redirect(url_for('show_team'))

    return render_template("vacation.html", form=form, emp_data=emp_data, vac_data=vac_data)


@app.errorhandler(404)
def page_not_found(error):
    return render_template("error404.html", title='Страница не найдено')
