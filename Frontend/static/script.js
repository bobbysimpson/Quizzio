// ⚡ script.js - Full Working Version
let flashcardCount = 1;
const maxFlashcards = 50;
let quizTitle = "";
let quizCategory = "";
let flashcards = [];

document.addEventListener("DOMContentLoaded", function () {
  // ----- Auth Forms -----
  const loginForm = document.getElementById("loginForm");
  const signupForm = document.getElementById("signupForm");
  const forgotPasswordForm = document.getElementById("forgotPasswordForm");
  const signupLink = document.getElementById("signupLink");
  const forgotPasswordLink = document.getElementById("forgotPasswordLink");
  const backToLogin1 = document.getElementById("backToLogin1");
  const backToLogin2 = document.getElementById("backToLogin2");


  // ----- Profile Editing -----
  window.enableEdit = function (id) {
    const input = document.getElementById(id);
    if (input) { input.disabled = false; input.focus(); }
  };

  window.saveProfile = function () {
    const username = document.getElementById("username");
    const email = document.getElementById("email");
    const password = document.getElementById("password");

    [username, email, password].forEach(el => el.disabled = true);

    const data = new FormData();
    data.append("newUsername", username.value);
    data.append("newEmail", email.value);
    data.append("newPassword", password.value);

    fetch("http://127.0.0.1:5000/edit", { method: "POST", body: data })
      .then(() => console.log("Profile update sent."));
  };

  // ----- Profile Picture Upload -----
  const profileImageInput = document.getElementById("profileImageInput");
  const profilePic = document.getElementById("profilePic");
  if (profileImageInput && profilePic) {
    profileImageInput.addEventListener("change", function (e) {
      const file = e.target.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = e => profilePic.src = e.target.result;
        reader.readAsDataURL(file);
      }
    });
  }

  // ----- Flashcard Creation -----
  const createQuizBtn = document.getElementById("createQuizBtn");
  const flashcardContainer = document.getElementById("flashcardContainer");
  const createBox = document.querySelector(".create-box h2");

  if (createQuizBtn && flashcardContainer && createBox) {
    createQuizBtn.addEventListener("click", () => {
      quizTitle = document.getElementById("quizTitle").value;
      quizCategory = document.getElementById("quizCategory").value;
      if (!quizTitle || !quizCategory) return alert("Please enter a quiz name and select a category.");
      createBox.textContent = quizTitle;
      document.getElementById("quizForm").style.display = "none";
      addFlashcard();
    });

    function addFlashcard() {
      if (flashcardCount > maxFlashcards) return alert("You have reached the maximum number of flashcards.");
      const prevFront = document.getElementById("flashcardInputFront");
      const prevBack = document.getElementById("flashcardInputBack");
      if (prevFront && prevBack) flashcards.push({ name: prevFront.value, content: prevBack.value });

      flashcardContainer.innerHTML = `
        <div class="flashcard">
          <h3>Flashcard ${flashcardCount}</h3>
          <div class="flashcard-input-container"><textarea id="flashcardInputFront" placeholder="Enter front content..." rows="6"></textarea></div>
          <div class="flashcard-input-container"><textarea id="flashcardInputBack" placeholder="Enter back content..." rows="6"></textarea></div>
          <div class="flashcard-buttons">
            <button id="nextFlashcardBtn">Next Flashcard</button>
            <button id="endQuizBtn">Save Quiz</button>
            <button id="BackBtn">Exit</button>
          </div>
        </div>
      `;

      document.getElementById("nextFlashcardBtn").addEventListener("click", () => { flashcardCount++; addFlashcard(); });
      document.getElementById("endQuizBtn").addEventListener("click", () => {
        const name = document.getElementById("flashcardInputFront").value;
        const content = document.getElementById("flashcardInputBack").value;
        flashcards.push({ name, content });
        submitQuiz();
      });
      document.getElementById("BackBtn").addEventListener("click", () => window.location.href = "/create");
    }

    function submitQuiz() {
      fetch("/api/quizzes", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title: quizTitle, category: quizCategory, flashcards }),
      }).then(res => {
        if (res.ok) window.location.href = "/library";
        else alert("Failed to save quiz.");
      });
    }
  }

  // ----- Event Delegation for Bookmark & Delete -----
  document.body.addEventListener("click", async function (e) {
    const bookmarkBtn = e.target.closest(".bookmark-button");
    const deleteBtn = e.target.closest(".delete-button");

    if (deleteBtn) {
      const quizId = deleteBtn.getAttribute("data-quiz-id");
      if (!confirm("Are you sure you want to delete this quiz? This action cannot be undone.")) return;
      try {
        const res = await fetch(`/api/sets/${quizId}`, { method: "DELETE", headers: { "Content-Type": "application/json" } });
        const result = await res.json();
        if (res.ok) deleteBtn.closest(".card")?.remove();
        else alert(result.error || "Failed to delete quiz");
      } catch (err) {
        console.error("Delete error:", err);
        alert("An error occurred while deleting the quiz.");
      }
    }

    if (bookmarkBtn) {
      const setId = bookmarkBtn.getAttribute("data-set-id");
      const isBookmarked = bookmarkBtn.getAttribute("data-bookmarked") === "true";
      const icon = bookmarkBtn.querySelector(".bookmark-icon");
      const pageType = document.body.getAttribute("data-page");

      try {
        let res;
        if (isBookmarked) {
          res = await fetch(`/api/unbookmark_set/${setId}`, { method: "DELETE", headers: { "Content-Type": "application/json" } });
          if (res.ok) {
            bookmarkBtn.setAttribute("data-bookmarked", "false");
            icon.src = "https://img.icons8.com/ios/20/f0c808/bookmark-ribbon--v1.png";
            if (pageType === "library") bookmarkBtn.closest(".card")?.remove();
          }
        } else {
          res = await fetch(`/api/bookmark_set/${setId}`, { method: "POST", headers: { "Content-Type": "application/json" } });
          if (res.ok) {
            bookmarkBtn.setAttribute("data-bookmarked", "true");
            icon.src = "https://img.icons8.com/ios-filled/20/f0c808/bookmark-ribbon.png";
          }
        }
      } catch (err) {
        console.error("Bookmark error:", err);
        alert("An error occurred while updating the bookmark.");
      }
    }
  });
});