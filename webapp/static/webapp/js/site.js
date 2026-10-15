document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll("a[href]").forEach((link) => {
    link.addEventListener("focus", () => link.classList.add("keyboard-focus"));
    link.addEventListener("blur", () => link.classList.remove("keyboard-focus"));
  });
});
