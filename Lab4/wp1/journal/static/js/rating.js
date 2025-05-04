// ---------------------------------------------------
// Інформація про рейтинг студентів на занятті
const getRating = async (idLesson) => {

  try {
    // надсилаємо запит 
    const response = await fetch(`/api/rating${idLesson ? "?idLesson=" + idLesson : ""}`, {
      method: "GET"
    });

    if (response.ok) {
      const rating = await response.json();
      document.getElementById("tbodyRating").innerHTML = "";
      // Малюємо рядки таблиці
      rating.forEach((r) => 
        document.getElementById("tbodyRating").append(row(r))
      );

      formLesson.subject.disabled = true;
      formLesson.journal.disabled = true;
      formLesson.date_lesson.disabled = true;
      formLesson.btnFindLesson.hidden = true;
      formLesson.btnNewLesson.hidden = true;

      document.getElementById("idDivRating").hidden = false;
      formRating.btnSave.disabled = true;
      formRating.btnDelete.hidden = false;     

      // Помилки 
    } else {
      showToast("Помилка!", `Помилка запиту даних рейтингу, статус: ${response.status}`, 2);        
      console.log("getRating:", response);
    }

  }
  catch (error) {
    console.log("getRating:", error);
    showToast("Помилка!", `Помилка запиту даних рейтингу: ${error}`, 2);      
  }
}

// ---------------------------------------------------
// Додавання рейтингів для заняття з idLesson
const addRating = async (idLesson) => {

  try {
    // рейтинг студентів на занятті
    const rating = [];
    // Вибираємо всі рядки таблиці рейтингу
    document.getElementById("tbodyRating").querySelectorAll("tr")
    .forEach((tr) => {
        const grade = tr.querySelector("input").value;
        rating.push({
          "idLesson": idLesson,
          "idStudent": tr.getAttribute("id-student"),
          "isPresence": tr.querySelector("select").value === "true",
          "grade": grade != "" ? parseInt(grade) : null
        })
    })   

    // надсилаємо запит 
    const response = await fetch(`/api/rating`, {
      method: "POST",
      headers: { "Accept": "application/json", "Content-Type": "application/json" },  
      // body - масив об'єктів класу Rating     
      body: JSON.stringify(rating)       
    });

    if (response.ok) {
      showToast("Повідомлення", `Нове заняття успішно створено.<br>Зміни записані до БД.`, 0);           
      // Перезапитуємо і перемальовуємо дані
      await getRating(idLesson);

      // Помилки 
    } else {   
      console.log("addRating:", response);
      showToast("Помилка!", `Помилка додавання даних рейтингу, статус: ${response.status}`, 2);  
    }
  }
  catch (error) {
    console.log("addRating:", error);
    showToast("Помилка!", `Помилка додавання даних рейтингу: ${error}`, 2);  
  }
}

// ---------------------------------------------------
// Коригування рейтингів для заняття з idLesson
const editRating = async (idLesson) => {

  try {
    // рейтинг студентів на занятті
    const rating = [];
    // Вибираємо всі рядки таблиці рейтингу
    document.getElementById("tbodyRating").querySelectorAll("tr")
    .forEach((tr) => {
        const grade = tr.querySelector("input").value;
        rating.push({
          // ідентифікатор рядку рейтинга
          "id": tr.getAttribute("data-rowid"),
          "idLesson": idLesson,
          "idStudent": tr.getAttribute("id-student"),
          "isPresence": tr.querySelector("select").value === "true",
          "grade": grade != "" ? parseInt(grade) : null
        })
    })   

    // надсилаємо запит 
    const response = await fetch(`/api/rating`, {
      method: "PUT",
      headers: { "Accept": "application/json", "Content-Type": "application/json" },  
      // body - масив об'єктів класу Rating     
      body: JSON.stringify(rating)       
    });

    if (response.ok) {
      showToast("Повідомлення", `Дані успішно відкориговані.<br>Зміни записані до БД.`, 0);        
      // Перезапитуємо і перемальовуємо дані
      await getRating(idLesson);

      // Помилки 
    } else {   
      console.log("editRating:", response);
      showToast("Помилка!", `Помилка редагування даних рейтингу, статус: ${response.status}`, 2);  
    }
  }
  catch (error) {
    console.log("editRating:", error);
    showToast("Помилка!", `Помилка редагування даних рейтингу: ${error}`, 2);  
  }
}

// ---------------------------------------------------
// Видалення рейтингів для заняття
const deleteRating = async () => {

  try {
    // рейтинг студентів на занятті
    const rating = [];
    // Вибираємо всі рядки таблиці рейтингу
    document.getElementById("tbodyRating").querySelectorAll("tr")
    .forEach((tr) => {
        rating.push({
          // ідентифікатор рядку рейтинга
          "id": tr.getAttribute("data-rowid"),
        })
    })   

    // надсилаємо запит 
    const response = await fetch(`/api/rating`, {
      method: "DELETE",
      headers: { "Accept": "application/json", "Content-Type": "application/json" },  
      // body - масив об'єктів ідентифікаторів рядків рейтингу  
      body: JSON.stringify(rating)       
    });

    if (response.ok) {
      return true;

      // Помилки 
    } else {   
      console.log("deleteRating:", response);
      showToast("Помилка!", `Помилка видалення даних рейтингу, статус: ${response.status}`, 2);  
      return false;
    }
  }
  catch (error) {
    console.log("deleteRating:", error);
    showToast("Помилка!", `Помилка видалення даних рейтингу: ${error}`, 2);  
    return false;
  }
}

// ---------------------------------------------------
// Інформація про рейтинг студента по обраному предмету за обраний навчальний рік
const getRatingStudent = async (idStudent, idJournal, idSubject) => {

  try {
    // надсилаємо запит 
    const response = await fetch(`/api/rating/student/${idStudent}/${idJournal}/${idSubject}`, {
      method: "GET"
    });

    if (response.ok) {
      const rating = await response.json();
      document.getElementById("tbodyRating").innerHTML = "";
      // Малюємо рядки таблиці
      rating.forEach((r) => 
        document.getElementById("tbodyRating").append(row(r))
      );

      document.getElementById("idDivRating").hidden = false;    

      // Помилки 
    } else {
      window.alert(`Помилка запиту даних рейтингу студента, статус: ${response.status}`);        
      console.log("getRatingStudent:", response);
    }

  }
  catch (error) {
    console.log("getRatingStudent:", error);
    window.alert(`Помилка запиту даних рейтингу студента: ${error}`);      
  }
}