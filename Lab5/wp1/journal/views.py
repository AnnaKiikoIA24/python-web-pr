# Create your views here.

from django.http import HttpResponse, JsonResponse, HttpResponseNotFound, HttpResponseBadRequest
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
import json
from django.forms.models import model_to_dict
from django.shortcuts import render
from .models import *
from .forms import *
   
def index(request):
  signForm = SignForm() 
  return render(request, "index.html", {"form": signForm})

def user(request): 
  registrForm = RegistrForm()
  return render(request, "user.html", {"form": registrForm})

def teacher(request): 
  return render(request, "teacher.html")

def student(request): 
  return render(request, "student.html")


def groups(request):
  """
  перелік груп студентів
  """  
  return JsonResponse(list(Group.objects.all().values()), safe=False)

def subjects(request):
  """
  перелік навчальних предметів
  """
  print(Subject.objects.all())
  return JsonResponse(list(Subject.objects.all().values()), safe=False)

def journals(request):
  """
  перелік журналів успішності
  """
  idGroup = request.GET.get("idGroup")
  journals = []
  # якщо група задана
  if idGroup != None:
    journals = Journal.objects.filter(idGroup = idGroup);
  else:
    journals = Journal.objects.all()
  print("journals=", journals.query)
  
  result = []
  for journal in journals:
    result.append({ "id": journal.id,
                   "year": journal.year,
                   "idGroup": journal.idGroup.id,
                   "name": journal.idGroup.name})
  # Якщо  safe=False,  то  серіалізації підлягає будь-який об'єкт (якщо True, то тільки dict)
  return JsonResponse(result, safe=False)


def findLesson(request):
  """
  пошук заняття за заданими параметрами
  """  
  # завантажуємо request.body в об'єкт json
  data = json.loads(request.body)
  idSubject = data.get("idSubject")
  idTeacher = data.get("idTeacher")
  dateLesson = data.get("dateLesson")

  try:
    # пошук в масиві занять за заданими умовами
    lesson = Lesson.objects.get(idSubject = idSubject, idTeacher = idTeacher, dateLesson = dateLesson)
    # model_to_dict перетворює об'єкт моделі у словник 
    return JsonResponse(model_to_dict(lesson))

  # якщо заняття не знайдено, відправляємо статусний код і повідомлення про помилку              
  except ObjectDoesNotExist: 
    return HttpResponseNotFound("Заняття не знайдено")   
  except MultipleObjectsReturned: 
    return HttpResponseBadRequest("Знайдено декілька занять")

def newLesson(request):
  """
  створення нового заняття
  """
  if request.method == "POST":   
    # завантажуємо request.body в об'єкт json
    data = json.loads(request.body)  

    newLesson = Lesson.objects.create(
      idSubject_id = data.get("idSubject"),
      idTeacher_id = data.get("idTeacher"),
      dateLesson = data.get("dateLesson"),
      idJournal_id = data.get("idJournal"),
      theme = data.get("theme"),
      maxGrade = data.get("maxGrade") if data.get("maxGrade") != "" else None)
    print("newLesson=", newLesson)
    
    return JsonResponse(model_to_dict(newLesson))
  else: 
    return HttpResponseBadRequest(f"Метод `{request.method}` не підтримується. Тільки POST!") 

def editLesson(request):
  """
  редагування даних про заняття
  """
  try: 
    if request.method == "PUT": 
      # завантажуємо request.body в об'єкт json
      data = json.loads(request.body)      
      lesson = Lesson.objects.get(id = data.get("id")) 

      lesson.idSubject_id = data.get("idSubject")
      lesson.idTeacher_id = data.get("idTeacher")
      lesson.dateLesson = data.get("dateLesson")
      lesson.idJournal_id = data.get("idJournal")
      lesson.theme = data.get("theme")
      lesson.maxGrade = data.get("maxGrade") if data.get("maxGrade") != "" else None

      lesson.save()
      return JsonResponse(model_to_dict(lesson))
    
    else: 
      return HttpResponseBadRequest(f"Метод `{request.method}` не підтримується. Тільки PUT!") 
  
  except ObjectDoesNotExist: 
    return HttpResponseNotFound("Заняття не знайдено") 

def deleteLesson(request, id:int):
  """
  видалення даних про заняття
  """
  try:      
    if request.method == "DELETE": 
      lesson = Lesson.objects.get(id = id) 
      lesson.delete()
      return JsonResponse({"deleted": True}, status = 200) 
    
    else: 
      return HttpResponseBadRequest(f"Метод `{request.method}` не підтримується. Тільки DELETE!") 
  
  except ObjectDoesNotExist: 
    return HttpResponseNotFound("Заняття не знайдено") 
  

