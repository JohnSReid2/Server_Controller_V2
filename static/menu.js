function toggleMenu(x) {
  x.classList.toggle("change");
  const dropdown = document.getElementById('navDropdown');
  if (dropdown.style.maxHeight) {
    dropdown.style.maxHeight = null;
  } else {
    dropdown.style.maxHeight = dropdown.scrollHeight + "px";
  }
}