from django.db import models 
  
# створюємо модель, об'єкти якої зберігатимуться в бд 
# Навчальний предмет
class Subject(models.Model): 
  nameShort = models.CharField(max_length = 20)
  nameFull = models.CharField(max_length = 60)

# Група
class Group(models.Model): 
  name = models.CharField(max_length = 10, unique = True)

# Журнал успішності
class Journal(models.Model): 
  year = models.PositiveIntegerField()
  idGroup = models.ForeignKey(Group, on_delete = models.CASCADE)

# Користувач
class User(models.Model): 
  login = models.EmailField(max_length = 15, unique = True)
  password = models.CharField(max_length = 20)
  firstName = models.CharField(max_length = 20)
  lastName = models.CharField(max_length = 25)
  role = models.BooleanField()
  idGroup = models.ForeignKey(Group, on_delete = models.CASCADE, null = True)  

# Заняття
class Lesson(models.Model): 
  idSubject = models.ForeignKey(Subject, on_delete = models.CASCADE)
  idTeacher = models.ForeignKey(User, on_delete = models.DO_NOTHING)
  dateLesson = models.DateField(null = False)
  idJournal = models.ForeignKey(Journal, on_delete = models.CASCADE)
  theme = models.CharField(max_length = 150, null = True)
  maxGrade = models.PositiveSmallIntegerField(null = True)
    
# Рейтинг
class Rating(models.Model): 
  idLesson = models.ForeignKey(Lesson, on_delete = models.CASCADE)
  idStudent = models.ForeignKey(User, on_delete = models.CASCADE)
  isPresence = models.BooleanField(null = False, default = True)
  grade = models.PositiveSmallIntegerField(null = True)    