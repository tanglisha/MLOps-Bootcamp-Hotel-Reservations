// Theme toggle functionality
function toggleTheme() {
  const body = document.body;
  const themeIcon = document.querySelector(".theme-icon");
  const themeText = document.querySelector(".theme-text");

  const currentTheme = body.getAttribute("data-theme");

  if (currentTheme === "dark") {
    body.removeAttribute("data-theme");
    themeIcon.textContent = "🌙";
    themeText.textContent = "Dark Mode";
    localStorage.setItem("theme", "light");
  } else {
    body.setAttribute("data-theme", "dark");
    themeIcon.textContent = "☀️";
    themeText.textContent = "Light Mode";
    localStorage.setItem("theme", "dark");
  }
}

// Load saved theme on page load
document.addEventListener("DOMContentLoaded", function () {
  const savedTheme = localStorage.getItem("theme");
  const themeIcon = document.querySelector(".theme-icon");
  const themeText = document.querySelector(".theme-text");

  if (savedTheme === "dark") {
    document.body.setAttribute("data-theme", "dark");
    themeIcon.textContent = "☀️";
    themeText.textContent = "Light Mode";
  }
});

// Add form submission loading state
document.querySelector("form").addEventListener("submit", function () {
  this.classList.add("loading");
});

// Add interactive feedback
document.querySelectorAll("input, select").forEach((input) => {
  input.addEventListener("focus", function () {
    this.parentElement.style.transform = "scale(1.02)";
  });

  input.addEventListener("blur", function () {
    this.parentElement.style.transform = "scale(1)";
  });
});
