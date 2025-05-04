# Create your views here.

from django.http import HttpResponse, JsonResponse, HttpResponseNotFound
import json
from django.shortcuts import render
from .data_sources import *
   
def index(request): 
  return render(request, "index.html")

def user(request): 
  return render(request, "user.html")

def teacher(request): 
  return render(request, "teacher.html")

def student(request): 
  return render(request, "student.html")

def groups(request):
  """
  перелік груп студентів
  """  
  return JsonResponse(aGroups, safe=False)

def subjects(request):
  """
  перелік навчальних предметів
  """
  return JsonResponse(aSubjects, safe=False)

def journals(request):
  """
  перелік журналів успішності
  """
  idGroup = request.GET.get("idGroup")
  journals = aJournals
  
  # якщо група задана
  if idGroup != None:
    journals = [journal for journal in aJournals if str(journal["idGroup"]) == idGroup]
  print(journals)
  # Якщо  safe=False,  то  серіалізації підлягає будь-який об'єкт (якщо True, то тільки dict)
  return JsonResponse(journals, safe=False)

def findLesson(request):
  """
  пошук заняття за заданими параметрами
  """  
  # завантажуємо request.body в об'єкт json
  data = json.loads(request.body)
  idSubject = data.get("idSubject")
  idTeacher = data.get("idTeacher")
  dateLesson = data.get("dateLesson")

  # пошук в масиві занять за заданими умовами
  lesson = next((lesson for lesson in aLessons 
                 if str(lesson["idSubject"]) == idSubject 
                 and str(lesson["idTeacher"]) == idTeacher
                 and lesson["dateLesson"] == dateLesson
                 ), None)
  
  # якщо заняття не знайдено, відправляємо статусний код і повідомлення про помилку 
  if lesson == None:   
    return HttpResponseNotFound("Заняття не знайдено")   
  return JsonResponse(lesson)

def rating(request):
  """
  рейтинг студентів (idLesson != None => на заданому занятті)
  \nякщо заняття не задане, повертаємо перелік всіх рейтингів по всіх заняттях
  """
  idLesson = request.GET.get("idLesson")
  rating = aRating
  if idLesson != None:
    rating = [ratingRow for ratingRow in aRating if str(ratingRow["idLesson"]) == idLesson]
  
  # поєднуємо масив rating та aUsers, щоб знайти прізвище та ім'я студента
  merged = [
      # Це варіант, якщо потрібно всі атрибути 2-х масивів
      #{**ratingRow, **user}
      {**ratingRow, "firstName": user["firstName"], "lastName": user["lastName"]}
      for user in aUsers
      for ratingRow in rating
      if ratingRow["idStudent"] == user["id"]
  ]

  return JsonResponse(merged, safe=False)

def ratingStudent(request, idStudent:int, idJournal:int, idSubject:int):
  """
  рейтинг студента за заданим id студента, журнала, навчального предмета
  """  
  # Фільтруємо масив рейтингу за задaним id студента
  rating = [ratingRow for ratingRow in aRating if ratingRow["idStudent"] == idStudent]
  print(rating)
  # поєднуємо масив rating, aLessons, aUsers, щоб відфільрувати дані за id журналу та предмета, 
  # а потім вивести прізвище та ім'я викладача
  merged = [
      { "id": ratingRow["id"], 
        "idLesson": ratingRow["idLesson"],
        "dateLesson": lesson["dateLesson"],
        "theme": lesson["theme"],
        "maxGrade": lesson["maxGrade"],
        "firstName": user["firstName"], 
        "lastName": user["lastName"],
        "isPresence": ratingRow["isPresence"],
        "grade": ratingRow["grade"]
      }
      for ratingRow in rating
      for lesson in aLessons
      for user in aUsers
      if ratingRow["idLesson"] == lesson["id"]
      and lesson["idSubject"] == idSubject
      and lesson["idJournal"] == idJournal
      and lesson["idTeacher"] == user["id"]
  ] 

  print(merged)    
  return JsonResponse(merged, safe=False)

def findUser(request):
  """
  користувач за заданим логіном та паролем
  """      
  login =  request.POST.get("login")
  password =  request.POST.get("password")  
  user = next((user for user in aUsers if user["login"] == login), None)

  # якщо не знайдений, відправляємо статусний код і повідомлення про помилку 
  if user == None:   
    return HttpResponseNotFound(f"Користувач {login} не знайдений") 

  if user["password"] != password:
    return HttpResponse('Неправильний пароль', status = 401) 
  
  response = JsonResponse(user)
  response.set_cookie("user_id", user["id"])
  response.set_cookie("group_id", user["idGroup"])

  return response

def getUser(request, id: int):
  user = next((user for user in aUsers if user["id"] == id), None)
  # якщо не знайдений, відправляємо статусний код і повідомлення про помилку 
  if user == None:   
    return HttpResponseNotFound("Користувач не знайдений")  
  
  response = JsonResponse(user)
  response.set_cookie("user_id", user["id"])
  response.set_cookie("group_id", user["idGroup"])

  return response  