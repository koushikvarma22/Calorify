# Calorify Architecture

Calorify is an AI-powered calorie and nutrition tracking platform featuring image-based food analysis, daily macronutrient breakdown, and hydration tracking.

## System Topology

```mermaid
graph TD
    Client["React + Vite Frontend (SPA)"]
    Auth["Firebase Authentication"]
    API["Flask REST Backend"]
    DB[(MySQL / SQLite Database)]
    Vision["OpenAI Vision API (Cali)"]

    Client -->|Google Sign-In| Auth
    Client -->|Authenticated REST API Requests| API
    API -->|Persist Users, Meals, Daily Logs| DB
    API -->|Multi-modal Food Image Analysis| Vision
```

## Core Modules
- **Frontend**: React 18 SPA built with Vite, Axios, Lucide Icons, and Vanilla CSS glassmorphic design.
- **Backend**: Python Flask REST API with SQLAlchemy ORM, Blueprint routing, and OpenAI SDK integration.
- **Database**: Relational schema supporting users, timestamped food entries, and daily aggregation logs.
- **Authentication**: Google Firebase OAuth provider for secure token-based user identity.
