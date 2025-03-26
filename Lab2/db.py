import psycopg2 
from fastapi import FastAPI 

# У разі вдалого підключення функція connect створює нову сесію бази даних і 
# повертає  об'єкт  connection.
conn = psycopg2.connect(dbname="journal", user="postgres", password="12345", host="127.0.0.1") 
print("Підключення встановлено") 
cursor = conn.cursor() 
  
conn.autocommit = True 

# =================================================================
cursor.execute("DROP TABLE IF EXISTS public.ratings")
conn.commit()

cursor.execute("DROP TABLE IF EXISTS public.lessons")
conn.commit()

cursor.execute("DROP TABLE IF EXISTS public.journals")
conn.commit()

cursor.execute("DROP TABLE IF EXISTS public.users")
conn.commit()

cursor.execute("DROP TABLE IF EXISTS public.groups")
conn.commit()

cursor.execute("DROP TABLE IF EXISTS public.subjects")
conn.commit()

# =================================================================
# створюємо таблицю groups
cursor.execute("CREATE TABLE groups (group_id SERIAL PRIMARY KEY, name VARCHAR(10) NOT NULL)")
conn.commit()
print("Таблиця groups успішно створена")  

# дані для додавання 
cursor.execute("INSERT INTO groups (group_id, name) VALUES (1, 'ІА-21')") 
cursor.execute("INSERT INTO groups (group_id, name) VALUES (2, 'ІА-22')") 
cursor.execute("INSERT INTO groups (group_id, name) VALUES (3, 'ІА-23')") 
cursor.execute("INSERT INTO groups (group_id, name) VALUES (4, 'ІА-24')") 
conn.commit()   
print("Дані до таблиці 'groups' додано") 

# =================================================================
# створюємо таблицю subjects
cursor.execute("CREATE TABLE subjects (subject_id SERIAL PRIMARY KEY, name_short VARCHAR(20) NOT NULL, name_full VARCHAR(80) NOT NULL)")
conn.commit()
print("Таблиця subjects успішно створена")  

# дані для додавання 
cursor.execute("INSERT INTO subjects (subject_id, name_short, name_full) VALUES (1, 'КМ', 'Комп''ютерні мережі')")
cursor.execute("INSERT INTO subjects (subject_id, name_short, name_full) VALUES (2, 'Web Python', 'Сучасні технології розробки WEB-застосувань з використанням мови Python')")
cursor.execute("INSERT INTO subjects (subject_id, name_short, name_full) VALUES (3, 'ТРПЗ', 'Технічна розробка програмного забезпечення')")
cursor.execute("INSERT INTO subjects (subject_id, name_short, name_full) VALUES (4, 'ІІТ', 'Інфраструктура інформаційних систем')")
cursor.execute("INSERT INTO subjects (subject_id, name_short, name_full) VALUES (5, 'БІС', 'Безпека інформаційних систем')")
cursor.execute("INSERT INTO subjects (subject_id, name_short, name_full) VALUES (6, 'ТАК', 'Теорія автоматичного керування')")
cursor.execute("INSERT INTO subjects (subject_id, name_short, name_full) VALUES (7, 'СІ', 'Системна інженерія')")
cursor.execute("INSERT INTO subjects (subject_id, name_short, name_full) VALUES (8, 'ВМ', 'Вища математика')")
cursor.execute("INSERT INTO subjects (subject_id, name_short, name_full) VALUES (9, 'ОКР', 'Основи клієнтської розробки')")
conn.commit()   
print("Дані до таблиці 'subjects' додано") 

# =================================================================
# створюємо таблицю users
cursor.execute("""CREATE TABLE users (
	user_id SERIAL PRIMARY KEY,
	login	VARCHAR(25) NOT NULL,
	password VARCHAR(20) NOT NULL,
	first_name VARCHAR(25) NOT NULL,
	last_name VARCHAR(25) NOT NULL,
	role BOOLEAN NOT NULL,
	id_group INTEGER,
	CONSTRAINT FK_User_Group FOREIGN KEY(id_group) REFERENCES groups(group_id))""")
conn.commit()
print("Таблиця 'users' успішно створена")  