def rating(request):
  """
  рейтинг студентів (idLesson != None => на заданому занятті)
  \nякщо заняття не задане, повертаємо перелік всіх рейтингів по всіх заняттях
  """
  idLesson = request.GET.get("idLesson")
  rating = []
  # якщо заняття задане
  if idLesson != None:
    rating= Rating.objects.filter(idLesson = idLesson)
  else:
    rating = Rating.objects.all()
     
  result = []
  for ratingRow in rating:
    result.append({ "id": ratingRow.id,
                   "idLesson": ratingRow.idLesson.id,
                   "isPresence": ratingRow.isPresence,
                   "grade": ratingRow.grade,
                   "idStudent": ratingRow.idStudent.id,
                   "firstName": ratingRow.idStudent.firstName,
                   "lastName": ratingRow.idStudent.lastName })
  print(result)
  # Якщо  safe=False,  то  серіалізації підлягає будь-який об'єкт (якщо True, то тільки dict)
  return JsonResponse(result, safe=False)

def ratingStudent(request, idStudent:int, idJournal:int, idSubject:int):
  """
  рейтинг студента за заданим id студента, журнала, навчального предмета
  """  
  # Фільтруємо масив рейтингу за задaним id студента
  rating = Rating.objects.filter(idStudent = idStudent, 
                                idLesson__idJournal__id = idJournal, 
                                idLesson__idSubject__id = idSubject)
  print(rating.query)
  
  result = []
  for ratingRow in rating:
    result.append({ "id": ratingRow.id,
                    "idLesson": ratingRow.idLesson.id,
                    "dateLesson": ratingRow.idLesson.dateLesson,
                    "theme": ratingRow.idLesson.theme,
                    "maxGrade": ratingRow.idLesson.maxGrade,
                    "firstName": ratingRow.idLesson.idTeacher.firstName, 
                    "lastName": ratingRow.idLesson.idTeacher.lastName,
                    "isPresence": ratingRow.isPresence,
                    "grade": ratingRow.grade })
  print(result)
  return JsonResponse(result, safe=False)

def newRating(request):
  """
  створення нового рейтингу за списком рядків
  """
  if request.method == "POST":   
    # завантажуємо request.body в об'єкт json
    data = json.loads(request.body)  

    # Формуємо масив об'єктів Rating для вставки
    insertedData = []
    for ratingRow in data:
      insertedData.append(Rating(
        idLesson_id = ratingRow["idLesson"],
        idStudent_id = ratingRow["idStudent"],
        isPresence = ratingRow["isPresence"],
        grade = ratingRow["grade"])
      )

    # Вставляємо масив об'єктів з використанням bulk_create
    newRating = Rating.objects.bulk_create(insertedData)

    return JsonResponse([
    {
        "id": r.id,
        "idLesson": r.idLesson_id,
        "idStudent": r.idStudent_id,
        "isPresence": r.isPresence,
        "grade": r.grade
    } for r in newRating], safe=False)
  else: 
    return HttpResponseBadRequest(f"Метод `{request.method}` не підтримується. Тільки POST!") 

def editRating(request):
  """
  редагування рейтингу за списком рядків
  """
  if request.method == "PUT":   
    # завантажуємо request.body в об'єкт json
    data = json.loads(request.body)  

    updatedRating = []
    for ratingRow in data:
      try: 
        updatedRatingRow = Rating.objects.get(id = ratingRow["id"])

        updatedRatingRow.idLesson_id = ratingRow["idLesson"]
        updatedRatingRow.idStudent_id = ratingRow["idStudent"]
        updatedRatingRow.isPresence = ratingRow["isPresence"]
        updatedRatingRow.grade = ratingRow["grade"]

        updatedRatingRow.save()
        updatedRating.append(updatedRatingRow)      
      
      except ObjectDoesNotExist: 
        return HttpResponseNotFound(f"Рядок рейтингу з {ratingRow['id']} не знайдений!") 
    
    return JsonResponse([
    {
        "id": r.id,
        "idLesson": r.idLesson_id,
        "idStudent": r.idStudent_id,
        "isPresence": r.isPresence,
        "grade": r.grade
    } for r in updatedRating], safe = False)
  else: 
    return HttpResponseBadRequest(f"Метод `{request.method}` не підтримується. Тільки PUT!") 
  
