# Create your views here.

from app import app 
from datetime import date
from flask import render_template, request, redirect, url_for, Response, jsonify, make_response
from sqlalchemy import desc
from sqlalchemy.orm import aliased
from .models import *
from .forms import *

@app.route('/') 
@app.route('/index.html') 
def index(): 
  """
  головна сторінка проєкту
  """    
  loginForm = LoginForm() 
  return render_template("index.html", form=loginForm)
# ------------------------------------------------------------------------
# Користувач

@app.route('/user') 
@app.route('/user.html') 
def user():
  """
  форма даних про користувача
  """  
  registrForm = RegistrForm()
  id = request.cookies.get('user_id')
  # якщо id користувача заданий: форма даних користувача відкривається на редагування
  if id != None and id != "": 
    user = db.session.query(User).get(id)
    # якщо користувач не знайдений, відправляємо статусний код і повідомлення про помилку
    if user == None:
      return jsonify(message=f"Користувач не знайдений", code=404), 404    
    
    registrForm.login.data = user.login
    registrForm.password.data = user.password
    registrForm.last_name.data = user.lastName
    registrForm.first_name.data = user.firstName
    registrForm.role.data = "1" if user.role else "0"
  return render_template("user.html", form=registrForm)

@app.route('/api/users/hello', methods=['post']) 
def findUser():
  """
  користувач за заданим логіном та паролем
  """ 
  form = LoginForm()     
  if form.validate_on_submit():
    login = form.login.data
    password = form.password.data
    # реалізація логіки бази даних
    user = db.session.query(User).filter(User.login == login, User.password == password).first()
    # якщо користувач не знайдений, відправляємо статусний код і повідомлення про помилку
    if user == None:
      return jsonify(message=f"Користувач {login} не знайдений", code=404), 404
    if user.password != password: 
      return jsonify(message='Неправильний пароль', code=401), 401   
    
    print("user_id=",user.id)
    response = jsonify(user.to_dict())
    response.set_cookie("user_id", str(user.id)) 
    return response
  
  return jsonify(message=f"Помилка валідації даних форми", code=600), 600

@app.route('/api/users/<int:id>')
def getUser(id: int):
  """
  користувач за заданим id
  """    
  user = db.session.query(User).get(id)
  # якщо користувач не знайдений, відправляємо статусний код і повідомлення про помилку
  if user == None:
    return jsonify(message=f"Користувач не знайдений", code=404), 404
  return user.to_dict()

@app.route('/api/users/new', methods=['post']) 
def newUser():
  """
  створення нового користувача
  """
  form = RegistrForm()     
  if form.validate_on_submit():
    user = db.session.query(User).filter(User.login == form.login.data).first()
    # якщо користувач знайдений, відправляємо статусний код і повідомлення про помилку
    if user != None:
      return jsonify(message=f"Користувач {form.login.data} вже існує в БД", code=409), 409
        
    newUser = User(
      login = form.login.data,
      password = form.password.data,
      lastName = form.last_name.data,
      firstName = form.first_name.data,
      role = True if form.role.data == "1" else False
    )
    db.session.add(newUser) 
    db.session.commit() 

    print("newUser_id=", newUser.id)
    response = jsonify(newUser.to_dict())
    response.set_cookie("user_id", str(newUser.id)) 
    return response
  
  return jsonify(message=f"Помилка валідації даних форми", code=600), 600

@app.route('/api/users/edit', methods=['post']) 
def editUser():
  """
  редагування даних про користувача
  """
  id = request.cookies.get('user_id')
  if id == None or id == "":
    return jsonify(message=f"Користувач не знайдений: не задано ідентифікатор", code=404), 404     
  
  form = RegistrForm()     
  if form.validate_on_submit():
    print("login =", form.login.data)
    user = db.session.query(User).filter(User.login == form.login.data, User.id != id).first()
    # якщо знайдений інший користувач з таким логіном, відправляємо статусний код і повідомлення про помилку
    if user != None:
      return jsonify(message=f"Інший користувач з логіном {form.login.data} вже існує в БД", code=409), 409
    
    user = db.session.query(User).get(id)
    # якщо користувач не знайдений, відправляємо статусний код і повідомлення про помилку
    if user == None:
      return jsonify(message=f"Користувач не знайдений", code=404), 404    
    
    user.login = form.login.data
    user.password = form.password.data
    user.lastName = form.last_name.data
    user.firstName = form.first_name.data
    user.role = True if form.role.data == "1" else False

    db.session.commit() 
    return user.to_dict()
  
  return jsonify(message=f"Помилка валідації даних форми", code=600), 600 

