# Calorify

AI calorie tracking web app starter: React + Vite + Axios, Flask, MySQL, Firebase Google authentication, and OpenAI-powered Cali food analysis.

## Run backend
1. Create MySQL database: `CREATE DATABASE calorify;`
2. `cd backend`
3. `python -m venv venv`
4. Windows: `venv\\Scripts\\activate`
5. `pip install -r requirements.txt`
6. Copy `.env.example` to `.env` and configure it.
7. `python app.py`

## Run frontend
1. `cd frontend`
2. `npm install`
3. Copy `.env.example` to `.env` and add Firebase Web App values.
4. `npm run dev`

Never put the OpenAI API key in the frontend.
