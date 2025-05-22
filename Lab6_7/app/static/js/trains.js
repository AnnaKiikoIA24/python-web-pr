// ---------------------------------------------------
// Додати новий поїзд
const addTrain = async () => {

  try {
    // надсилаємо запит 
    const response = await fetch("/api/trains/new", {
      method: "POST",
      body: new FormData(idFormTrainInfo)
    });

    // Успіх
    if (response.ok) {
      const train = await response.json();
      idFormTrainInfo.id_train.value = train.id;
      idFormTrainInfo.old_period.value = idFormTrainInfo.period.value
      idDivTrainRoute.hidden = false;
      showToast("Повідомлення", `Новий поїзд успішно створений.<br>Зміни записані до БД.`, 0);      
     // Помилки створення поїзду
    } else {
      // Аналізуємо статус відповіді
      switch (response.status) {
        case 409:
          showToast("Увага!", 
            `Поїзд з номером ${idFormTrainInfo.num_train.value} в обраному періоді вже існує!`, 1);          
          break;  
        default:
          console.log("addTrain =", response);   
          showToast("Помилка", `Помилка створення нового поїзда, статус: ${response.status}`, 2);          
      }
      console.log(response);     
    }
  }
  catch(error) {
    console.log("addTrain:", error);  
    showToast("Помилка", `Помилка запиту створення нового поїзда: ${error}`, 2);    
  }
}

// ---------------------------------------------------
// Редагувати поїзд
const editTrain = async () => {

  try {
    // надсилаємо запит 
    const response = await fetch("/api/trains/edit", {
      method: "POST",
      body: new FormData(idFormTrainInfo)
    });

    // Успіх
    if (response.ok) {
      idFormTrainInfo.old_period.value = idFormTrainInfo.period.value
      showToast("Повідомлення", `Поїзд успішно відкоригований.<br>Зміни записані до БД.`, 0); 

    // Помилки редагування поїзду
    } else {
      // Аналізуємо статус відповіді
      switch (response.status) {
        case 404:
          showToast("Увага!", `Поїзд з Id = ${idFormTrainInfo.id_train.value} не існує в обраному періоді!`, 1);
          break; 
        case 409:
          showToast("Увага!", `В обраному періоді існує інший поїзд з тим же номером ${idFormTrainInfo.num_train.value}!`, 1);
          break;            
        default:
          console.log("editTrain =", response);             
          showToast("Помилка", `Помилка редагування поїзда, статус: ${response.status}`, 2);                
      }
      console.log(response);     
    }
  }
  catch(error) {
    console.log("editTrain:", error);    
    showToast("Помилка", `Помилка редагування поїзда: ${error}`, 2); 
  }
}


// ---------------------------------------------------
// Видалити поїзд
const deleteTrain = async (idTrain, idPeriod) => {

  try {
    // надсилаємо запит 
    const response = await fetch(`/api/trains/delete/${idTrain}/${idPeriod}`, {
      method: "DELETE"
    });

    // Успіх
    if (response.ok) {     

      idFormFindTrain.period.value = idFormTrains.selected_period.value;
      idFormFindTrain.num_train.value = idFormTrains.selected_num_train.value || "";
      idFormFindTrain.submit();
      showToast("Повідомлення", `Поїзд успішно видалений.<br>Зміни записані до БД.`, 0);       

    // Помилки видалення поїзду
    } else {
      // Аналізуємо статус відповіді
      switch (response.status) {
        case 404:
          showToast("Увага!", `Поїзд з Id = ${idTrain} не існує в обраному періоді!`, 2);
          break;           
        default:
          console.log("deleteTrain =", response);             
          showToast("Помилка", `Помилка видалення поїзда, статус: ${response.status}`, 2);                
      }
      console.log(response);     
    }
  }
  catch(error) {
    console.log("deleteTrain:", error);    
    showToast("Помилка", `Помилка видалення поїзда: ${error}`, 2); 
  }
}

