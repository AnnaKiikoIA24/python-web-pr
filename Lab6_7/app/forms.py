from flask_wtf import FlaskForm 
from wtforms import StringField, IntegerField, PasswordField, RadioField, EmailField, SelectField, DateField, HiddenField, validators
from wtforms.validators import Regexp, DataRequired, Length, Optional
from datetime import date

# Форма вводу даних логіну/паролю користувача
class LoginForm(FlaskForm): 
  login = EmailField("Логін*", [DataRequired()],
                render_kw={"class": "form-control", 
                           "placeholder": "kk@example.com"})
              
  password = PasswordField("Пароль*", [validators.Length(min=4)],
                render_kw={"class": "form-control"})

# Форма реєстрації/зміни даних користувача
class RegistrForm(FlaskForm): 
  login = EmailField("Логін (Email)*", 
                render_kw={"class": "form-control", 
                           "placeholder": "kk@example.com"},
                description="Будь ласка, введіть валідний Email")
  password = PasswordField("Пароль*",
                [Length(min=4)],
                render_kw={"class": "form-control"},
                description="Будь ласка, введіть валідний пароль (довжина має бути не менше 4 символів)") 
  last_name = StringField("Прізвище*", 
                [DataRequired(),
                 # Якщо серверна валідація
                 Regexp(r"^[A-ZА-ЯЄЇІ][A-Za-zА-Яа-яЄєЇїІі'\s]+$",
                        message="Будь ласка, введіть валідне прізвище: не містить номерів, перша літера велика, мінімум 2 символи"
                )],
                render_kw={"class": "form-control",
                           "pattern": "^[A-ZА-ЯЄЇІ][A-Za-zА-Яа-яЄєЇїІі'\s]+$"}, 
                description="Будь ласка, введіть валідне прізвище: не містить номерів, перша літера велика, мінімум 2 символи")
  first_name = StringField("Ім'я*", 
                [DataRequired(message="Ім'я не має бути пустим")],
                render_kw={"class": "form-control",
                           "pattern": "^[A-ZА-ЯЄЇІ][A-Za-zА-Яа-яЄєЇїІі'\s]*$"},
                description="Будь ласка, введіть валідне ім'я: не містить номерів, перша літера велика") 
  role = RadioField('Роль*:',
                choices=[(0, 'Диспетчер'), (1, 'Пасажир')],
                validators=[DataRequired()],
                description="Оберіть роль користувача") 

# Форма вводу параметрів для пошуку поїздів (для диспетчера)
class FindTrainsForm(FlaskForm): 
  num_train = IntegerField("Номер поїзда", 
                render_kw={"class": "form-control"},
                validators=[Optional()])
  period = SelectField("Період дії розкладу*",
                render_kw={"class": "form-control"},
                coerce=int,
                validators=[DataRequired()],
                description="Оберіть період дії розкладу")
  

# Форма вводу параметрів для пошуку маршрутів (для пасажира)
class FindRoutesForm(FlaskForm): 
  station_start = SelectField("Звідки*",
                render_kw={"class": "form-control"},
                coerce=int,
                validators=[DataRequired()],
                description="Оберіть початкову станцію")
  station_fin = SelectField("Куди*",
                render_kw={"class": "form-control"},
                coerce=int,
                validators=[DataRequired()],
                description="Оберіть кінцеву станцію")  
  date_route = DateField("Дата відправлення", 
                default=date.today, 
                render_kw={"class": "form-control"},
                validators=[DataRequired()],
                description="Введіть дату відправлення")  

# Форма вводу/коригування інформації про поїзд (для диспетчера)
class TrainInfoForm(FlaskForm): 
  id_train = HiddenField("ID поїзда")
  num_train = IntegerField("Номер поїзда*", 
                render_kw={"class": "form-control"},
                validators=[DataRequired()],
                description="Введіть номер поїзда")
  old_period = HiddenField("Існуючий період поїзда")
  period = SelectField("Період розкладу*",
                render_kw={"class": "form-control", "style": "font-weight: 600"},
                coerce=int,
                validators=[DataRequired()],
                description="Оберіть період дії розкладу")
  station_from = SelectField("Початкова станція відправлення*",
                render_kw={"class": "form-control"},
                coerce=int,
                validators=[DataRequired()],
                description="Оберіть початкову станцію відправлення")
  station_to = SelectField("Кінцева станція прибуття*",
                render_kw={"class": "form-control"},
                coerce=int,
                validators=[DataRequired()],
                description="Оберіть кінцеву станцію прибуття") 

# Форма вводу/коригування інформації про рядок розкладу руху (для диспетчера)
class TrainRouteRowInfoForm(FlaskForm): 
  id_row = HiddenField("ID рядка розкладу руху")
  id_train = HiddenField("ID поїзда")
  num_order = IntegerField("Номер з/п*", 
                render_kw={"class": "form-control"},
                validators=[DataRequired()],
                description="Введіть номер з/п рядка розкладу")  
  station = SelectField("Станція*",
                render_kw={"class": "form-control"},
                coerce=int,
                validators=[DataRequired()],
                description="Оберіть станцію")  
  hours_arr = IntegerField("Години прибуття", 
                render_kw={"class": "form-control",
                           "min": "0", "max": "23"},
                validators=[Optional()],
                description="Значення має бути від 0 до 23") 
  minutes_arr = IntegerField("Хвилини прибуття", 
                render_kw={"class": "form-control",
                           "min": "0", "max": "59"},
                validators=[Optional()],
                description="Значення має бути від 0 до 59")    
  hours_depart = IntegerField("Години відправлення", 
                render_kw={"class": "form-control",
                           "min": "0", "max": "23"},
                validators=[Optional()],
                description="Значення має бути від 0 до 23") 
  minutes_depart = IntegerField("Хвилини відправлення", 
                render_kw={"class": "form-control",
                           "min": "0", "max": "59"},
                validators=[Optional()],
                description="Значення має бути від 0 до 59")  