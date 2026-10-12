# Nav-AI — Local AI Chatbot

Nav-AI is a web-based AI chatbot built as a learning project to explore how frontend interfaces, backend APIs, and locally running language models work together.

## Features

- Interactive chatbot interface
- Conversation sidebar and saved chat history
- Formatted AI responses
- Theme customization
- Local AI inference using Ollama

## Tech Stack

- Python
- FastAPI
- HTML, CSS, JavaScript
- Ollama
- Llama 3.2 1B

## Prerequisites

- Python installed
- Ollama installed
- The `llama3.2:1b` model downloaded in Ollama

## Run Locally

1. Install Ollama and download the model:

   `ollama pull llama3.2:1b`

2. Install the Python dependencies used by the project.

3. Start the FastAPI server:

   `python -m uvicorn main:app --reload`

4. Open `http://127.0.0.1:8000` in your browser.

## Learning Goals

This project helped me explore API integration, local LLMs, backend development, debugging, and AI-assisted coding.

## Project Status

Learning project — ongoing improvements planned.
