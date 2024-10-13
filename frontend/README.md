# Deloitte Auditor Enterprise Chat UI

## Overview

This project is a React.js application designed as part of a Deloitte Auditor Enterprise Chat interface. The primary functionality of this application is to allow users (auditors) to interact with OpenAI's GPT-3.5-turbo model for guidance on US tax law. The application restricts queries to tax-related questions and provides clear, concise answers based on the user's prompt. If the query is unrelated to US tax law, the system warns the user to limit questions to the relevant domain.

## Features

- Prompt Input: Users can input a query related to tax laws.
- Send & Cancel Buttons:
    - Send: Sends the user prompt along with predefined contextual information to the GPT-3.5-turbo model.
    - Cancel: Clears the input field and any generated responses.
- Response Section: Displays the response returned by the GPT-3.5-turbo model.
- Custom Message: The system ensures all responses are tailored to US tax law-related queries and warns users if they stray off-topic.

## Setup

Provide your chatGPT api key in .env file in src folder

## Technologies Used

- React: For building the user interface and handling state management.
- OpenAI API (GPT-3.5 Turbo): For generating responses based on user inputs.
- CSS: Basic styling for the layout and UI components.

## Usage

- Enter a question related to US Tax Law in the text box provided.
- Click the Send button to submit the question to the AI.
- The AI response will appear below the "Response" section.
- To clear the input and response, click the Cancel button.
