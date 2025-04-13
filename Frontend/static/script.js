let flashcardCount = 1;
const maxFlashcards = 50;
let quizTitle = "";
let quizCategory = "";
let flashcards = []; // store all created flashcards here

document.addEventListener("DOMContentLoaded", function () {
    const loginForm = document.getElementById("loginForm");
    const signupForm = document.getElementById("signupForm");
    const forgotPasswordForm = document.getElementById("forgotPasswordForm");

    const signupLink = document.getElementById("signupLink");
    const forgotPasswordLink = document.getElementById("forgotPasswordLink");
    const backToLogin1 = document.getElementById("backToLogin1");
    const backToLogin2 = document.getElementById("backToLogin2");

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

    window.enableEdit = function (elementId) {
        var inputField = document.getElementById(elementId);
        if (inputField) {
            inputField.disabled = false;
            inputField.focus();
        }
    }

    window.saveProfile = function () {
        const username = document.getElementById('username');
        const email = document.getElementById('email');
        const password = document.getElementById('password');

        username.disabled = true;
        email.disabled = true;
        password.disabled = true;

        let data = new FormData();
        data.append("newUsername", username.value);
        data.append("newEmail", email.value);
        data.append("newPassword", password.value);

        fetch("http://127.0.0.1:5000/edit", {
            method: "POST",
            body: data
        }).then(() => console.log("Sent data"));

        console.log("Profile saved:", {
            username: username.value,
            email: email.value,
            password: password.value
        });
    }

    const profileImageInput = document.getElementById('profileImageInput');
    const profilePic = document.getElementById('profilePic');

    if (profileImageInput && profilePic) {
        profileImageInput.addEventListener('change', function (event) {
            var file = event.target.files[0];
            if (file) {
                var reader = new FileReader();
                reader.onload = function (e) {
                    profilePic.src = e.target.result;
                }
                reader.readAsDataURL(file);
            }
        });
    }

    const createQuizBtn = document.getElementById("createQuizBtn");
    const flashcardContainer = document.getElementById("flashcardContainer");
    const createBox = document.querySelector(".create-box h2");

    if (createQuizBtn && flashcardContainer && createBox) {
        createQuizBtn.addEventListener("click", function () {
            quizTitle = document.getElementById("quizTitle").value;
            quizCategory = document.getElementById("quizCategory").value;

            if (!quizTitle || !quizCategory) {
                alert("Please enter a quiz name and select a category.");
                return;
            }

            createBox.textContent = quizTitle;
            document.getElementById("quizForm").style.display = "none";
            addFlashcard();
        });

        function addFlashcard() {
            if (flashcardCount > maxFlashcards) {
                alert("You have reached the maximum number of flashcards.");
                return;
            }

            const prevNameInput = document.querySelector("#flashcardInputFront");
            const prevContentInput = document.querySelector("#flashcardInputBack");
            if (prevNameInput && prevContentInput) {
                flashcards.push({
                    name: prevNameInput.value,
                    content: prevContentInput.value
                });
            }

            flashcardContainer.innerHTML = "";

            const flashcard = document.createElement("div");
            flashcard.classList.add("flashcard");

            flashcard.innerHTML = `
                <h3>Flashcard ${flashcardCount}</h3>
                <div class="flashcard-input-container">
                    <textarea placeholder="Enter front content..." id="flashcardInputFront" rows="6"></textarea>
                </div>
                <div class="flashcard-input-container">
                    <textarea placeholder="Enter back content..." id="flashcardInputBack" rows="6"></textarea>
                </div>
                <div class="flashcard-buttons">
                    <button id="nextFlashcardBtn">Next Flashcard</button>
                    <button id="endQuizBtn">Save Quiz</button>
                    <button id="BackBtn">Exit</button>
                </div>
            `;

            flashcardContainer.appendChild(flashcard);

            document.getElementById("nextFlashcardBtn").addEventListener("click", function () {
                flashcardCount++;
                addFlashcard();
            });

            document.getElementById("endQuizBtn").addEventListener("click", function () {
                const name = document.getElementById("flashcardInputFront").value;
                const content = document.getElementById("flashcardInputBack").value;
                flashcards.push({ name, content });
                submitQuiz();
            });

            document.getElementById("BackBtn").addEventListener("click", function () {
                window.location.href = "/create";
            });
        }

        function submitQuiz() {
            const payload = {
                title: quizTitle,
                category: quizCategory,
                flashcards: flashcards
            };

            fetch("/api/quizzes", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(payload)
            }).then(res => {
                if (res.ok) {
                    window.location.href = "/library";
                } else {
                    alert("Failed to save quiz.");
                }
            });
        }
    }
});