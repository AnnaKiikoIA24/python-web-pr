// ---------------------------------------------------
// Перевірка логіну/паролю
const checkUser = async () => {

  try {
    // надсилаємо запит 
    const response = await fetch("/api/users/hello", {
      method: "POST",
      body: new FormData(idFormSignIn)
    });

    // Верифікація успішна
    if (response.ok) {
      const user = await response.json();
      window.location.href = `../${!user.role ? "trains" : "routes"}.html`;
    // Помилки верифікації
    } else {
      // Аналізуємо статус відповіді
      switch (response.status) {
        case 401:
          document.getElementById("idError").textContent = "Неправильний пароль";
          break;
        case 404:
          document.getElementById("idError").textContent = `Користувач ${formSignIn.login.value} не знайдений!`;
          break;  
        default:
          document.getElementById("idError").textContent = `Помилка пошуку даних про користувача, статус: ${response.status}`; 
          console.log("checkUser =", response);                  
      }
      document.getElementById("idError").style.display = "block";    
    }
  }
  catch(error) {
    console.log("checkUser:", error);    
    document.getElementById("idError").textContent = error;  
    document.getElementById("idError").style.display = "block";  
  }
}

// ---------------------------------------------------
// Додати нового користувача
const addUser = async () => {

  try {
    // надсилаємо запит 
    const response = await fetch("/api/users/new", {
      method: "POST",
      body: new FormData(idFormRegistr)
    });

    // Верифікація успішна
    if (response.ok) {
      const user = await response.json();
      window.location.href = `../${!user.role ? "trains" : "routes"}.html`;
    // Помилки верифікації
    } else {
      // Аналізуємо статус відповіді
      switch (response.status) {
        case 409:
          window.alert(`Користувач ${idFormRegistr.login.value} вже існує!`);
          break;  
        default:
          console.log("addUser =", response);             
          window.alert(`Помилка створення користувача, статус: ${response.status}`);                
      }
      console.log(response);     
    }
  }
  catch(error) {
    console.log("addUser:", error);    
    window.alert(`Помилка створення користувача: ${error}`); 
  }
}

// ---------------------------------------------------
// Редагувати користувача
const editUser = async (userId) => {

  try {
    // надсилаємо запит 
    const response = await fetch("/api/users/edit", {
      method: "POST",
      body: new FormData(idFormRegistr)
    });

    // Верифікація успішна
    if (response.ok) {
      const user = await response.json();
      window.location.href = `../${!user.role ? "trains" : "routes"}.html`;
    // Помилки верифікації
    } else {
      // Аналізуємо статус відповіді
      switch (response.status) {
        case 404:
          window.alert(`Користувач з Id = ${userId} не існує!`);
          break; 
        case 409:
          window.alert(`Інший користувач з логіном ${idFormRegistr.login.value} вже існує в БД!`);
          break;            
        default:
          console.log("editUser =", response);             
          window.alert(`Помилка редагування користувача, статус: ${response.status}`);                
      }
      console.log(response);     
    }
  }
  catch(error) {
    console.log("editUser:", error);    
    window.alert(`Помилка редагування користувача: ${error}`); 
  }
}

// ---------------------------------------------------
// Повертає cookie за визначеним name,
// або undefined, якщо нічого не знайдено
const getCookie = (name) => {
  let matches = document.cookie.match(new RegExp(
    "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
  ));
  return matches ? decodeURIComponent(matches[1]) : undefined;
}

// ---------------------------------------------------
// Інформація про користувача за заданим id
const getUser = async (id, callbackFn) => {

  try {
    // надсилаємо запит 
    const response = await fetch(`/api/users/${id}`, {
      method: "GET"
    });

    if (response.ok) {
      const user = await response.json();
      if (callbackFn)
        callbackFn(user);
    // Помилки 
    } else {
      // Аналізуємо статус відповіді
      switch (response.status) {
        case 404:
          window.alert(`Користувач не знайдений!`);
          break;  
        default:
          console.log("getUser =", response);             
          window.alert(`Помилка запиту даних про користувача, статус: ${response.status}`);              
      }
      console.log(response);     
    }
  }
  catch(error) {
    console.log("getUser:", error);    
    window.alert(`Помилка запиту даних про користувача: ${error}`);  
  }
}

// ---------------------------------------------------
// Відобразити інформацію про користувача в панелі навігації
const navUserInfo = (user) => {
  document.getElementById("idUserName").innerHTML = 
    `Користувач: <small><strong>${user.firstName} ${user.lastName}</strong> (${user.role ? "Пасажир" : "Диспетчер"})</small>`;
  document.getElementById("idUserInfo").textContent = `${user.login}`;  
}
// ---------------------------------------------------
// Вихід з облікового запису
const signOut = () => {
  const userId = getCookie("user_id");
  if (userId) {
    document.cookie = `user_id=; Max-Age=-1; Path=/; `;
    document.cookie = `group_id=; Max-Age=-1; Path=/; `;    
  }
  window.location.href = "../index.html";
}

