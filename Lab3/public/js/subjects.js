// ---------------------------------------------------
// Інформація про список предметів
const getSubjects = async (element) => {

    try {
      // надсилаємо запит 
      const response = await fetch(`/api/subjects`, {
        method: "GET"
      });
  
      if (response.ok) {
        const subjects = await response.json();
        console.log("subjects =", subjects);
        subjects.forEach((sub) => {
          // Заповнити випадаючий список
          const newOption = new Option(`${sub.nameFull} (${sub.nameShort})`, sub.id);
          element.options[element.options.length] = newOption;
        })
        element.selectedIndex = -1;        
        // Помилки 
      } else {
        console.log("subjects =", response);        
        window.alert(`Помилка запиту даних про перелік предметів, статус: ${response.status}`);
      }
    }
    catch (error) {
      console.log("subjects:", error);
      window.alert(`Помилка запиту даних про перелік предметів: ${error}`);
    }
  }