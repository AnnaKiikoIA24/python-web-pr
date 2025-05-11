/* global bootstrap: false */
// ---------------------------------------------------
// Пошук заняття за заданими параметрами
const findLesson = async () => {

  try {
    // надсилаємо запит 
    const response = await fetch(`/api/lessons/find`, {
      method: "POST",
      headers: { 
        "Accept": "application/json", 
        "Content-Type": "application/json",
        'X-CSRFToken': getCookie('csrftoken') },  
      // body - об'єкт класу Lesson     
      body: JSON.stringify({  
        "idJournal": formLesson.journal.value, 
        "idTeacher": getCookie("user_id"),
        "idSubject":  formLesson.subject.value, 
        "dateLesson": formLesson.date_lesson.value
      }),
      credentials: 'include'  // важливо, щоб куки передавались!       
    });

    // заняття знайдено
    if (response.ok) {
      const lesson = await response.json();
      console.log("lesson=", lesson);
      // У компоненти форм записуємо значення id та теми заняття
      formLesson.idLesson.value = lesson.id;  
      formRating.theme.value = lesson.theme;
      formRating.max_grade.value = lesson.maxGrade;

      // Отримуємо та відображаємо рейтинг студентів за заданим lesson.id
      await getRating(lesson.id);        
      // Помилки 
    } else {
      // Аналізуємо статус відповіді
      if (response.status === 404) {
        showToast("Увага!", "Заняття не знайдено.", 1);
        // відображаємо кнопку "Нове заняття"
        formLesson.btnNewLesson.hidden = false;               
      } else {   
        showToast("Помилка!", `Помилка запиту даних про заняття, статус: ${response.status}`, 2);        
        console.log("findLesson:", response);
      }
    }

  }
  catch (error) {
    console.log("findLesson:", error);
    showToast("Помилка!", error, 2);         
  }
}

// ---------------------------------------------------
// Додавання нового заняття
const addLesson = async () => {

  try {
    // надсилаємо запит 
    const response = await fetch(`/api/lessons/new`, {
      method: "POST",
      headers: { 
        "Accept": "application/json", 
        "Content-Type": "application/json",
        'X-CSRFToken': getCookie('csrftoken') },
      // body - об'єкт класу Lesson     
      body: JSON.stringify({  
        "idJournal": formLesson.journal.value, 
        "idTeacher": getCookie("user_id"),
        "idSubject":  formLesson.subject.value, 
        "dateLesson": formLesson.date_lesson.value,
        "theme": formRating.theme.value,
        "maxGrade": formRating.max_grade.value        
      })       
    });

    if (response.ok) {
      const lesson = await response.json();
      formLesson.idLesson.value = lesson.id;
      console.log("added lesson=", lesson);    

      // Додаємо рейтинг студентів за заданим lesson.id
      await addRating(lesson.id);

      // Помилки 
    } else {
      showToast("Помилка!", `Помилка створення нового заняття, статус: ${response.status}`, 2);         
      console.log("addLesson:", response);
    }

  }
  catch (error) {
    console.log("addLesson:", error);
    showToast("Помилка!", `Помилка запиту створення нового заняття: ${error}`, 2);        
  }
}

// ---------------------------------------------------
// Коригування заняття
const editLesson = async () => {

  try {
    // надсилаємо запит 
    const response = await fetch(`/api/lessons/edit`, {
      method: "PUT",
      headers: { 
        "Accept": "application/json", 
        "Content-Type": "application/json",
        'X-CSRFToken': getCookie('csrftoken') },
      // body - об'єкт класу Lesson     
      body: JSON.stringify({  
        "id": formLesson.idLesson.value,  
        "idJournal": formLesson.journal.value, 
        "idTeacher": getCookie("user_id"),
        "idSubject":  formLesson.subject.value, 
        "dateLesson": formLesson.date_lesson.value,
        "theme": formRating.theme.value,        
        "maxGrade": formRating.max_grade.value
      })       
    });

    if (response.ok) {
      const lesson = await response.json();
      console.log("edited lesson=", lesson);    

      // Коригуємо рейтинг студентів за заданим lesson.id
      await editRating(lesson.id);

      // Помилки 
    } else {
      showToast("Помилка!", `Помилка коригування заняття, статус: ${response.status}`, 2);             
      console.log("editLesson:", response);
    }

  }
  catch (error) {
    console.log("editLesson:", error);
    showToast("Помилка!", `Помилка запиту на коригування заняття: ${error}`, 2);        
  }
}

// ---------------------------------------------------
// Видалення заняття
const deleteLesson = async () => {
  // Спочатку видаляємо рейтинг студентів за заданим formLesson.idLesson.value
  const resultDelRating = await deleteRating(formLesson.idLesson.value);
  if (!resultDelRating)
    return;

  try {
    // надсилаємо запит на видалення заняття
    const response = await fetch(`/api/lessons/delete/${formLesson.idLesson.value}`, {
      headers: { 
        "Accept": "application/json", 
        "Content-Type": "application/json",
        'X-CSRFToken': getCookie('csrftoken') },      
      method: "DELETE"   
    });

    if (response.ok) {
      console.log("Заняття з id=", formLesson.idLesson.value, "видалено");    
      showToast("Повідомлення", `Заняття успішно видалено. <br>Зміни записані до БД.`, 0);        
      formLesson.subject.disabled = false;
      formLesson.subject.selectedIndex = -1;
      formLesson.journal.disabled = false;
      formLesson.journal.selectedIndex = -1;      
      formLesson.date_lesson.disabled = false;
      formLesson.btnFindLesson.hidden = false;
      formLesson.btnFindLesson.disabled = true;
      formLesson.btnNewLesson.hidden = true;
      formLesson.idLesson.value = "";

      document.getElementById("idDivRating").hidden = true;
      // Помилки 
    } else {
      showToast("Помилка!", `Помилка видалення заняття, статус: ${response.status}`, 2);        
      console.log("deleteLesson: ", response);
    }

  }
  catch (error) {
    console.log("deleteLesson:", error);
    showToast("Помилка!", `Помилка запиту на видалення заняття: ${error}`, 2);  
  }
}
