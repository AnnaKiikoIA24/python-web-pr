// ---------------------------------------------------
// Інформація про список груп студентів
const getGroups = async (element) => {

  try {
    // надсилаємо запит 
    const response = await fetch(`/api/groups`, {
      method: "GET"
    });

    if (response.ok) {
      const groups = await response.json();
      console.log("groups =", groups);            
      groups.forEach((gr) => {
        // Заповнити випадаючий список
        const newOption = new Option(gr.name, gr.id);
        element.options[element.options.length] = newOption;
      })
      // Помилки 
    } else {
      console.log("groups =", response);      
      window.alert(`Помилка запиту даних про перелік груп, статус: ${response.status}`);
    }
  }
  catch (error) {
    console.log("groups:", error);
    window.alert(`Помилка запиту даних про перелік груп: ${error}`);
  }
}