@app.route('/api/users/delete/<int:id>', methods=['delete']) 
def deleteUser(id:int):
  """
  видалення даних про користувача
  """
  user = db.session.query(User).get(id)
  # якщо користувач не знайдений, відправляємо статусний код і повідомлення про помилку
  if user == None:
    return jsonify(message=f"Користувач не знайдений", code=404), 404 

  db.session.delete(user)
  db.session.commit()   

# ------------------------------------------------------------------------
# Нормативна інформація
@app.route('/api/stations')
def getStations():
  """
  перелік станцій
  """    
  stations = db.session.query(Station).order_by(Station.nameStation).all()
  # Перетворюємо у масив tuple для подальшого відображення у випадаючому списку
  stationsData = [ (station.id, station.nameStation) for station in stations]
  return [(-1, '')] + stationsData

@app.route('/api/periods')
def getPeriods():
  """
  перелік періодів дії розкладу
  """    
  # перелік періодів курсування поїздів
  periods = db.session.query(Period).order_by(desc(Period.dateBeg)).all()
  # Перетворюємо у масив tuple для подальшого відображення у випадаючому списку
  return [
    (period.id, f"{period.dateBeg.strftime('%d.%m.%Y')}-{period.dateEnd.strftime('%d.%m.%Y')}") 
    for period in periods]

# ------------------------------------------------------------------------
# Пошук та перелік поїздів (для диспетчера)
@app.route('/api/trains/<int:idPeriod>/<int:numTrain>')
@app.route('/api/trains/<int:idPeriod>')
def getTrains(idPeriod:int, numTrain=None):
  """
  перелік поїздів за заданим idPeriod та номером поїзда (необов'язковий параметр)
  """    
  stationFrom = aliased(Station)
  stationTo = aliased(Station)

  trains = (db.session.query(Train.id, Train.numTrain, Train.stationFrom, Train.stationTo,
                            stationFrom.nameStation.label("nameStationFrom"), 
                            stationTo.nameStation.label("nameStationTo"))
            .join(Train.periodsTrain)
            .filter(Period.id == idPeriod,
                    # якщо номер поїзда відсутній, то результат порівняння за номером завжди True
                    True if numTrain == None else Train.numTrain == numTrain)            
              .order_by(Train.numTrain)
              # поєднуємо з таблицею станцій для відображення назв початкової та кінцевої станцій
              .join(stationFrom, stationFrom.id == Train.stationFrom)
              .join(stationTo, stationTo.id == Train.stationTo)
              .all())

  # Перетворюємо результат у масив словників
  trainsData = [{
        "id": train.id,
        "numTrain": train.numTrain,
        "stationFrom": train.stationFrom,
        "nameStationFrom": train.nameStationFrom,
        "stationTo": train.stationTo,
        "nameStationTo": train.nameStationTo           
  } for train in trains]
  return trainsData

