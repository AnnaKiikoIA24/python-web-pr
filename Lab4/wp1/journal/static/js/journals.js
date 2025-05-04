// ---------------------------------------------------
// Інформація про перелік журналів груп
const getJournals = async (element,  idGroup = null) => {

  try {
    // надсилаємо запит 
    const response = await fetch(`/api/journals${idGroup ? "?idGroup=" + idGroup : ""}`, {
      method: "GET"
    });

    if (response.ok) {
      const journals = await response.json();
      console.log("journals =", journals); 
      journals.forEach((journal) => {
        // Заповнити випадаючий список
        const newOption = new Option(`${journal.name} ${journal.year}/${journal.year+1}`, journal.id);
        newOption.setAttribute("id-group", journal.idGroup);
        element.options[element.options.length] = newOption;
      })
      if (!idGroup)
        element.selectedIndex = -1;
      // Помилки 
    } else {
      console.log("journals =", response);      
      window.alert(`Помилка запиту даних про перелік журналів, статус: ${response.status}`);
    }
  }
  catch (error) {
    console.log("journals:", error);
    window.alert(`Помилка запиту даних про перелік журналів: ${error}`);
  }
}