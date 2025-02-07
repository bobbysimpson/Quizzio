document.addEventListener("DOMContentLoaded", function () {  //javascript for animations by Rahul Mehra still learning and improving this 
    const createQuizBtn = document.getElementById("createQuizBtn");
    const flashcardContainer = document.getElementById("flashcardContainer");
    const createBox = document.querySelector(".create-box h2"); 

    let flashcardCount = 1; 
    const maxFlashcards = 5; 
    let quizTitle = ""; 

    createQuizBtn.addEventListener("click", function () {
        quizTitle = document.getElementById("quizTitle").value;
        const quizCategory = document.getElementById("quizCategory").value;

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

        
        flashcardContainer.innerHTML = "";

        
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

        // button links
        document.getElementById("nextFlashcardBtn").addEventListener("click", function () {
            if (flashcardCount < maxFlashcards) {
                flashcardCount++;
                addFlashcard();
            } else {
                alert("You have reached the maximum number of flashcards.");
            }
        });

        document.getElementById("endQuizBtn").addEventListener("click", function () {
            window.location.href = "library.html"; 
        });

        document.getElementById("BackBtn").addEventListener("click", function () {
            window.location.href = "create.html"; 
        });
    }
});