@app.route('/trains', methods=['get','post']) 
@app.route('/trains.html', methods=['get','post']) 
def trains():
  """
  сторінка даних про поїзди (для диспетчера)
  """  
  findTrainsForm = FindTrainsForm()
  # формуємо перелік періодів дії розкладів
  findTrainsForm.period.choices = getPeriods()
  trainsData = []
  headerResult = ""

  if (request.method == "POST"):
    if not findTrainsForm.validate_on_submit():
      print(findTrainsForm.errors)
      return jsonify(message=f"Помилка валідації даних форми", code=600), 600
    
    idPeriod = findTrainsForm.period.data
    # Знаходимо опис періоду дії розкладу
    labelPeriod = next((label for pid, label in findTrainsForm.period.choices if pid == idPeriod), "")
    numTrain = findTrainsForm.num_train.data
    print("idPeriod =", idPeriod, "numTrain =", numTrain, "labelPeriod =", labelPeriod)
    
    # отримання інформації про поїзди
    trainsData = getTrains(idPeriod, numTrain)

    if numTrain == None:
      headerResult = (f"Перелік поїздів" +
                      f" у період курсування <strong>{labelPeriod}</strong>" +
                      f" (загалом {len(trainsData)} поїзд(ів))")
    else:
      headerResult = (f"Інформація про поїзд" +
                      f" з номером <strong>{numTrain}</strong>" +
                      f" період курсування <strong>{labelPeriod}</strong>")
    print ("header_result =", headerResult)

  return (
      render_template("trains.html", 
                      find_form=findTrainsForm, 
                      header_result=headerResult,
                      trains=trainsData))

# ------------------------------------------------------------------------
# Поїзди-маршрути (для пасажира)
@app.route('/api/routes/<dateRoute>/<int:stationStart>/<int:stationFin>')
def getRoutes(dateRoute:date, stationStart:int, stationFin:int):
  """
  перелік поїздів відправленям на задану дату dateRoute та заданим напрямком stationStart - stationFin
  """      
  # аліаси маршрутів
  routeStart = aliased(TrainRoute)
  routeFin = aliased(TrainRoute)

  # аліаси станцій сполучення поїзда
  stationFrom = aliased(Station)
  stationTo = aliased(Station)

  # Основний запит до БД
  trains = (
      db.session.query(
          Train.id,
          Train.numTrain,
          stationFrom.nameStation.label("nameStationFrom"),
          stationTo.nameStation.label("nameStationTo"),
          routeStart.numOrder.label("startOrder"),
          routeStart.hoursDepart, routeStart.minutesDepart,
          routeFin.numOrder.label("finOrder"),
          routeFin.hoursArr, routeFin.minutesArr
      )
      .join(Train.periodsTrain)
      .join(routeStart, routeStart.idTrain == Train.id)
      .join(routeFin, routeFin.idTrain == Train.id)
      .filter(
          dateRoute >= Period.dateBeg, 
          dateRoute <= Period.dateEnd,
          routeStart.station == stationStart,
          routeFin.station == stationFin,
          routeStart.numOrder < routeFin.numOrder
      )
      # для відображення сполучення поїзда
      .join(stationFrom, Train.stationFrom == stationFrom.id)
      .join(stationTo, Train.stationTo == stationTo.id)      
      .order_by(routeStart.hoursDepart, routeStart.minutesDepart)
      .all()
  )
  # Перетворюємо результат у масив словників 
  trainsData = [{
        "id": train.id,
        "numTrain": train.numTrain,
        "nameStationFrom": train.nameStationFrom,
        "nameStationTo": train.nameStationTo,        
        "startOrder": train.startOrder,
        "hoursDepart": train.hoursDepart,
        "minutesDepart": train.minutesDepart,           
        "finOrder": train.finOrder,             
        "hoursArr": train.hoursArr,
        "minutesArr": train.minutesArr                     
  } for train in trains]
  return trainsData

