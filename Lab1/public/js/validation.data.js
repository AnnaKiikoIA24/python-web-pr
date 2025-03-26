// -------------------------------------------------------
function dateFormat(date) {
  console.log("date=",`${date.getFullYear()}-${date.getMonth() + 1}-${date.getDate()}`);
  let day = date.getDate();
  let month = date.getMonth() + 1;
  let year = date.getFullYear();

  if (day < 10) day = "0" + day;
  if (month < 10) month = "0" + month;
  return `${year}-${month}-${day}`;
}

// -------------------------------------------------------
// Перевірка на валідність елемента
function checkValidation(event) {
  // let aa = $("input[name='flexRadio']:checked+label").text();
  const node = event.currentTarget;
  console.log(event.currentTarget.value);

  // Встановлення стилів css
  // Якщо значення елементу invalid
  if (!node.checkValidity()) {
    node.classList.remove('is-valid');
    node.classList.add('is-invalid');
  }
  else {
    node.classList.remove('is-invalid');
    node.classList.add('is-valid');
  }
}

// -------------------------------------------------------
// default-cтилі елементу форми 
function resetClassList(node) {
  if (node.classList.contains('is-valid') || node.classList.contains('is-invalid')) {
    node.classList.remove('is-valid');
    node.classList.remove('is-invalid');
  }
}