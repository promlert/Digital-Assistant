# Digital Assistant App Plan

## Requirements

The Digital Assistant app must support the following features:

1. **Voice/Text Input**: Accept voice input via microphone using ElevenLabs STT, and text input via a chat interface.
2. **Reminders with Google Calendar Integration**: Allow users to create, view, update, and delete reminders/events synced with Google Calendar.
3. **Conversational Form Filling**: Guide users through filling forms (e.g., appointments, surveys) via natural language conversation.
4. **Thai Language Support**: Handle Thai language in speech recognition, text-to-speech, and text processing.
5. **Technology Stack**: Use Pipecat framework for agent logic, ElevenLabs for STT/TTS, and Grok Voice API for AI-driven responses.

Additional requirements:
- Real-time interaction
- User authentication
- Data persistence
- Error handling and fallback
- Responsive web interface

## Tech Stack

- **Programming Language**: Python 3.9+
- **Backend Framework**: FastAPI for RESTful API and WebSocket support
- **Voice Agent Framework**: Pipecat for building conversational voice agents
- **Speech Services**: ElevenLabs API for Speech-to-Text (STT) and Text-to-Speech (TTS)
- **AI Service**: Grok API for text-based AI responses, Grok Voice API for voice responses
- **Calendar Integration**: Google Calendar API v3
- **Frontend**: React.js for web interface with voice controls
- **Database**: PostgreSQL for user data and session storage (SQLite for development)
- **Authentication**: OAuth 2.0 with Google for user login and calendar access
- **Hosting/Deployment**: Docker for containerization, AWS/GCP for cloud hosting
- **Other Libraries**: 
  - `google-api-python-client` for Google Calendar
  - `websockets` for real-time communication
  - `pydantic` for data validation
  - `uvicorn` for ASGI server

## System Architecture

### High-Level Architecture
```
[Web Client] <---HTTP/WebSocket---> [FastAPI Server] <---API---> [External Services]
                                      |
                                      v
                               [Pipecat Agent]
                                      |
                    +-----------------+-----------------+
                    |                 |                 |
               [ElevenLabs STT] [Grok API/Voice] [Google Calendar API]
```

### Data Flow
1. User speaks or types input in web client
2. Audio/text sent to FastAPI server
3. Server routes to Pipecat agent
4. Agent uses ElevenLabs STT to convert speech to text (if voice)
5. Text sent to Grok API for processing
6. Grok returns response text
7. Agent uses Grok Voice API or ElevenLabs TTS to generate voice response
8. Response sent back to client
9. For reminders: Agent makes API calls to Google Calendar

### Components
- **Client Layer**: React app with microphone access, text input, audio playback
- **API Layer**: FastAPI handles requests, authentication, WebSocket connections
- **Agent Layer**: Pipecat manages conversation flow, state, and integrations
- **Service Layer**: Wrappers for external APIs (ElevenLabs, Grok, Google Calendar)
- **Data Layer**: Database for user sessions, cached data

## Project Files and Structure

```
digital-assistant/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI application entry point
│   │   ├── agent.py             # Pipecat agent configuration
│   │   ├── stt_service.py       # ElevenLabs STT integration
│   │   ├── tts_service.py       # ElevenLabs/Grok Voice TTS integration
│   │   ├── grok_service.py      # Grok API integration
│   │   ├── calendar_service.py  # Google Calendar API integration
│   │   ├── auth.py              # OAuth authentication
│   │   ├── models.py            # Pydantic models and database schemas
│   │   ├── database.py          # Database connection and utilities
│   │   └── config.py            # Configuration settings
│   ├── tests/
│   │   ├── test_agent.py
│   │   └── test_services.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── README.md
├── frontend/
│   ├── public/
│   │   ├── index.html
│   │   └── favicon.ico
│   ├── src/
│   │   ├── App.js
│   │   ├── components/
│   │   │   ├── VoiceInput.js
│   │   │   ├── TextInput.js
│   │   │   ├── ChatDisplay.js
│   │   │   └── ReminderList.js
│   │   ├── services/
│   │   │   ├── api.js
│   │   │   └── websocket.js
│   │   ├── utils/
│   │   │   └── audioUtils.js
│   │   └── index.js
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml
├── .env.example
├── .gitignore
└── README.md
```

## Development Milestones

1. **Project Setup (Week 1)**: Initialize repository, set up Python/Node.js environments, create basic project structure, configure Docker.
2. **Backend Foundation (Week 2)**: Implement FastAPI server, basic routing, database setup, authentication with Google OAuth.
3. **Voice/Text Input Integration (Week 3)**: Integrate ElevenLabs STT/TTS, implement basic voice and text input handling in Pipecat agent.
4. **AI Integration (Week 4)**: Connect to Grok API and Grok Voice API, implement basic conversational responses.
5. **Google Calendar Integration (Week 5)**: Implement reminder creation, viewing, updating via Google Calendar API.
6. **Conversational Form Filling (Week 6)**: Develop state management for multi-turn conversations, implement form filling logic.
7. **Thai Language Support (Week 7)**: Test and optimize STT/TTS for Thai, add language detection and processing.
8. **Frontend Development (Week 8)**: Build React interface, integrate WebSocket for real-time updates, add voice controls.
9. **Testing and Refinement (Week 9)**: Unit tests, integration tests, user testing, bug fixes.
10. **Security and Deployment (Week 10)**: Implement security measures, deploy to cloud, monitor performance.

## Security Considerations

1. **API Key Management**: Store API keys for ElevenLabs, Grok, Google in environment variables, never in code. Use secret management services in production.
2. **Authentication and Authorization**: Implement OAuth 2.0 for user login. Ensure users can only access their own calendar data.
3. **Data Encryption**: Encrypt sensitive data at rest and in transit. Use HTTPS for all communications.
4. **Input Validation**: Validate all user inputs to prevent injection attacks. Sanitize text and audio data.
5. **Rate Limiting**: Implement rate limiting on API endpoints to prevent abuse.
6. **Privacy Protection**: Handle voice data carefully - process in memory, don't store audio files unless necessary. Comply with data protection regulations (GDPR, etc.).
7. **Access Controls**: Use role-based access control if needed. Limit API permissions to minimum required.
8. **Logging and Monitoring**: Log security events without exposing sensitive data. Monitor for unusual activity.
9. **Dependency Security**: Regularly update dependencies, scan for vulnerabilities.
10. **Backup and Recovery**: Implement data backups and disaster recovery plans.

## Mermaid Diagram

```mermaid
graph TD
    A[User] --> B[Web Client]
    B --> C[FastAPI Server]
    C --> D[Pipecat Agent]
    D --> E[ElevenLabs STT]
    D --> F[Grok API]
    D --> G[Grok Voice API / ElevenLabs TTS]
    D --> H[Google Calendar API]
    H --> I[(Database)]
    C --> I
    G --> B
    F --> D
```</content>
</xai:function_call name="update_todo_list">
<parameter name="todos">[x] Define detailed requirements based on specified features (voice/text input, reminders with Google Calendar, conversational form filling, Thai language support, Pipecat/ElevenLabs STT + Grok Voice API)
[x] Select and justify tech stack components
[x] Design system architecture including data flow and integrations
[x] List necessary files and project structure
[x] Define development milestones and phases
[x] Identify security considerations and best practices
[x] Compile and write the complete plan to plan.md