@app.route('/routes', methods=['get','post']) 
@app.route('/routes.html', methods=['get','post']) 
def routes():
  """
  сторінка даних для пасажира для пошуку та відображення поїздів 
  \nза заданими початковою/кінцевою станціями 
  \nна задану дату
  """  
  findRoutesForm = FindRoutesForm()
  # формуємо перелік станцій (заповнюємо випадаючі списки форми)
  stations = getStations()
  findRoutesForm.station_start.choices = stations
  findRoutesForm.station_fin.choices = stations

  trainsData = []
  headerResult = ""
  nameStationStart = ""
  nameStationFin = ""

  if (request.method == "POST"):
    dateRoute = findRoutesForm.date_route.data
    stationStart = findRoutesForm.station_start.data
    stationFin = findRoutesForm.station_fin.data    
    # Знаходимо назву станції "Звідки"
    nameStationStart = next((label for pid, label in findRoutesForm.station_start.choices if pid == stationStart), "")
    # Знаходимо назву станції "Куди"
    nameStationFin = next((label for pid, label in findRoutesForm.station_fin.choices if pid == stationFin), "")
    print("dateRoute =", dateRoute, "nameStationStart =", nameStationStart, "nameStationFin =", nameStationFin)
    
    # отримання інформації з БД про поїзди за заданим напрямком на задану дату
    trainsData = getRoutes(dateRoute, stationStart, stationFin)

    if len(trainsData) > 0:
      headerResult = (f"Перелік поїздів" +
                      f" від станції <strong>{nameStationStart}</strong>" + 
                      f" до станції <strong>{nameStationFin}</strong>" +
                      f" на дату відправлення <strong>{dateRoute.strftime('%d.%m.%Y')}</strong>")
    else:
      headerResult = (f"На жаль, поїзди" +
                      f" від станції <strong>{nameStationStart}</strong>" + 
                      f" до станції <strong>{nameStationFin}</strong>" +
                      f" на дату відправлення <strong>{dateRoute.strftime('%d.%m.%Y')}</strong> відсутні...")      
    print ("header_result =", headerResult)

  return (
      render_template("routes.html", 
                      find_form=findRoutesForm, 
                      header_result=headerResult,
                      name_station_start = nameStationStart,
                      name_station_fin = nameStationFin,
                      trains=trainsData))

# ------------------------------------------------------------------------
# Інформація про поїзд
def getTrain(idTrain:int, idPeriod:int):
  """
  інформація про поїзд за заданим idTrain, idPeriod
  """    
  train = (db.session.query(Train)
           .join(Train.periodsTrain)
           .filter(Train.id == idTrain, Period.id == idPeriod)
           .first())
  return train

@app.route('/train_info') 
@app.route('/train_info.html') 
def trainInfo():
  """
  сторінка даних для вводу/коригування інформації про поїзд
  """  
  trainInfoForm = TrainInfoForm()

  # заповнення випадаючих списків форми
  stationsData = getStations()
  trainInfoForm.station_from.choices = stationsData
  trainInfoForm.station_to.choices = stationsData
  trainInfoForm.period.choices = getPeriods()

  idTrain = request.args.get('id_train', default=None, type=int) 
  idPeriod = request.args.get('period', default=None, type=int)  
  trainInfoForm.period.data = idPeriod 
  # якщо це новий поїзд
  if (idTrain == None): 
    trainInfoForm.num_train.data = request.args.get('num_train', default=None, type=int) 
    return (
      render_template("train_info.html", 
                      train_info_form = trainInfoForm))      
  # якщо це існуючий поїзд
  else:
    trainInfoForm.id_train.data = idTrain    
    # отримуємо з БД інформацію про поїзд
    train = getTrain(idTrain, idPeriod)
    if train == None:
      return jsonify(message=f"Поїзд не знайдений", code=404), 404
    
    trainInfoForm.num_train.data = train.numTrain
    trainInfoForm.station_from.data = train.stationFrom
    trainInfoForm.station_to.data = train.stationTo
    trainInfoForm.old_period.data = idPeriod

    trainRoutes = getTrainRoute(idTrain)
    return (
      render_template("train_info.html", 
                      train_info_form = trainInfoForm,
                      train_routes=trainRoutes)) 

