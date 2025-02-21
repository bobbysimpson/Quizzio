CREATE DATABASE IF NOT EXISTS sgbsimp2;
USE sgbsimp2;

-- USERS TABLE: Stores user account information
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- FLASHCARD SETS TABLE: Stores sets of flashcards
CREATE TABLE flashcard_sets (
    set_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_public BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- FLASHCARDS TABLE: Stores individual flashcards within a set
CREATE TABLE flashcards (
    flashcard_id INT AUTO_INCREMENT PRIMARY KEY,
    set_id INT NOT NULL,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (set_id) REFERENCES flashcard_sets(set_id) ON DELETE CASCADE
);

-- USER PROGRESS TABLE: Tracks user's performance on flashcards
CREATE TABLE user_progress (
    progress_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    flashcard_id INT NOT NULL,
    is_correct BOOLEAN NOT NULL,
    attempted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (flashcard_id) REFERENCES flashcards(flashcard_id) ON DELETE CASCADE
);

-- BOOKMARKS TABLE: Stores user's bookmarked flashcards
CREATE TABLE bookmarks (
    bookmark_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    flashcard_id INT NOT NULL,
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (flashcard_id) REFERENCES flashcards(flashcard_id) ON DELETE CASCADE
);

-- INDEXES FOR PERFORMANCE
CREATE INDEX idx_user_progress ON user_progress(user_id, flashcard_id);
CREATE INDEX idx_bookmarks ON bookmarks(user_id, flashcard_id);

-- TEST DATA INSERTION
INSERT INTO users (username, email, password_hash) VALUES
('testuser', 'test@example.com', 'hashedpassword');

INSERT INTO flashcard_sets (user_id, title, description, is_public) VALUES
(1, 'Biology Basics', 'Basic concepts in biology', TRUE),
(1, 'History Facts', 'Important historical events', FALSE);

INSERT INTO flashcards (set_id, question, answer) VALUES
(1, 'What is the powerhouse of the cell?', 'Mitochondria'),
(1, 'What is DNA?', 'Deoxyribonucleic Acid'),
(2, 'Who was the first US president?', 'George Washington');

INSERT INTO user_progress (user_id, flashcard_id, is_correct) VALUES
(1, 1, TRUE),
(1, 2, FALSE);

INSERT INTO bookmarks (user_id, flashcard_id) VALUES
(1, 1),
(1, 2);

-- CHECK DATABASE CONTENT
SELECT * FROM users;
SELECT * FROM flashcard_sets;
SELECT * FROM flashcards;
SELECT * FROM user_progress;
SELECT * FROM bookmarks;