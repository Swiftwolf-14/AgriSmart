const roleOptions = document.querySelectorAll(".role-option");
const passwordToggles = document.querySelectorAll(".toggle-password");
const registerForm = document.getElementById("registerForm");

// Role selection
roleOptions.forEach((option) => {
  option.addEventListener("click", () => {
    roleOptions.forEach((item) => {
      item.classList.remove("selected");
    });

    option.classList.add("selected");

    const radio = option.querySelector('input[type="radio"]');

    if (radio) {
      radio.checked = true;
    }
  });
});

// Show and hide passwords
passwordToggles.forEach((button) => {
  button.addEventListener("click", () => {
    const input = document.getElementById(button.dataset.target);

    if (!input) return;

    const shouldShow = input.type === "password";

    input.type = shouldShow ? "text" : "password";

    button.setAttribute(
      "aria-label",
      shouldShow ? "Hide password" : "Show password"
    );
  });
});

// Validate passwords, then allow Django to process the form
if (registerForm) {
  registerForm.addEventListener("submit", (event) => {
    const passwordInput = document.getElementById("password");
    const confirmPasswordInput =
      document.getElementById("confirmPassword");

    if (!passwordInput || !confirmPasswordInput) {
      event.preventDefault();
      console.error("Could not find both password fields.");
      return;
    }

    if (passwordInput.value !== confirmPasswordInput.value) {
      event.preventDefault();

      alert("Your passwords do not match. Please check and try again.");

      confirmPasswordInput.focus();
    }

    // When passwords match, the form submits normally to Django.
  });
}