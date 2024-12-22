from dataclasses import dataclass
from datetime import date, timedelta
from random import shuffle
from carcass import db


class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16), unique=True, nullable=False)
    skills = db.Column(db.String, nullable=False)
    workdays = db.Column(db.String(32), nullable=False)
    workshifts = db.Column(db.String(16), nullable=False)
    meal_break = db.Column(db.String(), nullable=False)
    status = db.Column(db.String(16), nullable=False)

    def __repr__(self):
        return str(self.name)

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return 'Successfully deleted'

    def update(self, skills, workdays, period, status):
        self.skills = skills
        self.workdays = workdays
        self.workshifts = period
        self.status = status
        db.session.commit()
        return 'Success'


class Vacation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16), nullable=False)
    start = db.Column(db.Date, nullable=False)
    end = db.Column(db.Date, nullable=False)

    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), unique=True)
    employee = db.relationship('Employee', backref=db.backref('tables', lazy='dynamic'))

    def __repr__(self):
        pass


@dataclass
class Unite:
    name: str
    meal_break: str
    am_duty: str = 'vacation'
    pm_duty: str = 'vacation'


@dataclass
class EmployeeToGen:
    name: str
    skills: str
    workshifts: str


def count_duty(data, name, pm, am):
    data[name] = data.get(name, {})
    x = data[name]
    if am != pm:
        x[pm] = x.get(pm, 0) + 1
        x[am] = x.get(am, 0) + 1
    else:
        x[am] = x.get(am, 0) + 1


def on_vacation(id):
    vacation = Vacation.query.filter_by(employee_id=id).first()
    employee = Employee.query.filter_by(id=id).first()
    if vacation:
        tomorrow = date.today() + timedelta(days=1)
        if vacation.start <= tomorrow <= vacation.end:
            if employee.status == 'Active':
                employee.status = f'Vacation till {vacation.end:%d.%m}'
                db.session.commit()
            return True
        elif 'Vacation' in employee.status:
            employee.status = 'Active'
            db.session.commit()
        return False
    else:
        return False


def imp_data() -> list:
    data = Employee.query.all()
    employees = []
    tomorrow = (date.today() + timedelta(days=1)).strftime('%a')
    for employee in data:
        if not on_vacation(employee.id) and employee.status == 'Active' and tomorrow in employee.workdays:
            employees.append((EmployeeToGen(name=employee.name, skills=employee.skills.split(','),
                                            workshifts=employee.workshifts)))
    shuffle(employees)
    return employees


def exp_data(name, skills):
    employee = Employee.query.filter_by(name=name).first()
    employee.skills = skills
    db.session.add(employee)
    db.session.commit()


def find_substitute(lst_of_employee):
    pos = ['Na Prv bot', 'Correct/KM', 'KK bot']
    assigned = []
    lst_of_substitute = []
    defined_to_bot = [employee for employee in lst_of_employee if employee.am_duty in pos]
    for employee in defined_to_bot:
        if employee.meal_break == '12-13':
            for sub in lst_of_employee:
                if (sub.meal_break == '13-14' and sub.am_duty not in pos and sub.name not in assigned
                        and 'free' not in sub.am_duty):
                    lst_of_substitute.append(
                        (sub.name, employee.name, employee.am_duty))
                    assigned.append(sub.name)
                    break
        else:
            for sub in lst_of_employee:
                if sub.meal_break == '12-13' and sub.pm_duty == employee.am_duty and sub.name not in assigned:
                    lst_of_substitute.append((sub.name, employee.name, employee.am_duty))
                    break
                elif sub.meal_break == '12-13' and sub.pm_duty not in pos and sub.name not in assigned:
                    lst_of_substitute.append((sub.name, employee.name, employee.am_duty))
                    break
    return lst_of_substitute


def some_process(data: dict):
    list_of_duties = []
    for i in data:
        employee = Employee.query.filter_by(name=i).first()
        list_of_duties.append(Unite(name=i, meal_break=employee.meal_break,
                                    am_duty=data[i].get('AM', 'free to do everything'),
                                    pm_duty=data[i].get('PM', 'free to do everything')))
    return sorted(list_of_duties, key=lambda x: x.name)
