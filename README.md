# Pulseboard

**Async check-in system for startup teams — built with FastAPI and GPT.**

Pulseboard is a lightweight, AI-powered journaling tool that helps teams stay aligned, reflect daily, and track momentum — all without meetings.

## 🌟 Features

- **Daily Team Check-ins**: Track team engagement and participation
- **AI-Powered Insights**: Get automated summaries and trends
- **Streak Tracking**: Monitor team consistency and engagement
- **Interactive Dashboard**: Visualize team activity and progress
- **Export Capabilities**: Download team summaries for reporting

## 🚀 Getting Started

1. Clone the repository
2. Set up the backend:
   ```bash
   cd apps/backend
   python -m venv venv
   source venv/bin/activate  # or `venv\Scripts\activate` on Windows
   pip install -r requirements.txt
   ```

3. Set up the frontend:
   ```bash
   cd apps/frontend
   npm install
   ```

4. Configure environment variables:
   - Copy `.env.example` to `.env`
   - Add your OpenAI API key and other configurations

5. Run the development servers:
   ```bash
   # Terminal 1 (Backend)
   cd apps/backend
   uvicorn main:app --reload

   # Terminal 2 (Frontend)
   cd apps/frontend
   npm run dev
   ```

## 📝 Project Structure

```
pulseboard/
├── apps/
│   ├── frontend/          # React + TypeScript frontend
│   └── backend/           # FastAPI backend
├── shared/               # Shared types and utilities
└── requirements.txt      # Python dependencies
```
