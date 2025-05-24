# PulseBoard

A modern team pulse survey application built with FastAPI and React.

## Features

- User authentication and authorization
- Team pulse surveys
- Real-time updates
- Slack integration
- Email notifications
- Beautiful and responsive UI

## Tech Stack

### Backend
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- Celery
- Redis
- JWT Authentication

### Frontend
- React
- TypeScript
- Tailwind CSS
- Axios
- React Query

## Prerequisites

- Docker and Docker Compose
- Node.js 18+
- Python 3.11+
- PostgreSQL 15+
- Redis 7+

## Getting Started

1. Clone the repository:
```bash
git clone https://github.com/yourusername/pulseboard.git
cd pulseboard
```

2. Create and configure environment files:
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. Start the development environment:
```bash
docker-compose up -d
```

4. Initialize the database:
```bash
docker-compose exec backend python scripts/init_db.py
```

5. Access the applications:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/api/docs

## Development

### Backend Development

1. Create and activate a virtual environment:
```bash
cd apps/backend
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the development server:
```bash
./scripts/run_dev.sh
```

### Frontend Development

1. Install dependencies:
```bash
cd apps/frontend
npm install
```

2. Start the development server:
```bash
npm run dev
```

## Testing

### Backend Tests
```bash
cd apps/backend
pytest
```

### Frontend Tests
```bash
cd apps/frontend
npm test
```

## Deployment

1. Build the Docker images:
```bash
docker-compose build
```

2. Start the production environment:
```bash
docker-compose -f docker-compose.prod.yml up -d
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