@app.route('/api/trains/new', methods=['post']) 
def newTrain():
  """
  створення нового поїзда
  """
  form = TrainInfoForm()     
  # заповнення випадаючих списків форми
  stationsData = getStations()
  form.station_from.choices = stationsData
  form.station_to.choices = stationsData
  form.period.choices = getPeriods()  

  if form.validate_on_submit():
    idPeriod = form.period.data
    # отримуємо з БД інформацію про поїзди за заданим періодом та номером поїзда 
    trains = getTrains(idPeriod, form.num_train.data)    
    # якщо поїзд знайдений, відправляємо статусний код і повідомлення про помилку
    if len(trains) > 0:
      return jsonify(message=f"Поїзд з номером {form.num_train.data} вже існує в заданому періоді", code=409), 409
        
    newTrain = Train(
      numTrain = form.num_train.data,
      stationFrom = form.station_from.data,
      stationTo = form.station_to.data,
    )

    # Знаходимо період за id
    period = db.session.get(Period, idPeriod)  
    if period != None:
      # Прив’язуємо період
      newTrain.periodsTrain.append(period)

    # Додаємо новий поїзд та зберігаємо
    db.session.add(newTrain) 
    db.session.commit() 

    print("newTrain_id=", newTrain.id)
    return newTrain.to_dict()
  
  return jsonify(message=f"Помилка валідації даних форми", code=600), 600

@app.route('/api/trains/edit', methods=['post']) 
def editTrain():
  """
  редагування даних про поїзд
  """
  print("called /api/trains/edit")
  form = TrainInfoForm()    
  # заповнення випадаючих списків форми
  stationsData = getStations()
  form.station_from.choices = stationsData
  form.station_to.choices = stationsData
  form.period.choices = getPeriods() 
  
  if form.validate_on_submit():
    idTrain = form.id_train.data
    idPeriod = form.period.data
    oldPeriod = form.old_period.data

    print("idTrain=", form.id_train.data, "idPeriod=", idPeriod, "oldPeriod=", oldPeriod)    
    train = (db.session.query(Train)
            .join(Train.periodsTrain)
            .filter(Train.numTrain == form.num_train.data, Train.id != idTrain, Period.id == idPeriod)
            .first())
    # якщо знайдений інший поїзд з таким же номером у тому ж періоді, відправляємо статусний код і повідомлення про помилку
    if train != None:
      return jsonify(message=f"В обраному періоді існує інший поїзд з тим же номером {form.num_train.data}", code=409), 409
    
    train = getTrain(idTrain, oldPeriod)
    print("train=", train.to_dict()) 

    if train == None:      
      # якщо поїзд за id не знайдений, відправляємо статусний код і повідомлення про помилку
      return jsonify(message=f"Поїзд з id={idTrain} в заданому періоді не знайдений у БД", code=404), 404
    
    train.numTrain = form.num_train.data
    train.stationFrom = form.station_from.data
    train.stationTo = form.station_to.data
    
    # Знаходимо період за id
    period = db.session.query(Period).get(idPeriod)  
    if period != None:
      print("period=", period.to_dict())
      # Додаємо новий період, якщо його не було у поїзда
      if period not in train.periodsTrain:
        train.periodsTrain.append(period)
    
    db.session.commit() 
    return train.to_dict()
  
  return jsonify(message=f"Помилка валідації даних форми", code=600), 600 

@app.route('/api/trains/delete/<int:idTrain>/<int:idPeriod>', methods=['delete']) 
def deleteTrain(idTrain:int, idPeriod: int):
  """
  видалення даних про поїзд
  """
  train = getTrain(idTrain, idPeriod)
  if train == None:      
    # якщо поїзд за id не знайдений, відправляємо статусний код і повідомлення про помилку
    return jsonify(message=f"Поїзд з id={idTrain} в заданому періоді не знайдений у БД", code=404), 404
  
  cntLinkPeriods = len(train.periodsTrain)
  print("cntLinkPeriods before =", cntLinkPeriods)

  # Видаляємо зв'язок "Поїзд - Період"
  deletePeriod = db.session.get(Period, idPeriod)
  if deletePeriod in train.periodsTrain:
    train.periodsTrain.remove(deletePeriod)  
  
  # Рахуємо кількість зв'язків з періодами, що залишились по даному поїзду
  cntLinkPeriods = len(train.periodsTrain)
  print("cntLinkPeriods after =", cntLinkPeriods)

  # Якщо зв'язки відсутні, видаляємо розклад по поїзду і сам поїзд
  if cntLinkPeriods == 0:
    trainRoutes = db.session.query(TrainRoute).filter(TrainRoute.idTrain == idTrain).all()
    for trainRoute in trainRoutes:
      db.session.delete(trainRoute)
    
    db.session.delete(train)
  
  db.session.commit()   
  return jsonify(message="deleted: True", code=200), 200