# дані для додавання 
cursor.execute("INSERT INTO users (user_id, login, password, first_name, last_name, role, id_group) VALUES (1, 'rolik.a@lll.kpi.ua', '1234', 'Олександр', 'Ролік', false, null)")
cursor.execute("INSERT INTO users (user_id, login, password, first_name, last_name, role, id_group) VALUES (2, 'barbaruk@lll.kpi.ua', '1234', 'Барбарук', 'Віктор', false, null)")
cursor.execute("INSERT INTO users (user_id, login, password, first_name, last_name, role, id_group) VALUES (3, 'akiyko@lll.kpi.ua', '1111', 'Кійко', 'Анна', true, 4)")
cursor.execute("INSERT INTO users (user_id, login, password, first_name, last_name, role, id_group) VALUES (4, 'yablon@lll.kpi.ua', '1111', 'Яблонський', 'Данил', true, 4)")
cursor.execute("INSERT INTO users (user_id, login, password, first_name, last_name, role, id_group) VALUES (5, 'karmazina@lll.kpi.ua', '1111', 'Кармазіна', 'Анастасія', true, 4)")
cursor.execute("INSERT INTO users (user_id, login, password, first_name, last_name, role, id_group) VALUES (6, 'chayka@lll.kpi.ua', '1111', 'Чайка', 'Антон', true, 4)")
cursor.execute("INSERT INTO users (user_id, login, password, first_name, last_name, role, id_group) VALUES (7, 'bodnar@lll.kpi.ua', '1111', 'Боднар', 'Антон', true, 4)")
cursor.execute("INSERT INTO users (user_id, login, password, first_name, last_name, role, id_group) VALUES (8, 'kravec@lll.kpi.ua', '1234', 'Кравець', 'Петро', false, null)")
cursor.execute("INSERT INTO users (user_id, login, password, first_name, last_name, role, id_group) VALUES (9, 'cymbal@lll.kpi.ua', '1234', 'Цимбал', 'Святослав', false, null)")
cursor.execute("INSERT INTO users (user_id, login, password, first_name, last_name, role, id_group) VALUES (10, 'sidenko@lll.kpi.ua', '1111', 'Сіденко', 'Дар''я', true, 4)")
cursor.execute("INSERT INTO users (user_id, login, password, first_name, last_name, role, id_group) VALUES (11, 'zelinsk@lll.kpi.ua', '1111', 'Зелінський', 'Іван ', true, 4)")
cursor.execute("INSERT INTO users (user_id, login, password, first_name, last_name, role, id_group) VALUES (12, 'kotlyar@lll.kpi.ua', '1111', 'Котлярчук ', 'Максим ', true, 4)")
cursor.execute("INSERT INTO users (user_id, login, password, first_name, last_name, role, id_group) VALUES (13, 'orlovska@lll.kpi.ua', '1111', 'Орловська ', 'Анна ', true, 4)")
conn.commit()   
print("Дані до таблиці 'users' додано") 

# =================================================================
# створюємо таблицю journals
cursor.execute("""CREATE TABLE journals (
	journal_id SERIAL PRIMARY KEY, 
	year INTEGER NOT NULL, 
	id_group INTEGER NOT NULL,  
	CONSTRAINT FK_Journal_Group FOREIGN KEY(id_group) REFERENCES groups (group_id)
)""")
conn.commit()
print("Таблиця 'journals' успішно створена")  

# дані для додавання 
cursor.execute("INSERT INTO journals (journal_id, year, id_group) VALUES (1, 2024, 4)")
cursor.execute("INSERT INTO journals (journal_id, year, id_group) VALUES (2, 2023, 4)")
conn.commit()   
print("Дані до таблиці 'journals' додано") 

# =================================================================
# створюємо таблицю lessons
cursor.execute("""CREATE TABLE lessons (
	lesson_id	SERIAL PRIMARY KEY,
	id_subject	INTEGER NOT NULL,
	id_teacher	INTEGER NOT NULL,
	date_lesson	DATE NOT NULL,
	id_journal	INTEGER NOT NULL,
	theme	VARCHAR(200),
	max_grade INTEGER,
	CONSTRAINT FK_Lesson_Subject FOREIGN KEY(id_subject) REFERENCES subjects(subject_id),
	CONSTRAINT FK_Lesson_User FOREIGN KEY(id_teacher) REFERENCES users(user_id),
	CONSTRAINT FK_Lesson_Journal FOREIGN KEY(id_journal) REFERENCES journals(journal_id)
)""")
conn.commit()
print("Таблиця 'lessons' успішно створена")  

