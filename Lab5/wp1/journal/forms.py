from django import forms

# Форма вводу даних логіну/паролю користувача
class SignForm(forms.Form): 
  login = forms.EmailField(label = "Логін*", help_text="Введіть Ваш логін (email)", 
                # через параметр віджетів attrs встановлюються атрибути того елемента html, який буде генеруватися
                widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "kk@example.com"}))
  password = forms.CharField(label = "Пароль*", min_length=4, 
                widget = forms.PasswordInput(attrs={"class": "form-control"}), help_text="Введіть пароль (довжина не менше 4-х символів)")

# Форма реєстрації/зміни даних користувача
class RegistrForm(forms.Form): 
  login = forms.EmailField(label = "Логін (Email)*", 
                help_text="Будь ласка, введіть валідний Email", 
                # через параметр віджетів attrs встановлюються атрибути того елемента html, який буде генеруватися
                widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "kk@example.com"}))
  password = forms.CharField(label = "Пароль*", min_length=4, 
                widget = forms.PasswordInput(attrs={"class": "form-control"}), 
                help_text="Будь ласка, введіть валідний пароль (довжина має бути не менше 4 символів)")  
  last_name = forms.CharField(label = "Прізвище*", 
                widget=forms.TextInput(attrs={
                  "class": "form-control",
                  "pattern": "^[A-ZА-ЯЄЇІ][A-Za-zА-Яа-яЄєЇїІі\s]+$" }),
                help_text="Будь ласка, введіть валідне прізвище: не містить номерів, перша літера велика, мінімум 2 символи")
  first_name = forms.CharField(label = "Ім'я*", 
                widget=forms.TextInput(attrs={
                  "class": "form-control", 
                  "pattern": "^[A-ZА-ЯЄЇІ][A-Za-zА-Яа-яЄєЇїІі\s]*$"}),
                help_text="Будь ласка, введіть валідне ім'я: не містить номерів, перша літера велика")  
  roles = [
    (0, 'Викладач'),
    (1, 'Студент'),
  ]
  role = forms.ChoiceField(widget=forms.RadioSelect(), 
                  choices=roles, help_text="Оберіть роль")
  
  group = forms.ChoiceField(label="Група", choices=(), 
                  widget=forms.Select(attrs={ "class": "form-control" }), 
                  help_text="Будь ласка, оберіть групу")  