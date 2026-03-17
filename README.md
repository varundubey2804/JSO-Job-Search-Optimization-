# Job Search Optimization (JSO) Agent

The JSO Agent is a dynamic AI-powered system designed to generate optimized Boolean and X-Ray job search queries for major job platforms including LinkedIn, Indeed, Naukri, Glassdoor, Reed, and TotalJobs.

## Architecture Diagram

```mermaid
graph TD
    A[User Dashboards (HTML/CSS/Vanilla JS)] -->|HTTP Requests| B[NodeJS API Gateway]
    B -->|Proxy| C[FastAPI Backend (Python)]
    C -->|JobAgentOrchestrator| D[Skill Extractor Agent]
    C -->|JobAgentOrchestrator| E[Query Generator Agent]
    C -->|JobAgentOrchestrator| F[Platform Adapter Agent]
    
    D --> G[Proxy LLM (OpenAI Compatible)]
    E --> G
    
    C --> H[(Supabase PostgreSQL Database)]
    C --> I[Supabase Resume Storage]
```

## Supported Platforms
- LinkedIn
- Indeed
- Naukri
- Glassdoor
- Reed
- TotalJobs

## Project Structure
- `backend/`: Python FastAPI service, containing the AI agents (`SkillExtractor`, `QueryGenerator`, `PlatformAdapter`) and services.
- `node_gateway/`: Node.js Express server acting as an API gateway.
- `frontend/`: Vanilla HTML, CSS, and JS dashboards (`user`, `hr`, `admin`, `licensing`).
- `database/`: Supabase PostgreSQL schema (`schema.sql`).

## Setup Instructions

### 1. Backend (Python FastAPI)
1. Navigate to the root directory.
2. Create a virtual environment: `python3 -m venv venv`
3. Activate the environment: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Configure `.env` file with your Proxy LLM API keys/URLs (`PROXY_API_KEY`, `PROXY_BASE_URL`) (or rely on the built-in mock fallback).
6. Run the server: `cd backend && python3 app.py` (Runs on port 8000).

### 2. API Gateway (NodeJS)
1. Open a new terminal.
2. Navigate to `node_gateway/`.
3. Install dependencies: `npm install`
4. Start the gateway: `node server.js` (Runs on port 3000, proxies to 8000, and serves the static frontend).

### 3. Frontend Dashboards
1. Open your browser and navigate to `http://localhost:3000/`.
2. The user dashboard will be the default view.
3. Use the sidebar to navigate to HR Consultant, Admin, and Licensing dashboards.

## Deployment Design
- **Frontend**: Vercel (serves the static HTML/CSS/JS)
- **Backend (API Gateway & Python Service)**: Docker container hosted on AWS/GCP or Render/Railway.
- **Database**: Supabase (PostgreSQL)
- **File Storage**: Supabase Storage
- **AI Models**: Proxy LLM (OpenAI Compatible)