# дані для додавання
cursor.execute("INSERT INTO lessons (lesson_id, id_subject, id_teacher, date_lesson, id_journal, theme, max_grade) VALUES (1, 1, 1, '2024-02-20', 2, 'Протоколи передачі даних', null)")
cursor.execute("INSERT INTO lessons (lesson_id, id_subject, id_teacher, date_lesson, id_journal, theme, max_grade) VALUES (2, 1, 1, '2024-02-11', 2, 'Вступ. Основні поняття КМ', null)")
cursor.execute("INSERT INTO lessons (lesson_id, id_subject, id_teacher, date_lesson, id_journal, theme, max_grade) VALUES (3, 1, 9, '2024-02-15', 2, 'Лабор. роб. №1', 5)")
cursor.execute("INSERT INTO lessons (lesson_id, id_subject, id_teacher, date_lesson, id_journal, theme, max_grade) VALUES (4, 1, 9, '2024-02-22', 2, 'Лабор. роб. №2', 5)")
cursor.execute("INSERT INTO lessons (lesson_id, id_subject, id_teacher, date_lesson, id_journal, theme, max_grade) VALUES (5, 4, 9, '2025-02-18', 1, 'Лабор. роб. №1', 5)")
cursor.execute("INSERT INTO lessons (lesson_id, id_subject, id_teacher, date_lesson, id_journal, theme, max_grade) VALUES (6, 4, 9, '2025-02-25', 1, 'Лабор. роб. №2', 5)")
cursor.execute("INSERT INTO lessons (lesson_id, id_subject, id_teacher, date_lesson, id_journal, theme, max_grade) VALUES (7, 4, 1, '2025-02-08', 1, 'Вступна лекція.', null)")
cursor.execute("INSERT INTO lessons (lesson_id, id_subject, id_teacher, date_lesson, id_journal, theme, max_grade) VALUES (8, 4, 1, '2025-02-15', 1, 'Основи віртуалізації', null)")
cursor.execute("INSERT INTO lessons (lesson_id, id_subject, id_teacher, date_lesson, id_journal, theme, max_grade) VALUES (9, 4, 1, '2025-02-25', 1, 'VirtualBox, Hyper-V', null)")
cursor.execute("INSERT INTO lessons (lesson_id, id_subject, id_teacher, date_lesson, id_journal, theme, max_grade) VALUES (10, 4, 1, '2025-03-11', 1, 'Dockers.', null)")
cursor.execute("INSERT INTO lessons (lesson_id, id_subject, id_teacher, date_lesson, id_journal, theme, max_grade) VALUES (11, 4, 9, '2025-03-10', 1, 'Лабор. роб. №3', 4)")
cursor.execute("INSERT INTO lessons (lesson_id, id_subject, id_teacher, date_lesson, id_journal, theme, max_grade) VALUES (12, 2, 2, '2025-03-11', 1, 'Лабор. роб. №1. FastAPI та SQLAlchemy ORM', 5)")
conn.commit()   
print("Дані до таблиці 'lessons' додано") 

# =================================================================
# створюємо таблицю ratings
cursor.execute("""CREATE TABLE ratings (
	rating_id SERIAL PRIMARY KEY, 
	id_lesson INTEGER NOT NULL, 
	id_student INTEGER NOT NULL, 
	is_presence BOOLEAN DEFAULT (true), 
	grade INTEGER,  
	CONSTRAINT FK_Rating_Lesson FOREIGN KEY(id_lesson) REFERENCES lessons (lesson_id), 
	CONSTRAINT FK_Rating_User FOREIGN KEY(id_student) REFERENCES users (user_id)
)""")
conn.commit()
print("Таблиця 'ratings' успішно створена")  

