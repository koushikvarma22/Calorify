# Calorify 🥗⚡

![CI Status](https://img.shields.io/badge/CI-Passing-brightgreen?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-blue?style=flat-square)
![React](https://img.shields.io/badge/React-18-61DAFB?style=flat-square&logo=react)
![Flask](https://img.shields.io/badge/Flask-2.x-black?style=flat-square&logo=flask)
![MySQL](https://img.shields.io/badge/MySQL-8.0-4479A1?style=flat-square&logo=mysql)
![OpenAI](https://img.shields.io/badge/OpenAI-Vision-412991?style=flat-square&logo=openai)

Calorify is an intelligent, full-stack AI calorie and nutrition tracking application. Featuring **Cali**, an integrated multi-modal food scanner, Calorify lets users log meals instantly with a single photo, track daily hydration and workouts, and monitor real-time macronutrient progress.

---

## ✨ Features

- 📸 **AI Food Scanner (Cali)**: Instant calorie & macro estimation from food photos powered by OpenAI Vision.
- 🎯 **Macronutrient Tracking**: Real-time progress bars for Protein, Carbohydrates, and Fats against customized goals.
- 💧 **Hydration & Workout Logging**: Quick one-click increments for daily water intake and active minutes.
- 🔐 **Firebase Authentication**: Secure Google OAuth authentication and session management.
- 📊 **Interactive Food Diary**: Historical meal logging with timestamped categorization.
- 🐳 **Containerized Deployment**: Ready-to-go Dockerfile and Docker Compose setup for instant local orchestration.

---

## 🏛 Architecture Overview

For in-depth architecture details and diagrams, refer to [docs/architecture.md](docs/architecture.md).  
API specifications are documented using OpenAPI 3.0 in [docs/openapi.yaml](docs/openapi.yaml).

---

## 🚀 Quick Start

### 1. Database Setup
```bash
mysql -u root -p < database/schema.sql
mysql -u root -p < database/seed.sql   # (Optional mock data)
```

### 2. Backend Setup
```bash
cd backend
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
cp .env.example .env
python app.py
```

### 3. Frontend Setup
```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

### 4. Docker Compose
```bash
docker-compose up --build
```

---

## 🧪 Testing

Run backend test suite using `pytest`:
```bash
PYTHONPATH=. pytest backend/tests -v
```

---

## 📄 License
Distributed under the MIT License. See `LICENSE` for more information.
