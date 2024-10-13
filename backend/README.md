# Deloitte Auditor Enterprise Chat Application

This application is designed to assist Deloitte auditors with queries related to U.S. tax law. It consists of a backend server and a frontend interface:

- Backend: A Python server using the Bottle framework that interacts with OpenAI's GPT-3.5-turbo model and stores conversation history in a MySQL database.
- Frontend: A React application that provides a user-friendly interface for auditors to input their queries and view responses.

## Database Setup

- Start MySQL Server
- Create the cmpe database
- Create the gpt_history table
        CREATE TABLE gpt_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    role VARCHAR(20),
    message TEXT,
    time DATETIME
);

## Usage

- Open the Application: Visit http://localhost:3000 in your web browser.
- Enter a Prompt: In the text area provided, type your tax-related query.
- Send the Prompt: Click the Send button to submit your query.
- View the Response: The assistant's response will appear below the prompt area.

