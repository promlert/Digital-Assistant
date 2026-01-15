# Digital Assistant

A voice-enabled digital assistant with text input, reminders integration via Google Calendar, conversational form filling, and Thai language support. Built using Pipecat, ElevenLabs STT/TTS, and Grok Voice API.

## Features

- Voice and text input
- Google Calendar reminders
- Conversational form filling
- Thai language support
- Real-time interaction

## Tech Stack

- Backend: Python, FastAPI, Pipecat
- Frontend: React.js
- Services: ElevenLabs, Grok API, Google Calendar API

## Setup

1. Clone the repository
2. Set up backend: `cd backend && pip install -r requirements.txt`
3. Set up frontend: `cd frontend && npm install`
4. Configure environment variables (see .env.example)
5. Run with Docker: `docker-compose up`

## Architecture

See [plan.md](plan.md) for detailed architecture and implementation plan.

## License

MIT