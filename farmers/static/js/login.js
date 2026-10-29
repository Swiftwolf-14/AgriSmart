
const loginForm = document.getElementById("loginForm");
const username = document.getElementById("username");
const password = document.getElementById("password");

const togglePassword = document.getElementById("togglePassword");
const formMessage = document.getElementById("formMessage");

const usernameError = document.getElementById("usernameError");
const passwordError = document.getElementById("passwordError");

// SHOW OR HIDE PASSWORD
togglePassword.addEventListener("click", function () {
    const isHidden = password.type === "password";

    password.type = isHidden ? "text" : "password";

    togglePassword.innerHTML = isHidden
        ? '<i class="fa-regular fa-eye-slash"></i>'
        : '<i class="fa-regular fa-eye"></i>';

    togglePassword.setAttribute(
        "aria-label",
        isHidden ? "Hide password" : "Show password"
    );
});

// CLEAR ERRORS WHEN USER TYPES
username.addEventListener("input", function () {
    usernameError.textContent = "";
    formMessage.textContent = "";
});

password.addEventListener("input", function () {
    passwordError.textContent = "";
    formMessage.textContent = "";
});

// LOGIN FORM VALIDATION
loginForm.addEventListener("submit", function (event) {
    event.preventDefault();

    usernameError.textContent = "";
    passwordError.textContent = "";
    formMessage.textContent = "";

    let valid = true;

    if (username.value.trim() === "") {
        usernameError.textContent =
            "Please enter your username or email.";

        valid = false;
    }

    if (password.value.trim() === "") {
        passwordError.textContent =
            "Please enter your password.";

        valid = false;
    }

    if (!valid) {
        return;
    }

    // Submit the form to Django
    HTMLFormElement.prototype.submit.call(loginForm);
});

// FORGOT PASSWORD
document.getElementById("forgotPassword")
    .addEventListener("click", function (event) {
        event.preventDefault();

        formMessage.style.color = "#087f46";
        formMessage.textContent =
            "Password recovery will be available when configured.";
    });

// GOOGLE SIGN-IN PLACEHOLDER
document.getElementById("googleLogin")
    .addEventListener("click", function () {
        formMessage.style.color = "#66778a";
        formMessage.textContent =
            "Google sign-in requires Google OAuth configuration.";
    });
