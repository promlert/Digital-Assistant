# Digital Assistant App Plan (Updated: January 15, 2026 - Added Stock Features)

## Requirements

The Digital Assistant app must support the following features:

1. **Voice/Text Input**: Accept voice input via microphone using ElevenLabs STT (or Deepgram as alternative for better Thai), and text input via a chat interface.
2. **Reminders with Google Calendar Integration**: Allow users to create, view, update, and delete reminders/events synced with Google Calendar.
3. **Conversational Form Filling**: Guide users through filling forms (e.g., appointments, surveys) via natural language conversation.
4. **Thai Language Support**: Handle Thai language in speech recognition, text-to-speech, and text processing (optimize for tonal language).
5. **Stock Portfolio Checking**: 
   - ผู้ใช้สามารถถามเช็คหุ้นในพอร์ตส่วนตัว (portfolio ของ user นั้น ๆ) เช่น "เช็คพอร์ตวันนี้" หรือ "PTT ในพอร์ตฉันราคาเท่าไหร่"
   - ดึงข้อมูลราคาปัจจุบัน, จำนวนหุ้น, gain/loss, มูลค่ารวม (ต้องเก็บพอร์ตใน DB หรือ link กับ broker)
6. **Stock News Alerts**:
   - ผู้ใช้กำหนด watchlist หุ้นที่สนใจ (e.g. "เตือนข่าว PTT, BANPU และหุ้นพลังงาน")
   - เตือนข่าวสำคัญแบบ proactive (voice/push/text) เมื่อมีข่าวเกี่ยวข้องหรือหุ้นในหมวดคล้ายกัน (e.g. energy sector)
   - Summarize ข่าว + relevance ด้วย Grok
7. **Technology Stack**: Use Pipecat framework for agent logic, ElevenLabs/Deepgram for STT/TTS, Grok API/Voice for AI-driven responses, **LiveKit** as real-time transport layer.

Additional requirements:
- Real-time interaction with low latency (<500ms E2E ideal)
- Natural interruptions/barge-in support
- User authentication
- Data persistence (รวมพอร์ตหุ้น + watchlist)
- Error handling and fallback
- Responsive web interface

## Tech Stack

- **Programming Language**: Python 3.10+
- **Backend Framework**: FastAPI for RESTful API and WebSocket support
- **Voice Agent Framework**: Pipecat for building conversational voice agents
- **Real-time Transport**: **LiveKit** (open-source WebRTC SFU, audio-only mode)
- **Speech Services**: 
  - STT: ElevenLabs (primary) หรือ Deepgram (alternative — รองรับไทยดีมาก + streaming)
  - TTS: ElevenLabs (Thai voices)
- **AI Service**: Grok API for text-based responses, Grok Voice API (ถ้ามี) หรือ fallback ไป ElevenLabs TTS
- **Calendar Integration**: Google Calendar API v3
- **Stock Integration** (NEW):
  - **thaistock** (UncleEngineer) — สำหรับ prototype: real-time price + historical (web scraping settrade.com, ฟรี ง่าย)
  - **Settrade Open API** (official) — สำหรับ production: real-time quotes, portfolio/account info (ต้อง OAuth/login กับ broker เช่น Pi Securities), news feed
  - Alternative: SMART Marketplace API จาก SET (delayed/real-time market data)
  - News: RSS from SET + Grok summarize หรือ web search
- **Frontend**: React.js for web interface with voice controls (WebRTC via LiveKit client SDK)
- **Database**: PostgreSQL for user data, sessions, stock portfolios, watchlists (SQLite for development)
- **Authentication**: OAuth 2.0 with Google (calendar) + Broker OAuth for Settrade (stock portfolio)
- **Hosting/Deployment**: Docker for containerization, self-host LiveKit server หรือ LiveKit Cloud, AWS/GCP/DigitalOcean
- **Other Libraries**: 
  - `google-api-python-client` for Google Calendar
  - `pipecat-ai[livekit]`
  - `livekit-plugins-turn-detector` (optional)
  - `thaistock` (pip install thaistock) สำหรับ prototype
  - `settrade` (official SDK สำหรับ Open API ถ้า production)
  - `websockets`, `pydantic`, `uvicorn`

## System Architecture

### High-Level Architecture

```
[Web Client (React + LiveKit JS SDK)] <---WebRTC (audio)---> [LiveKit Server (SFU)]
                          |
                          v
            [FastAPI Server (control + auth)]
                          |
                          v
                  [Pipecat Agent]
                          |
+-------------------------+-------------------------+
|                         |                         |
[ElevenLabs/Deepgram STT + VAD] [Grok API]             [ElevenLabs TTS]
|
+-------------------------+-------------------------+
|                         |                         |
[Google Calendar API]     [Stock Service: thaistock / Settrade Open API]     [News RSS + Grok Summarize]
|
v
[(Database: portfolios + watchlists)]
```

### Data Flow (Stock Features)
- User พูด "เช็คพอร์ตหุ้น" → Pipecat detect intent → call stock_service.get_portfolio(user_id)
- User เพิ่ม watchlist → เก็บใน DB → periodic task (cron) เช็คข่าว → ถ้ามี match ส่ง notification หรือ voice alert
- Interruptions ทำงานเหมือนเดิม (LiveKit VAD + Pipecat strategy)

## Project Files and Structure (เพิ่ม stock)



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
11. **Stock Portfolio Prototype (Week 11)**: Integrate thaistock สำหรับ price checking + basic portfolio storage in DB
12. **Stock News Alerts + Production (Week 12)**: Add Settrade Open API (broker login), watchlist, periodic news check + proactive alerts, test interruptions กับ stock queries

## Interruptions / Barge-in Handling

เหมือนเดิม: LiveKit hardware VAD + custom EOU + Pipecat allow_interruptions=True  
(สำคัญสำหรับ stock queries ที่อาจยาว เช่น "สรุปข่าว PTT ล่าสุด")

## Security Considerations (เพิ่ม financial)

- **Financial Data**: Encrypt portfolio/watchlist ใน DB (ใช้ Fernet หรือ vault)
- Broker OAuth: ใช้ Settrade Open API ด้วย minimal scope (read-only สำหรับ portfolio)
- Consent: User ยินยอมชัดเจนก่อน link broker
- No storage of sensitive broker credentials
- Rate limiting + audit logs สำหรับ stock API calls

## Mermaid Diagram 

```mermaid
graph TD
    A[User] --> B[Web Client + LiveKit JS SDK]
    B <--> C[LiveKit Server SFU WebRTC Audio]
    C --> D[Pipecat Agent via LiveKitTransport]
    D --> E[ElevenLabs/Deepgram STT + VAD/EOU]
    D --> F[Grok API]
    D --> G[ElevenLabs TTS]
    D --> H[Google Calendar API]
    D --> I[Stock Service: thaistock / Settrade API]
    D --> J[News Service + Grok Summarize]
    H --> K[(Database: users, calendars, portfolios, watchlists)]
    I --> K
    J --> K
    G --> C
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
