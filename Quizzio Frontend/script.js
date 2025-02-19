document.addEventListener("DOMContentLoaded", function () {
    //V1.2
    // Form Sections
    const loginForm = document.getElementById("loginForm");
    const signupForm = document.getElementById("signupForm");
    const forgotPasswordForm = document.getElementById("forgotPasswordForm");

    // Navigation Links
    const signupLink = document.getElementById("signupLink");
    const forgotPasswordLink = document.getElementById("forgotPasswordLink");
    const backToLogin1 = document.getElementById("backToLogin1");
    const backToLogin2 = document.getElementById("backToLogin2");

    // Ensure the forms exist before adding event listeners
    if (signupLink && signupForm) {
        signupLink.addEventListener("click", function (e) {
            e.preventDefault();
            loginForm.classList.add("hidden");
            signupForm.classList.remove("hidden");
        });
    }

    if (forgotPasswordLink && forgotPasswordForm) {
        forgotPasswordLink.addEventListener("click", function (e) {
            e.preventDefault();
            loginForm.classList.add("hidden");
            forgotPasswordForm.classList.remove("hidden");
        });
    }

    if (backToLogin1 && signupForm) {
        backToLogin1.addEventListener("click", function (e) {
            e.preventDefault();
            signupForm.classList.add("hidden");
            loginForm.classList.remove("hidden");
        });
    }

    if (backToLogin2 && forgotPasswordForm) {
        backToLogin2.addEventListener("click", function (e) {
            e.preventDefault();
            forgotPasswordForm.classList.add("hidden");
            loginForm.classList.remove("hidden");
        });
    }
});