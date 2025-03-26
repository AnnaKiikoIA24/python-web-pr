from sqlalchemy import create_engine 
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy import Column, Integer, String, ForeignKey, CheckConstraint, Boolean, Date
from sqlalchemy.sql import expression
from sqlalchemy.orm import sessionmaker 
   
# рядок підключення 
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_journal.db" 
  
# створюємо рушій SqlAlchemy 
engine = create_engine( 
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": 
False} 
) 
#створюємо базовий клас для моделей 
Base = declarative_base() 
  
# створюємо модель, об'єкти якої зберігатимуться в бд 
# Навчальний предмет
class Subject(Base): 
    __tablename__ = "subjects" 
  
    id = Column("subject_id", Integer, primary_key=True, index=True, autoincrement=True) 
    nameShort = Column("name_short", String(20), nullable=False)
    nameFull = Column("name_full",String(60), nullable=False) 
  
# Група
class Group(Base): 
    __tablename__ = "groups" 
  
    id = Column("group_id", Integer, primary_key=True, autoincrement=True) 
    name = Column(String(10), nullable=False)

# Користувач
class User(Base): 
    __tablename__ = "users" 
  
    id = Column("user_id", Integer, primary_key=True, autoincrement=True) 
    login = Column(String(15), unique=True, index=True, nullable=False)
    password = Column(String(20), nullable=False)
    firstName = Column("first_name", String(20), nullable=False)
    lastName = Column("last_name", String(25), nullable=False)
    role = Column(Boolean(), nullable=False)
    idGroup = Column("id_group", Integer, ForeignKey("groups.group_id"))
    CheckConstraint("role in (1,0)", name="check_role")

# Журнал
class Journal(Base):
    __tablename__ = "journals"

    id = Column("journal_id", Integer, primary_key=True, autoincrement=True)
    year = Column(Integer, nullable=False)
    idGroup = Column("id_group", Integer, ForeignKey("groups.group_id"), nullable=False)

# Заняття
class Lesson(Base):
    __tablename__ = "lessons"

    id = Column("lesson_id", Integer, primary_key=True, autoincrement=True)
    idSubject = Column("id_subject", Integer, ForeignKey("subjects.subject_id"), nullable=False)
    idTeacher = Column("id_teacher", Integer, ForeignKey("users.user_id"), nullable=False)
    dateLesson = Column("date_lesson", Date, nullable=False)
    idJournal = Column("id_journal", Integer, ForeignKey("journals.journal_id"), nullable=False)
    theme = Column(String(150))
    maxGrade = Column("max_grade", Integer)

# Рейтинг
class Rating(Base):
    __tablename__ = "ratings"
    id = Column("rating_id", Integer, primary_key=True, autoincrement=True)
    idLesson = Column("id_lesson", Integer, ForeignKey("lessons.lesson_id"), nullable=False)
    idStudent = Column("id_student", Integer, ForeignKey("users.user_id"), nullable=False)
    isPresence = Column("is_presence", Boolean(), server_default=expression.true())
    grade = Column(Integer)


# визначаємо залежність 
# функція get_db(), через яку об'єкт сесії бази даних буде передаватися у функцію обробки
def get_db(): 
    # створюємо об'єкт сесії бази даних
    db = SessionLocal() 
    try: 
        # yield  буде  виконуватися  при отриманні кожного нового запиту
        yield db 
    finally: 
        db.close() 
        
SessionLocal = sessionmaker(autoflush=False, bind=engine) 
# створюємо таблиці 
Base.metadata.create_all(bind=engine) 