# дані для додавання
cursor.execute("INSERT INTO ratings (rating_id, id_lesson, id_student, is_presence, grade) VALUES (1, 1, 7, true, null)")
cursor.execute("INSERT INTO ratings (rating_id, id_lesson, id_student, is_presence, grade) VALUES (2, 1, 11, true, null)")
cursor.execute("INSERT INTO ratings (rating_id, id_lesson, id_student, is_presence, grade) VALUES (3, 1, 5, true, null)")
cursor.execute("INSERT INTO ratings (rating_id, id_lesson, id_student, is_presence, grade) VALUES (4, 1, 12, false, null)")
cursor.execute("INSERT INTO ratings (rating_id, id_lesson, id_student, is_presence, grade) VALUES (5, 1, 3, true, null)")
cursor.execute("INSERT INTO ratings (rating_id, id_lesson, id_student, is_presence, grade) VALUES (6, 1, 13, true, null)")
cursor.execute("INSERT INTO ratings (rating_id, id_lesson, id_student, is_presence, grade) VALUES (7, 1, 10, true, null)")
cursor.execute("INSERT INTO ratings (rating_id, id_lesson, id_student, is_presence, grade) VALUES (8, 1, 6, true, null)")
cursor.execute("INSERT INTO ratings (rating_id, id_lesson, id_student, is_presence, grade) VALUES (9, 1, 4, true, null)")
cursor.execute("INSERT INTO ratings (rating_id, id_lesson, id_student, is_presence, grade) VALUES (10, 2, 7, false, null)")
cursor.execute("INSERT INTO ratings (rating_id, id_lesson, id_student, is_presence, grade) VALUES (11, 2, 11, true, null)")
cursor.execute("INSERT INTO ratings (rating_id, id_lesson, id_student, is_presence, grade) VALUES (12, 2, 5, true, null)")
cursor.execute("INSERT INTO ratings (rating_id, id_lesson, id_student, is_presence, grade) VALUES (13, 2, 12, true, null)")
cursor.execute("INSERT INTO ratings (rating_id, id_lesson, id_student, is_presence, grade) VALUES (14, 2, 3, true, null)")
cursor.execute("INSERT INTO ratings (rating_id, id_lesson, id_student, is_presence, grade) VALUES (15, 2, 13, true, null)")
cursor.execute("INSERT INTO ratings (rating_id, id_lesson, id_student, is_presence, grade) VALUES (16, 2, 10, true, null)")
cursor.execute("INSERT INTO ratings (rating_id, id_lesson, id_student, is_presence, grade) VALUES (17, 2, 6, false, null)")
cursor.execute("INSERT INTO ratings (rating_id, id_lesson, id_student, is_presence, grade) VALUES (18, 2, 4, true, null)")
cursor.execute("INSERT INTO ratings (rating_id, id_lesson, id_student, is_presence, grade) VALUES (19, 3, 7, true, 4)")
cursor.execute("INSERT INTO ratings (rating_id, id_lesson, id_student, is_presence, grade) VALUES (20, 3, 11, true, 5)")
cursor.execute("INSERT INTO ratings (rating_id, id_lesson, id_student, is_presence, grade) VALUES (21, 3, 5, true, 3)")
cursor.execute("INSERT INTO ratings (rating_id, id_lesson, id_student, is_presence, grade) VALUES (22, 3, 12, true, 4)")
cursor.execute("INSERT INTO ratings (rating_id, id_lesson, id_student, is_presence, grade) VALUES (23, 3, 3, true, 4)")
cursor.execute("INSERT INTO ratings (rating_id, id_lesson, id_student, is_presence, grade) VALUES (24, 3, 13, true, 4)")
cursor.execute("INSERT INTO ratings (rating_id, id_lesson, id_student, is_presence, grade) VALUES (25, 3, 10, true, 4)")
cursor.execute("INSERT INTO ratings (rating_id, id_lesson, id_student, is_presence, grade) VALUES (26, 3, 6, true, 5)")
cursor.execute("INSERT INTO ratings (rating_id, id_lesson, id_student, is_presence, grade) VALUES (27, 3, 4, true, 5)")
cursor.execute("INSERT INTO ratings (rating_id, id_lesson, id_student, is_presence, grade) VALUES (28, 4, 7, true, 4)")
cursor.execute("INSERT INTO ratings (rating_id, id_lesson, id_student, is_presence, grade) VALUES (29, 4, 11, false, null)")
cursor.execute("INSERT INTO ratings (rating_id, id_lesson, id_student, is_presence, grade) VALUES (30, 4, 5, true, 4)")
cursor.execute("INSERT INTO ratings (rating_id, id_lesson, id_student, is_presence, grade) VALUES (31, 4, 12, true, 4)")
cursor.execute("INSERT INTO ratings (rating_id, id_lesson, id_student, is_presence, grade) VALUES (32, 4, 3, false, null)")
cursor.execute("INSERT INTO ratings (rating_id, id_lesson, id_student, is_presence, grade) VALUES (33, 4, 13, true, 5)")
cursor.execute("INSERT INTO ratings (rating_id, id_lesson, id_student, is_presence, grade) VALUES (34, 4, 10, true, 4)")
cursor.execute("INSERT INTO ratings (rating_id, id_lesson, id_student, is_presence, grade) VALUES (35, 4, 6, true, 4)")
cursor.execute("INSERT INTO ratings (rating_id, id_lesson, id_student, is_presence, grade) VALUES (36, 4, 4, true, 5)")
cursor.execute("INSERT INTO ratings (rating_id, id_lesson, id_student, is_presence, grade) VALUES (37, 5, 7, false, null)")
cursor.execute("INSERT INTO ratings (rating_id, id_lesson, id_student, is_presence, grade) VALUES (38, 5, 11, true, 5)")
cursor.execute("INSERT INTO ratings (rating_id, id_lesson, id_student, is_presence, grade) VALUES (39, 5, 5, true, 4)")
cursor.execute("INSERT INTO ratings (rating_id, id_lesson, id_student, is_presence, grade) VALUES (40, 5, 12, true, 4)")
cursor.execute("INSERT INTO ratings (rating_id, id_lesson, id_student, is_presence, grade) VALUES (41, 5, 3, true, 5)")
cursor.execute("INSERT INTO ratings (rating_id, id_lesson, id_student, is_presence, grade) VALUES (42, 5, 13, true, 4)")
cursor.execute("INSERT INTO ratings (rating_id, id_lesson, id_student, is_presence, grade) VALUES (43, 5, 10, true, 4)")
cursor.execute("INSERT INTO ratings (rating_id, id_lesson, id_student, is_presence, grade) VALUES (44, 5, 6, false, null)")
cursor.execute("INSERT INTO ratings (rating_id, id_lesson, id_student, is_presence, grade) VALUES (45, 5, 4, true, 5)")
cursor.execute("INSERT INTO ratings (rating_id, id_lesson, id_student, is_presence, grade) VALUES (46, 6, 7, true, 4)")
cursor.execute("INSERT INTO ratings (rating_id, id_lesson, id_student, is_presence, grade) VALUES (47, 6, 11, true, 5)")
cursor.execute("INSERT INTO ratings (rating_id, id_lesson, id_student, is_presence, grade) VALUES (48, 6, 5, true, 4)")
cursor.execute("INSERT INTO ratings (rating_id, id_lesson, id_student, is_presence, grade) VALUES (49, 6, 12, false, null)")
cursor.execute("INSERT INTO ratings (rating_id, id_lesson, id_student, is_presence, grade) VALUES (50, 6, 3, true, 4)")
cursor.execute("INSERT INTO ratings (rating_id, id_lesson, id_student, is_presence, grade) VALUES (51, 6, 13, false, null)")
cursor.execute("INSERT INTO ratings (rating_id, id_lesson, id_student, is_presence, grade) VALUES (52, 6, 10, true, 5)")
cursor.execute("INSERT INTO ratings (rating_id, id_lesson, id_student, is_presence, grade) VALUES (53, 6, 6, true, 4)")
cursor.execute("INSERT INTO ratings (rating_id, id_lesson, id_student, is_presence, grade) VALUES (54, 6, 4, true, 4)")
cursor.execute("INSERT INTO ratings (rating_id, id_lesson, id_student, is_presence, grade) VALUES (55, 7, 7, true, null)")
cursor.execute("INSERT INTO ratings (rating_id, id_lesson, id_student, is_presence, grade) VALUES (56, 7, 11, true, null)")
cursor.execute("INSERT INTO ratings (rating_id, id_lesson, id_student, is_presence, grade) VALUES (57, 7, 5, true, null)")
cursor.execute("INSERT INTO ratings (rating_id, id_lesson, id_student, is_presence, grade) VALUES (58, 7, 12, true, null)")
cursor.execute("INSERT INTO ratings (rating_id, id_lesson, id_student, is_presence, grade) VALUES (59, 7, 3, true, null)")
cursor.execute("INSERT INTO ratings (rating_id, id_lesson, id_student, is_presence, grade) VALUES (60, 7, 13, true, null)")
cursor.execute("INSERT INTO ratings (rating_id, id_lesson, id_student, is_presence, grade) VALUES (61, 7, 10, false, null)")
cursor.execute("INSERT INTO ratings (rating_id, id_lesson, id_student, is_presence, grade) VALUES (62, 7, 6, true, null)")
cursor.execute("INSERT INTO ratings (rating_id, id_lesson, id_student, is_presence, grade) VALUES (63, 7, 4, false, null)")
cursor.execute("INSERT INTO ratings (rating_id, id_lesson, id_student, is_presence, grade) VALUES (64, 8, 7, false, null)")
cursor.execute("INSERT INTO ratings (rating_id, id_lesson, id_student, is_presence, grade) VALUES (65, 8, 11, true, null)")
cursor.execute("INSERT INTO ratings (rating_id, id_lesson, id_student, is_presence, grade) VALUES (66, 8, 5, true, null)")
cursor.execute("INSERT INTO ratings (rating_id, id_lesson, id_student, is_presence, grade) VALUES (67, 8, 12, true, null)")
cursor.execute("INSERT INTO ratings (rating_id, id_lesson, id_student, is_presence, grade) VALUES (68, 8, 3, false, null)")
cursor.execute("INSERT INTO ratings (rating_id, id_lesson, id_student, is_presence, grade) VALUES (69, 8, 13, true, null)")
cursor.execute("INSERT INTO ratings (rating_id, id_lesson, id_student, is_presence, grade) VALUES (70, 8, 10, true, null)")
cursor.execute("INSERT INTO ratings (rating_id, id_lesson, id_student, is_presence, grade) VALUES (71, 8, 6, true, null)")
cursor.execute("INSERT INTO ratings (rating_id, id_lesson, id_student, is_presence, grade) VALUES (72, 8, 4, true, null)")
cursor.execute("INSERT INTO ratings (rating_id, id_lesson, id_student, is_presence, grade) VALUES (73, 9, 7, true, null)")
cursor.execute("INSERT INTO ratings (rating_id, id_lesson, id_student, is_presence, grade) VALUES (74, 9, 11, true, null)")
cursor.execute("INSERT INTO ratings (rating_id, id_lesson, id_student, is_presence, grade) VALUES (75, 9, 5, true, null)")
cursor.execute("INSERT INTO ratings (rating_id, id_lesson, id_student, is_presence, grade) VALUES (76, 9, 12, false, null)")
cursor.execute("INSERT INTO ratings (rating_id, id_lesson, id_student, is_presence, grade) VALUES (77, 9, 3, true, null)")
cursor.execute("INSERT INTO ratings (rating_id, id_lesson, id_student, is_presence, grade) VALUES (78, 9, 13, true, null)")
cursor.execute("INSERT INTO ratings (rating_id, id_lesson, id_student, is_presence, grade) VALUES (79, 9, 10, true, null)")
cursor.execute("INSERT INTO ratings (rating_id, id_lesson, id_student, is_presence, grade) VALUES (80, 9, 6, false, null)")
cursor.execute("INSERT INTO ratings (rating_id, id_lesson, id_student, is_presence, grade) VALUES (81, 9, 4, true, null)")
cursor.execute("INSERT INTO ratings (rating_id, id_lesson, id_student, is_presence, grade) VALUES (82, 10, 7, true, null)")
cursor.execute("INSERT INTO ratings (rating_id, id_lesson, id_student, is_presence, grade) VALUES (83, 10, 11, true, null)")
cursor.execute("INSERT INTO ratings (rating_id, id_lesson, id_student, is_presence, grade) VALUES (84, 10, 5, false, null)")
cursor.execute("INSERT INTO ratings (rating_id, id_lesson, id_student, is_presence, grade) VALUES (85, 10, 12, true, null)")
cursor.execute("INSERT INTO ratings (rating_id, id_lesson, id_student, is_presence, grade) VALUES (86, 10, 3, true, null)")
cursor.execute("INSERT INTO ratings (rating_id, id_lesson, id_student, is_presence, grade) VALUES (87, 10, 13, true, null)")
cursor.execute("INSERT INTO ratings (rating_id, id_lesson, id_student, is_presence, grade) VALUES (88, 10, 10, true, null)")
cursor.execute("INSERT INTO ratings (rating_id, id_lesson, id_student, is_presence, grade) VALUES (89, 10, 6, true, null)")
cursor.execute("INSERT INTO ratings (rating_id, id_lesson, id_student, is_presence, grade) VALUES (90, 10, 4, true, null)")
cursor.execute("INSERT INTO ratings (rating_id, id_lesson, id_student, is_presence, grade) VALUES (91, 11, 7, true, 3)")
cursor.execute("INSERT INTO ratings (rating_id, id_lesson, id_student, is_presence, grade) VALUES (92, 11, 11, true, 3)")
cursor.execute("INSERT INTO ratings (rating_id, id_lesson, id_student, is_presence, grade) VALUES (93, 11, 5, true, 4)")
cursor.execute("INSERT INTO ratings (rating_id, id_lesson, id_student, is_presence, grade) VALUES (94, 11, 12, true, 4)")
cursor.execute("INSERT INTO ratings (rating_id, id_lesson, id_student, is_presence, grade) VALUES (95, 11, 3, true, 4)")
cursor.execute("INSERT INTO ratings (rating_id, id_lesson, id_student, is_presence, grade) VALUES (96, 11, 13, true, 3)")
cursor.execute("INSERT INTO ratings (rating_id, id_lesson, id_student, is_presence, grade) VALUES (97, 11, 10, true, 4)")
cursor.execute("INSERT INTO ratings (rating_id, id_lesson, id_student, is_presence, grade) VALUES (98, 11, 6, true, 3)")
cursor.execute("INSERT INTO ratings (rating_id, id_lesson, id_student, is_presence, grade) VALUES (99, 11, 4, true, 4)")
cursor.execute("INSERT INTO ratings (rating_id, id_lesson, id_student, is_presence, grade) VALUES (100, 12, 7, false, null)")
cursor.execute("INSERT INTO ratings (rating_id, id_lesson, id_student, is_presence, grade) VALUES (101, 12, 11, true, 5)")
cursor.execute("INSERT INTO ratings (rating_id, id_lesson, id_student, is_presence, grade) VALUES (102, 12, 5, false, null)")
cursor.execute("INSERT INTO ratings (rating_id, id_lesson, id_student, is_presence, grade) VALUES (103, 12, 12, true, 4)")
cursor.execute("INSERT INTO ratings (rating_id, id_lesson, id_student, is_presence, grade) VALUES (104, 12, 3, true, 5)")
cursor.execute("INSERT INTO ratings (rating_id, id_lesson, id_student, is_presence, grade) VALUES (105, 12, 13, true, 4)")
cursor.execute("INSERT INTO ratings (rating_id, id_lesson, id_student, is_presence, grade) VALUES (106, 12, 10, true, 4)")
cursor.execute("INSERT INTO ratings (rating_id, id_lesson, id_student, is_presence, grade) VALUES (107, 12, 6, true, 5)")
cursor.execute("INSERT INTO ratings (rating_id, id_lesson, id_student, is_presence, grade) VALUES (108, 12, 4, true, 5)")
conn.commit()   
print("Дані до таблиці 'ratings' додано") 
# =================================================================
cursor.close() 
conn.close() # закриваємо підключення

app=FastAPI()  
   