# ------------------------------------------------------------------------
# Інформація про розклад руху поїзда
def getTrainRouteRow(idRow:int):
  """
  інформація про рядок розкладу руху поїзда
  """    
  row = (db.session.query(TrainRoute)
           .filter(TrainRoute.id == idRow)
           .first())
  return row

@app.route('/api/train_route/<int:idTrain>')
@app.route('/api/train_route/<int:idTrain>/<int:startNumOrder>')
def getTrainRoute(idTrain:int, startNumOrder:int = None):
  """
  розклад руху поїзда
  """    
  trainRoute = (db.session.query(TrainRoute.id, TrainRoute.numOrder, 
                             TrainRoute.station, Station.nameStation,
                             TrainRoute.hoursArr, TrainRoute.minutesArr,
                             TrainRoute.hoursDepart, TrainRoute.minutesDepart)
            .filter(TrainRoute.idTrain == idTrain, True if startNumOrder == None else TrainRoute.numOrder >= startNumOrder)            
              # поєднуємо з таблицею станцій для відображення назви станції маршруту слідування
              .join(Station)
              .order_by(TrainRoute.numOrder)
              .all())

  # Перетворюємо у масив словників (для подальшої серіалізації в json) 
  trainRouteData = [{
        "id": routeRow.id,
        "numOrder": routeRow.numOrder,
        "station": routeRow.station,
        "hoursArr": routeRow.hoursArr,
        "minutesArr": routeRow.minutesArr,
        "hoursDepart": routeRow.hoursDepart,
        "minutesDepart": routeRow.minutesDepart,
        "nameStation": routeRow.nameStation          
  } for routeRow in trainRoute]
  return trainRouteData

@app.route('/train_route_row_info') 
@app.route('/train_route_row_info.html') 
def trainRouteRowInfo():
  """
  сторінка даних для вводу/коригування інформації про рядок розкладу руху
  """  
  trainRouteRowInfoForm = TrainRouteRowInfoForm()

  # заповнення випадаючого списку станцій
  trainRouteRowInfoForm.station.choices = getStations()

  idRow = request.args.get('id_row', default=None, type=int) 
  idTrain = request.args.get('id_train', default=None, type=int)  

  # якщо це існуючий рядок
  if (idRow != None):      
    trainRouteRowInfoForm.id_row.data = idRow    
    # отримуємо з БД інформацію про поїзд
    row = getTrainRouteRow(idRow)
    if row == None:
      return jsonify(message=f"Рядок розкладу не знайдений", code=404), 404
    
    trainRouteRowInfoForm.num_order.data = row.numOrder
    trainRouteRowInfoForm.id_train.data = row.idTrain
    trainRouteRowInfoForm.station.data = row.station
    trainRouteRowInfoForm.hours_arr.data = row.hoursArr
    trainRouteRowInfoForm.minutes_arr.data = row.minutesArr
    trainRouteRowInfoForm.hours_depart.data = row.hoursDepart
    trainRouteRowInfoForm.minutes_depart.data = row.minutesDepart
  else:
    trainRouteRowInfoForm.id_train.data = idTrain
  return (
    render_template("train_route_row_info.html", 
                    form = trainRouteRowInfoForm)) 

def __reorderNumOrder__(idRow, idTrain, numOrder):
  """
  Автоматична перенумерація номерів рядків
  """
  currNumOrder = numOrder + 1
  nextRows = (db.session.query(TrainRoute)
          .filter(TrainRoute.idTrain == idTrain, 
                  TrainRoute.numOrder >= numOrder,
                  TrainRoute.id != idRow)            
            .order_by(TrainRoute.numOrder)
            .all())
  
  for row in nextRows:
    print("nextRow=", row)
    print("currNumOrder=", currNumOrder)
    row.numOrder = currNumOrder
    currNumOrder += 1
  return

