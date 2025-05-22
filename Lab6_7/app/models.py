from app import db
from sqlalchemy.orm import declarative_base
 
# створюємо модель, об'єкти якої зберігатимуться в БД 
# Станція
class Station(db.Model): 
  __tablename__ = "stations" 

  id = db.Column("id", db.Integer, primary_key=True, index=True, autoincrement=True) 
  codeStation = db.Column("code_station", db.Integer, nullable=False, unique=True)
  nameStation = db.Column("name_station", db.String(40), nullable=False) 

  # створює рядкове представлення об'єкта
  def __repr__(self): 
    return "<{}: {} ({})>".format(id, self.nameStation, self.codeStation) 
  def to_dict(self):
    return {
        "id": self.id,
        "codeStation": self.codeStation,
        "nameStation": self.nameStation
    }   
  
# Таблиця асоціацій створюється за допомогою SQLAlchemy Core
period_trains = db.Table('period_trains', 
    db.Column('period_id', db.Integer, db.ForeignKey('periods.id'), primary_key=True), 
    db.Column('train_id', db.Integer, db.ForeignKey('trains.id'), primary_key=True) 
) 

# Період дії розкладу
class Period(db.Model): 
  __tablename__ = "periods" 

  id = db.Column("id", db.Integer, primary_key=True, index=True, autoincrement=True) 
  dateBeg = db.Column("date_beg", db.Date, nullable=False)
  dateEnd = db.Column("date_end", db.Date, nullable=False) 
  # якщо двосторонній зв'язок  
  #trains = db.relationship('Train', secondary=period_trains, back_populates='periodsTrain')
  db.CheckConstraint("date_beg <= date_end", name="check_dates")

  def __repr__(self): 
    return "<{}: {}--{}>".format(id, self.dateBeg, self.dateEnd) 
  def to_dict(self):
    return {
        "id": self.id,
        "dateBeg": self.dateBeg.strftime("%d.%m.%Y"),
        "dateEnd": self.dateEnd.strftime("%d.%m.%Y")
    }     
  
# Поїзд
class Train(db.Model): 
  __tablename__ = "trains" 

  id = db.Column("id", db.Integer, primary_key=True, index=True, autoincrement=True) 
  numTrain = db.Column("num_train", db.Integer, nullable=False)
  stationFrom = db.Column("station_from", db.Integer, db.ForeignKey("stations.id"), nullable=False)
  stationTo = db.Column("station_to", db.Integer, db.ForeignKey("stations.id"), nullable=False)
  route = db.relationship('TrainRoute', backref='trains') 
  periodsTrain = db.relationship('Period', secondary=period_trains, backref='trains')
  # якщо двосторонній зв'язок 
  # periodsTrain = db.relationship('Period', secondary=period_trains, back_populates='trains')    
  
  def __repr__(self): 
    return "<{}: {} ({}--{})>".format(id, self.numTrain, self.stationFrom, self.stationTo)   
  def to_dict(self):
    return {
        "id": self.id,
        "numTrain": self.numTrain,
        "stationFrom": self.stationFrom,
        "stationTo": self.stationTo
        #"route": self.route
    }
  
# Маршрут руху поїзда
class TrainRoute(db.Model):
  __tablename__ = "train_route" 

  id = db.Column("id", db.Integer, primary_key=True, index=True, autoincrement=True) 
  idTrain = db.Column("id_train", db.Integer, db.ForeignKey("trains.id"), nullable=False)
  numOrder = db.Column("num_order", db.Integer, nullable=False)
  station = db.Column("station", db.Integer, db.ForeignKey("stations.id"), nullable=False)
  hoursArr = db.Column("hours_arr", db.Integer)
  minutesArr = db.Column("minutes_arr", db.Integer)
  hoursDepart = db.Column("hours_depart", db.Integer)  
  minutesDepart = db.Column("minutes_depart", db.Integer)
  
  def __repr__(self): 
    return "<{}: ({}--{})>".format(id, self.numOrder, self.station)   
  def to_dict(self):
    return {
        "id": self.id,
        "idTrain": self.idTrain,
        "numOrder": self.numOrder,
        "station": self.station,
        "hoursArr": self.hoursArr,
        "minutesArr": self.minutesArr,
        "hoursDepart": self.hoursDepart,
        "minutesDepart": self.minutesDepart
    }
  
# Користувач
class User(db.Model): 
  __tablename__ = "users" 

  id = db.Column("id", db.Integer, primary_key=True, autoincrement=True) 
  login = db.Column(db.String(30), unique=True, index=True, nullable=False)
  password = db.Column(db.String(20), nullable=False)
  firstName = db.Column("first_name", db.String(25), nullable=False)
  lastName = db.Column("last_name", db.String(25), nullable=False)
  role = db.Column(db.Boolean(), nullable=False)
  db.CheckConstraint("role in (1,0)", name="check_role")

  def __repr__(self): 
    return "<{}) {}: {} {} роль {})>".format(id, self.login, self.firstName, self.lastName, self.role)
  def to_dict(self):
    return {
        "id": self.id,
        "login": self.login,
        "password": self.password,
        "lastName": self.lastName,
        "firstName": self.firstName,        
        "role": self.role  
    }    

