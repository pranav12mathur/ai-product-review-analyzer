# AI Product Review Analyzer

This project was built as part of an internship assignment.

The main idea behind the project is to take product reviews from users and generate useful insights using AI. The application can identify common complaints, positive points, overall customer sentiment, and also generate marketing content like ad copy and hooks.

I used Streamlit for the frontend because it was simple and quick to work with, and Groq API for the AI analysis part.


## Features

- Enter product name or URL
- Paste product reviews/comments
- Analyze reviews using AI
- Detect common complaints
- Find positive highlights
- Generate sentiment summary
- Generate marketing content
- Generate AI image and video prompts


## Technologies Used

- Python
- Streamlit
- Groq API
- Llama 3.3 70B model
- python-dotenv


## Project Workflow

1. User enters product name or product URL
2. User pastes product reviews/comments
3. Reviews are sent to the LLM using Groq API
4. AI generates insights and marketing content
5. Results are displayed on the screen


## Installation

Clone the repository:

```bash
git clone <your-repository-link>