@app.route('/api/train_route/new', methods=['post']) 
def newTrainRouteRow():
  """
  створення нового рядку розкладу
  """
  trainRouteRowInfoForm = TrainRouteRowInfoForm()    
  idTrain = trainRouteRowInfoForm.id_train.data 
  # заповнення випадаючого списку станцій
  trainRouteRowInfoForm.station.choices = getStations()

  if trainRouteRowInfoForm.validate_on_submit(): 
        
    newRow = TrainRoute(
      idTrain = idTrain,
      numOrder = trainRouteRowInfoForm.num_order.data,
      station = trainRouteRowInfoForm.station.data,
      hoursArr = trainRouteRowInfoForm.hours_arr.data,
      minutesArr = trainRouteRowInfoForm.minutes_arr.data,
      hoursDepart = trainRouteRowInfoForm.hours_depart.data,
      minutesDepart = trainRouteRowInfoForm.minutes_depart.data
    )  
    # Додаємо новий рядок розкладу та зберігаємо
    db.session.add(newRow) 
    db.session.commit()  
    print("newRow_id=", newRow.id)

    # Автомат. перенумерація номерів рядків
    __reorderNumOrder__(newRow.id, idTrain, newRow.numOrder)   
    db.session.commit()  

    return newRow.to_dict()
  
  return jsonify(message=f"Помилка валідації даних форми", code=600), 600

@app.route('/api/train_route/edit', methods=['post']) 
def editTrainRouteRow():
  """
  редагування даних про рядок розкладу
  """
  trainRouteRowInfoForm = TrainRouteRowInfoForm()    
  # заповнення випадаючого списку станцій
  trainRouteRowInfoForm.station.choices = getStations()
  
  if trainRouteRowInfoForm.validate_on_submit():
    idRow = trainRouteRowInfoForm.id_row.data
    print("idRow=", idRow)    
       
    editedRow = getTrainRouteRow(idRow)
    print("oldRow=", editedRow.to_dict()) 

    if editedRow == None:      
      # якщо поїзд за id не знайдений, відправляємо статусний код і повідомлення про помилку
      return jsonify(message=f"Рядок у розкладі з id={idRow} не знайдений у БД", code=404), 404
    
    editedRow.numOrder = trainRouteRowInfoForm.num_order.data
    editedRow.hoursArr = trainRouteRowInfoForm.hours_arr.data
    editedRow.minutesArr = trainRouteRowInfoForm.minutes_arr.data
    editedRow.hoursDepart = trainRouteRowInfoForm.hours_depart.data
    editedRow.minutesDepart = trainRouteRowInfoForm.minutes_depart.data
    editedRow.station = trainRouteRowInfoForm.station.data
    
    # Автомат. перенумерація номерів рядків
    __reorderNumOrder__(editedRow.id, editedRow.idTrain, editedRow.numOrder)       
    db.session.commit()
    return editedRow.to_dict()
  
  return jsonify(message=f"Помилка валідації даних форми", code=600), 600 

@app.route('/api/train_route/delete/<int:idRow>', methods=['delete']) 
def deleteTrainRouteRow(idRow:int):
  """
  видалення даних рядку в розкладу
  """
  deletedRow = getTrainRouteRow(idRow)
  if deletedRow == None:      
    # якщо рядок за id не знайдений, відправляємо статусний код і повідомлення про помилку
    return jsonify(message=f"`Рядок у розкладі з id={idRow} не знайдений у БД", code=404), 404
    
  db.session.delete(deletedRow)
  # Автомат. перенумерація номерів рядків
  __reorderNumOrder__(idRow, deletedRow.idTrain, deletedRow.numOrder - 1) 
  db.session.commit()   
  return jsonify(message="deleted: True", code=200), 200

