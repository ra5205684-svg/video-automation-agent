# Video Automation Agent 🎬

A full-featured automated video creation and YouTube upload system that generates and publishes videos daily.

## Features

✅ **Automated Video Generation** - Create videos on a daily schedule
✅ **YouTube Integration** - Automatic uploads to your channel
✅ **Smart Scheduling** - Configurable upload times
✅ **Dashboard** - Manage videos and monitor uploads
✅ **API-First Architecture** - RESTful API for all operations
✅ **Error Handling** - Retry logic and notifications
✅ **Analytics** - Track video performance
✅ **Multi-format Support** - Various video types and resolutions

## Quick Start

### Prerequisites
- Python 3.9+
- Node.js 16+ (for dashboard)
- Docker & Docker Compose
- YouTube API credentials
- PostgreSQL

### Installation

```bash
# Clone repository
git clone https://github.com/ra5205684-svg/video-automation-agent.git
cd video-automation-agent

# Setup backend
cd backend
pip install -r requirements.txt
cp .env.example .env
# Configure your YouTube API credentials in .env

# Setup frontend
cd ../frontend
npm install

# Start services
cd ..
docker-compose up
```

## Architecture

```
├── backend/              # FastAPI service
├── frontend/             # React dashboard
├── workers/              # Video generation workers
├── .github/workflows/    # GitHub Actions automation
├── docker-compose.yml    # Service orchestration
└── docs/                 # Documentation
```

## Configuration

See [SETUP.md](./docs/SETUP.md) for detailed configuration instructions.

## API Documentation

API docs available at `http://localhost:8000/docs` after startup.

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md)

## License

MIT
