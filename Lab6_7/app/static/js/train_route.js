// ---------------------------------------------------
let modal;
const openModalRouteRow = (id, idTrain) => {
  fetch(`/train_route_row_info?id_row=${id}&id_train=${idTrain}`)
    .then(response => response.text())
    .then(html => {
      document.getElementById("trainRouteModalContent").innerHTML = html;
      form_modal.btnSaveInfoRow.disabled = true;
      modal = new bootstrap.Modal(document.getElementById("trainRouteModal"));
      modal.show();
    });
}

// ---------------------------------------------------
// Додати новий рядок до розкладу
const addRow = async () => {

  try {
    // надсилаємо запит 
    const response = await fetch("/api/train_route/new", {
      method: "POST",
      body: new FormData(idFormModal)
    });

    // Успіх
    if (response.ok) {
      showToast("Повідомлення", `Новий рядок розкладу успішно створений.<br>Зміни записані до БД.`, 0);  
      modal.hide();  
      location.href = `../train_info?id_train=${idFormTrainInfo.id_train.value}&period=${idFormTrainInfo.old_period.value}`

     // Помилки створення рядку розкладу
    } else {
      // Аналізуємо статус відповіді
      switch (response.status) { 
        default:
          console.log("addRow =", response);   
          showToast("Помилка", `Помилка створення нового рядку розкладу, статус: ${response.status}`, 2);          
      }
      console.log(response);     
    }
  }
  catch(error) {
    console.log("addRow:", error);  
    showToast("Помилка", `Помилка запиту створення нового рядку розкладу: ${error}`, 2);    
  }
}

// ---------------------------------------------------
// Редагувати існуючий рядок розкладу
const editRow = async () => {

  try {
    // надсилаємо запит 
    const response = await fetch("/api/train_route/edit", {
      method: "POST",
      body: new FormData(idFormModal)
    });

    // Успіх
    if (response.ok) {
      showToast("Повідомлення", `Рядок розкладу успішно відкоригований.<br>Зміни записані до БД.`, 0); 
      modal.hide();  
      location.href = `../train_info?id_train=${idFormTrainInfo.id_train.value}&period=${idFormTrainInfo.old_period.value}`

    // Помилки редагування поїзду
    } else {
      // Аналізуємо статус відповіді
      switch (response.status) {
        case 404:
          showToast("Увага!", `Рядок у розкладі з Id = ${idFormTrainInfo.id_train.value} не знайдений у БД!`, 1);
          break; 
        default:
          console.log("editRow =", response);             
          showToast("Помилка", `Помилка редагування розкладу, статус: ${response.status}`, 2);                
      }
      console.log(response);     
    }
  }
  catch(error) {
    console.log("editRow:", error);    
    showToast("Помилка", `Помилка редагування розкладу: ${error}`, 2); 
  }
}


// ---------------------------------------------------
// Видалити рядок розкладу
const deleteRow = async (idRow) => {

  try {
    // надсилаємо запит 
    const response = await fetch(`/api/train_route/delete/${idRow}`, {
      method: "DELETE"
    });

    // Успіх
    if (response.ok) {     

      showToast("Повідомлення", `Рядок з розкладу успішно видалений.<br>Зміни записані до БД.`, 0);       
      location.href = `../train_info?id_train=${idFormTrainInfo.id_train.value}&period=${idFormTrainInfo.old_period.value}`

    // Помилки видалення рядку у розкладі
    } else {
      // Аналізуємо статус відповіді
      switch (response.status) {
        case 404:
          showToast("Увага!", `Рядок у розкладі з Id = ${idRow} не існує в БД!`, 2);
          break;           
        default:
          console.log("deleteRow =", response);             
          showToast("Помилка", `Помилка видалення рядку у розкладі, статус: ${response.status}`, 2);                
      }
      console.log(response);     
    }
  }
  catch(error) {
    console.log("deleteRow:", error);    
    showToast("Помилка", `Помилка видалення рядку у розкладі: ${error}`, 2); 
  }
}

