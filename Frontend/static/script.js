document.addEventListener("DOMContentLoaded", function () {
  // Navigation between login, signup, and forgot password forms has been removed.
  // Each page now handles its own content via separate HTML files.

  /* --------------------------
     Profile Editing Functions
  ---------------------------*/
  window.enableEdit = function(elementId) {
    var inputField = document.getElementById(elementId);
    if (inputField) {
      inputField.disabled = false;
      inputField.focus(); // Set focus for editing
    }
  }

  window.saveProfile = function() {
    var username = document.getElementById('username');
    var email = document.getElementById('email');
    var password = document.getElementById('password');

    // Disable fields after saving
    username.disabled = true;
    email.disabled = true;
    password.disabled = true;

    // Place to add AJAX request for persisting changes
    console.log("Profile saved:", {
      username: username.value,
      email: email.value,
      password: password.value
    });
    alert("Profile saved successfully!");
  }

  /* --------------------------
     Profile Picture Upload
  ---------------------------*/
  var profileImageInput = document.getElementById('profileImageInput');
  var profilePic = document.getElementById('profilePic');

  if (profileImageInput && profilePic) {
    profileImageInput.addEventListener('change', function(event) {
      var file = event.target.files[0];
      if (file) {
        var reader = new FileReader();
        reader.onload = function(e) {
          // Update profile picture preview
          profilePic.src = e.target.result;
        }
        reader.readAsDataURL(file);
      }
    });
  }

  /* --------------------------
     Create Flashcard Functionality (for create.html)
  ---------------------------*/
  const createQuizBtn = document.getElementById("createQuizBtn");
  const flashcardContainer = document.getElementById("flashcardContainer");
  const createBox = document.querySelector(".create-box h2");

  // Only run if these elements exist (i.e. on create.html)
  if (createQuizBtn && flashcardContainer && createBox) {
      let flashcardCount = 1;
      const maxFlashcards = 50;
      let quizTitle = "";

      createQuizBtn.addEventListener("click", function () {
          quizTitle = document.getElementById("quizTitle").value;
          const quizCategory = document.getElementById("quizCategory").value;

          if (!quizTitle || !quizCategory) {
              alert("Please enter a quiz name and select a category.");
              return;
          }

          // Update the header text of the create box with the quiz title
          createBox.textContent = quizTitle;

          // Hide the quiz form
          document.getElementById("quizForm").style.display = "none";

          // Start flashcard creation
          addFlashcard();
      });

      function addFlashcard() {
          if (flashcardCount > maxFlashcards) {
              alert("You have reached the maximum number of flashcards.");
              return;
          }

          // Clear previous flashcard (if any) for single flashcard interface
          flashcardContainer.innerHTML = "";

          // Create a new flashcard element
          const flashcard = document.createElement("div");
          flashcard.classList.add("flashcard");

          flashcard.innerHTML = `
              <h3>Flashcard ${flashcardCount}</h3>
              <div class="flashcard-input-container">
                  <input type="text" placeholder="Enter flashcard name" id="flashcardInput">
              </div>
              <div class="flashcard-input-container">
                  <input type="text" placeholder="Enter flashcard content..." id="flashcardInput">
              </div>
              <div class="flashcard-buttons">
                  <button id="nextFlashcardBtn">Next Flashcard</button>
                  <button id="endQuizBtn">Save Quiz</button>
                  <button id="BackBtn">Exit</button>
              </div>
          `;

          flashcardContainer.appendChild(flashcard);

          // Next Flashcard button
          document.getElementById("nextFlashcardBtn").addEventListener("click", function () {
              if (flashcardCount < maxFlashcards) {
                  flashcardCount++;
                  addFlashcard();
              } else {
                  alert("You have reached the maximum number of flashcards.");
              }
          });

          // Save Quiz button - redirects to library.html
          document.getElementById("endQuizBtn").addEventListener("click", function () {
              window.location.href = "library.html";
          });

          // Exit button - returns to create.html
          document.getElementById("BackBtn").addEventListener("click", function () {
              window.location.href = "create.html";
          });
      }
  }
});