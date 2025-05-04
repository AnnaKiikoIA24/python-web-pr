"""
  масив груп студентів
"""  
aGroups = [
  {
    "id": 1,
    "name": "ІА-21"
  },
  {
    "id": 2,
    "name": "ІА-22"
  },
  {
    "id": 3,
    "name": "ІА-23"
  },
  {
    "id": 4,
    "name": "ІА-24"
  }]

"""
масив користувачів системи
"""  
aUsers = [
  {
    "id": 1,
    "login": "rolik.a@lll.kpi.ua",
    "password": "1234",
    "firstName": "Олександр",
    "lastName": "Ролік",
    "role": False,
    "idGroup": None,
    "name": None
  },
  {
    "id": 2,
    "login": "barbaruk@lll.kpi.ua",
    "password": "1234",
    "firstName": "Віктор",
    "lastName": "Барбарук",
    "role": False,
    "idGroup": None,
    "name": None
  },
  {
    "id": 3,
    "login": "akiyko@lll.kpi.ua",
    "password": "1111",
    "firstName": "Анна",
    "lastName": "Кійко",
    "role": True,
    "idGroup": 4,
    "name": "ІА-24"
  },
  {
    "id": 4,
    "login": "yablon@lll.kpi.ua",
    "password": "1111",
    "firstName": "Данил",
    "lastName": "Яблонський",
    "role": True,
    "idGroup": 4
  },
  {
    "id": 5,
    "login": "karmazina@lll.kpi.ua",
    "password": "1111",
    "firstName": "Анастасія",
    "lastName": "Кармазіна",
    "role": True,
    "idGroup": 4,
    "name": "ІА-24"
  },
  {
    "id": 6,
    "login": "chayka@lll.kpi.ua",
    "password": "1111",
    "firstName": "Антон",
    "lastName": "Чайка",
    "role": True,
    "idGroup": 4,
    "name": "ІА-24"
  },
  {
    "id": 7,
    "login": "bodnar@lll.kpi.ua",
    "password": "1111",
    "firstName": "Антон",
    "lastName": "Боднар",
    "role": True,
    "idGroup": 4,
    "name": "ІА-24"
  },
  {
    "id": 8,
    "login": "kravec@lll.kpi.ua",
    "password": "1234",
    "firstName": "Петро",
    "lastName": "Кравець",
    "role": False,
    "group": None,
    "name": None
  },
  {
    "id": 9,
    "login": "cymbal@lll.kpi.ua",
    "password": "1234",
    "firstName": "Святослав",
    "lastName": "Цимбал",
    "role": False,
    "idGroup": None,
    "name": None
  },
  {
    "id": 10,
    "login": "sidenko@lll.kpi.ua",
    "password": "1111",
    "firstName": "Дарина",
    "lastName": "Сіденко",
    "role": True,
    "idGroup": 4,
    "name": "ІА-24"
  },
  {
    "id": 11,
    "login": "zelinsk@lll.kpi.ua",
    "password": "1111",
    "firstName": "Іван",
    "lastName": "Зелінський",
    "role": True,
    "idGroup": 4,
    "name": "ІА-24"
  },
  {
    "id": 12,
    "login": "kotlyar@lll.kpi.ua",
    "password": "1111",
    "firstName": "Максим",
    "lastName": "Котлярчук",
    "role": True,
    "idGroup": 4,
    "name": "ІА-24"
  },
  {
    "id": 13,
    "login": "orlovska@lll.kpi.ua",
    "password": "1111",
    "firstName": "Анна",
    "lastName": "Орловська",
    "role": True,
    "idGroup": 4,
    "name": "ІА-24"
  }]

"""
масив навчальних предметів
"""
aSubjects = [
  {
    "id": 1,
    "nameShort": "КМ",
    "nameFull": "Комп'ютерні мережі"
  },
  {
    "id": 2,
    "nameShort": "Web Python",
    "nameFull": "Сучасні технології розробки WEB-застосувань з використанням мови Python"
  },
  {
    "id": 3,
    "nameShort": "ТРПЗ",
    "nameFull": "Технічна розробка програмного забезпечення"
  },
  {
    "id": 4,
    "nameShort": "ІІТ",
    "nameFull": "Інфраструктура інформаційних систем"
  },
  {
    "id": 5,
    "nameShort": "БІС",
    "nameFull": "Безпека інформаційних систем"
  },
  {
    "id": 6,
    "nameShort": "ТАК",
    "nameFull": "Теорія автоматичного керування"
  },
  {
    "id": 7,
    "nameShort": "СІ",
    "nameFull": "Системна інженерія"
  },
  {
    "id": 8,
    "nameShort": "ВМ",
    "nameFull": "Вища математика"
  },
  {
    "id": 9,
    "nameShort": "ОКР",
    "nameFull": "Основи клієнтської розробки"
  }]

"""
масив журналів успішності
"""
aJournals = [
  { "id": 1,
    "year": 2024,
    "idGroup": 4,
    "name": "ІА-24"
  },    
  { "id": 2,
    "year": 2023,
    "idGroup": 4,
    "name": "ІА-24"
  },
  { "id": 3,
    "year": 2024,
    "idGroup": 1,
    "name": "ІА-21"
  },            
]

"""
масив занять
"""
aLessons = [{
    "id": 1,
    "theme": "Віртуалізація",
    "maxGrade": None,
    "dateLesson": "2025-04-20",
    "idJournal": 1,
    "idSubject": 1,
    "idTeacher": 1
  }]

"""
масив рейтингів
"""
aRating = [
  {
    "id": 1,
    "grade": 5,
    "idLesson": 1,
    "idStudent": 3,
    "isPresence": True
  },
    {
    "id": 1,
    "grade": 4,
    "idLesson": 1,
    "idStudent": 4,
    "isPresence": True
  },
    {
    "id": 1,
    "grade": None,
    "idLesson": 1,
    "idStudent": 5,
    "isPresence": False
  },
  ]