def deleteRating(request):
  """
  видалення рейтингу за списком рядків
  """
  if request.method == "DELETE":   
    # завантажуємо request.body в об'єкт json
    data = json.loads(request.body)  
    print(data)
    for ratingRow in data:
      Rating.objects.filter(id = ratingRow["id"]).delete()   
    return JsonResponse({"deleted": True}, status = 200)  
  else: 
    return HttpResponseBadRequest(f"Метод `{request.method}` не підтримується. Тільки DELETE!") 
    

def findUser(request):
  """
  користувач за заданим логіном та паролем
  """     
  if request.method == "POST":    
    login =  request.POST.get("login")
    password =  request.POST.get("password")  

    try:
      user = User.objects.get(login = login)
      if user.password != password: 
        return HttpResponse('Неправильний пароль', status = 401) 
      
      response = JsonResponse(model_to_dict(user))
      response.set_cookie("user_id", user.id)
      response.set_cookie("group_id", None if user.idGroup == None else user.idGroup.id)

      return response
    # якщо користувач не знайдений, відправляємо статусний код і повідомлення про помилку              
    except ObjectDoesNotExist: 
      return HttpResponseNotFound(f"Користувач {login} не знайдений")  
  else: 
    return HttpResponseBadRequest(f"Метод `{request.method}` не підтримується. Тільки POST!")    

def getUser(request, id: int):
  try:
    user = User.objects.get(id = id)
    response = JsonResponse(model_to_dict(user))
    response.set_cookie("user_id", user.id)
    response.set_cookie("group_id", None if user.idGroup == None else user.idGroup.id)

    return response
  # якщо не знайдений, відправляємо статусний код і повідомлення про помилку 
  except ObjectDoesNotExist:   
    return HttpResponseNotFound("Користувач не знайдений")
  
def users(request):
  """
  перелік користувачів
  """  
  idGroup = request.GET.get("idGroup")

  # якщо група задана, то тільки перелік користувачів (студентів) групи
  if idGroup != None:
    return JsonResponse(list(User.objects.filter(idGroup = idGroup).order_by('lastName').values()), safe=False)
  else:
    return JsonResponse(list(User.objects.all().order_by('lastName').values()), safe=False)
  
def newUser(request):
  """
  створення нового користувача
  """
  if request.method == "POST":   
    # Дані передаються у form => конвертація у json не потрібна
    newUser = User.objects.create(
      login = request.POST.get("login"),
      password = request.POST.get("password"),
      lastName = request.POST.get("last_name"),
      firstName = request.POST.get("first_name"),
      role = True if request.POST.get("role") == "1" else False,
      idGroup_id = request.POST.get("group")
    )

    response = JsonResponse(model_to_dict(newUser))
    response.set_cookie("user_id", newUser.id)
    response.set_cookie("group_id", None if newUser.idGroup == None else newUser.idGroup.id)
    return response
  else: 
    return HttpResponseBadRequest(f"Метод `{request.method}` не підтримується. Тільки POST!")

def editUser(request):
  """
  редагування даних про користувача
  """
  try: 
    if request.method == "POST":    
      user = User.objects.get(id = request.COOKIES["user_id"]) 

      user.login = request.POST.get("login")
      user.password = request.POST.get("password")
      user.lastName = request.POST.get("last_name")
      user.firstName = request.POST.get("first_name")
      user.role = True if request.POST.get("role") == "1" else False
      user.idGroup_id = request.POST.get("group")

      user.save()
      response = JsonResponse(model_to_dict(user))
      response.set_cookie("user_id", user.id)
      response.set_cookie("group_id", None if user.idGroup == None else user.idGroup.id)
      return response
    
    else: 
      return HttpResponseBadRequest(f"Метод `{request.method}` не підтримується. Тільки POST!") 
  
  except ObjectDoesNotExist: 
    return HttpResponseNotFound("Користувач не знайдений") 

def deleteUser(request, id:int):
  """
  видалення даних про користувача
  """
  try:      
    if request.method == "DELETE": 
      user = User.objects.get(id = id) 
      user.delete()
      return JsonResponse({"deleted": True}, status = 200) 
    
    else: 
      return HttpResponseBadRequest(f"Метод `{request.method}` не підтримується. Тільки DELETE!") 
  
  except ObjectDoesNotExist: 
    return HttpResponseNotFound("Користувач не знайдений") 