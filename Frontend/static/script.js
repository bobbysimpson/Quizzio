let flashcardCount = 1;
const maxFlashcards = 50;
let quizTitle = "";
let quizCategory = "";
let flashcards = []; // store all created flashcards here

document.addEventListener("DOMContentLoaded", function () {
    /* --------------------------
       Existing Form Navigation   <!-- Version 1.3-->
    ---------------------------*/
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
      const editURL = "{{ url_for('/edit')}}";
      var username = document.getElementById('username');
      var email = document.getElementById('email');
      var password = document.getElementById('password');

      // Disable fields after saving
      username.disabled = true;
      email.disabled = true;
      password.disabled = true;

      // Place to add AJAX request for persisting changes

      let data = new FormData()
      data.append("newUsername",  username.value)
      data.append("newEmail", email.value)
      data.append("newPassword", password.value)
      fetch("http://127.0.0.1:5000/edit", { // temporary solution - change in production !!!!!
          "method": "POST",
          "body": data,
      }).then(console.log("Sent data"))

      console.log("Profile saved:", {
        username: username.value,
        email: email.value,
        password: password.value
      });
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
            quizCategory = document.getElementById("quizCategory").value; // got rid of const here as category wasnt getting thru to backend

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
      
          // Save previous flashcard before overwriting the container
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
                  <input type="text" placeholder="Enter front content" id="flashcardInputFront">
              </div>
              <div class="flashcard-input-container">
                  <input type="text" placeholder="Enter back content..." id="flashcardInputBack">
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
              // Save current flashcard
              const name = document.getElementById("flashcardInputFront").value;
              const content = document.getElementById("flashcardInputBack").value;
              flashcards.push({ name, content });
      
              // Submit to backend
              submitQuiz();
          });
      
          document.getElementById("BackBtn").addEventListener("click", function () {
              window.location.href = "create.html";
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
    async function deleteQuiz(setId) {
      if (!confirm('Are you sure you want to delete this quiz? This action cant be undone.')) {
        return;
      }

      try {
        const response = await fetch(`/api/sets/${setId}`, {
          method: 'DELETE',
          headers: {
            'Content-Type': 'application/json',
          },
        });

        const result = await response.json();

        if (response.ok) {
          const card = document.querySelector(`.card[data-set-id="${setId}"]`);
          if (card) {
            card.remove();
          }
          alert('Quiz deleted successfully!');
          if (!document.querySelector('.card')) {
            const container = document.querySelector('.quizzes-container');
            container.innerHTML = `
              <div class="empty-library">
                <p>You have no saved quizzes.</p>
                <a href="{{ url_for('views.index') }}" class="browse-link">Click here to browse or search for quizzes.</a>
              </div>
            `;
          }
        } else {
          alert(result.error || 'Failed to delete quiz');
        }
      } catch (error) {
        console.error('Error deleting quiz:', error);
        alert('An error occurred while deleting the quiz');
      }
    }
    document.querySelectorAll('.delete-button').forEach(button => {
      button.addEventListener('click', () => deleteQuiz(button.getAttribute('data-quiz-id')));
    });

    document.querySelectorAll('.bookmark-button').forEach(button => {
      button.addEventListener('click', async function() {
          const setId = this.getAttribute('data-set-id');
          const isBookmarked = this.getAttribute('data-bookmarked') === 'true';
          const bookmarkIcon = this.querySelector('.bookmark-icon');
          const card = this.closest('.card');
  
          try {
              let response;
              if (isBookmarked) {
                  response = await fetch(`/api/unbookmark_set/${setId}`, {
                      method: 'DELETE',
                      headers: { 'Content-Type': 'application/json' },
                  });
                  if (response.ok) {
                      if (card) card.remove();
  
                      if (!document.querySelectorAll('.card').length) {
                          document.querySelector('.quizzes-container').innerHTML = `
                              <div class="empty-library">
                                  <p>You have no saved quizzes.</p>
                                  <a href="/index" class="browse-link">Click here to browse or search for quizzes.</a>
                              </div>
                          `;
                      }
                  }
              } else {
                  response = await fetch(`/api/bookmark_set/${setId}`, {
                      method: 'POST',
                      headers: { 'Content-Type': 'application/json' },
                  });
              }
  
              const result = await response.json();
              if (response.ok) {
                  if (isBookmarked) {
                      bookmarkIcon.src = 'https://img.icons8.com/ios/20/f0c808/bookmark-ribbon--v1.png'; // Outline
                      this.setAttribute('data-bookmarked', 'false');
                  } else {
                      bookmarkIcon.src = 'https://img.icons8.com/ios-filled/20/f0c808/bookmark-ribbon.png'; // Filled 
                      this.setAttribute('data-bookmarked', 'true');
                  }
                  console.log(result.message);
              } else {
                  alert(result.error || 'Failed to update bookmark');
              }
          } catch (error) {
              console.error('Error updating bookmark:', error);
              alert('An error occurred while updating the bookmark');
          }
      });
  });
});
