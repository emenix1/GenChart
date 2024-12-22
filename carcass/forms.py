from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SubmitField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired


class AddNewEmployeeForm(FlaskForm):
    name = StringField('Имя', validators=[DataRequired()])
    skills = StringField('Навыки', validators=[DataRequired()])
    workdays = StringField('Рабочие дни', validators=[DataRequired()])
    workshifts = SelectField('Смена', choices=['AM, PM', 'AM', 'PM'])
    status = SelectField('Статус', choices=['Active', 'Inactive'])
    meal_break = StringField('Время обеда', validators=[DataRequired()])
    submit = SubmitField('Submit')


class VacationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    start = DateField('Start Date')
    end = DateField('End Date')
    submit = SubmitField('Submit')


class UpdateEmployeeForm(FlaskForm):
    skills = StringField('Навыки', validators=[DataRequired()])
    workdays = StringField('Рабочие дни', validators=[DataRequired()])
    workshifts = SelectField('Смена', choices=['AM, PM', 'AM', 'PM'])
    status = SelectField('Статус', choices=['Active', 'Inactive'])
    meal_break = StringField('Время обеда', validators=[DataRequired()])
    submit = SubmitField('Submit')
