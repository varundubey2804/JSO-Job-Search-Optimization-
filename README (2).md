<div align="center">

<br/>

# 🔍 JSO — Job Search Optimization Agent

### *Stop searching blindly. Start searching smart.*

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Node.js](https://img.shields.io/badge/Node.js-18+-339933?style=for-the-badge&logo=nodedotjs&logoColor=white)](https://nodejs.org)
[![Supabase](https://img.shields.io/badge/Supabase-PostgreSQL-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white)](https://supabase.com)
[![Google Gemini](https://img.shields.io/badge/Google%20Gemini-AI-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)

<br/>

> **Agentic JSO** is a full-stack, AI-powered career intelligence platform designed for the **AariyaTech Corp** Agentic AI ecosystem. It automatically generates hyper-targeted **Boolean** and **X-Ray search queries** for every major job platform, bridging the *Search Literacy Gap* for job seekers and saving HR consultants hours of manual effort.

<br/>

---

</div>

## ✨ What Makes JSO Different?

Most job searches are scattershot. JSO uses a **multi-agent AI pipeline** powered by Google Gemini (with a Groq Llama 3.3 fallback) to:

- 🧠 **Extract skills** from candidate resumes automatically to reduce HR burnout.
- 🎯 **Generate platform-specific Boolean queries** that actually surface the right results.
- 🌐 **Adapt queries for 6 major platforms** — LinkedIn, Indeed, Naukri, Glassdoor, Reed, TotalJobs — with their unique syntax quirks.
- 📊 **Track analytics and usage** through a role-based gateway system (User, HR, Admin, Licensing).
- 🛡️ **Ensure Ethical AI** by keeping data processing transparent, localized, and inclusive.

---

## 🚀 System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│               Frontend  (HTML / CSS / Vanilla JS)               │
│       User │ HR Consultant │ Admin │ Licensing Dashboards        │
└────────────────────────┬────────────────────────────────────────┘
                         │  HTTP Requests
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│              Node.js API Gateway  (Port 3000)                   │
│          Handles Routing, Proxying & Static Files               │
└────────────────────────┬────────────────────────────────────────┘
                         │  Proxy
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                  FastAPI Backend  (Port 8000)                   │
│                                                                 │
│   ┌──────────────── JobAgentOrchestrator ─────────────────────┐ │
│   │                                                           │ │
│   │  ┌─────────────────┐  ┌─────────────────┐  ┌──────────┐  │ │
│   │  │ SkillExtractor  │→ │  QueryGenerator  │→ │ Platform │  │ │
│   │  │     Agent       │  │      Agent       │  │ Adapter  │  │ │
│   │  └─────────────────┘  └─────────────────┘  └──────────┘  │ │
│   │                              ▼                            │ │
│   │              Google Gemini 1.5 Flash (Primary)            │ │
│   │              Groq Llama 3.3           (Fallback)           │ │
│   └───────────────────────────────────────────────────────────┘ │
│                                                                 │
│          ┌──────────────────┐   ┌───────────────────┐          │
│          │     Supabase     │   │     Supabase      │          │
│          │   PostgreSQL     │   │  Cloud Storage    │          │
│          └──────────────────┘   └───────────────────┘          │
└─────────────────────────────────────────────────────────────────┘
```

> **Offline Fallback:** If no API keys are configured or rate limits are hit, JSO automatically switches to a built-in **mock response engine** — ensuring the UI never breaks during local testing.

---

## 🎯 Supported Platforms

| Platform | Query Style | X-Ray Support |
|----------|-------------|:---:|
| 🔵 **LinkedIn** | Boolean + field operators | ✅ |
| 🟢 **Indeed** | Boolean + proximity search | ✅ |
| 🟠 **Naukri** | Keyword + Boolean | ✅ |
| 🟡 **Glassdoor** | Boolean | ✅ |
| 🔴 **Reed** | Boolean + category filters | ✅ |
| 🟣 **TotalJobs** | Keyword + Boolean | ✅ |

---

## 📁 Project Structure

```
JSO/
├── 📂 backend/                  # Python FastAPI service & AI Agents
│   ├── 📂 agent/                # Orchestration, Skill Extraction, Query Generation
│   ├── 📂 api/                  # FastAPI Routes & Auth logic
│   ├── 📂 models/               # Pydantic schemas
│   ├── 📂 services/             # LLM integrations (Gemini/Groq) & Storage
│   └── app.py                   # FastAPI Application entry point
│
├── 📂 node_gateway/             # Node.js Express API Gateway
│   ├── server.js                # Proxies requests & serves frontend
│   └── routes.js                # Axios proxy routing to backend
│
├── 📂 frontend/                 # Vanilla HTML/CSS/JS — Glassmorphism UI
│   ├── 📂 css/                  # Theming and styling
│   ├── 📂 dashboards/           # User, HR, Admin, and Licensing HTML views
│   └── 📂 js/                   # Client-side API fetching and DOM manipulation
│
└── 📂 database/
    └── schema.sql               # Supabase PostgreSQL relational schema
```

---

## ⚙️ Setup & Installation

### Prerequisites

- Python 3.9+
- Node.js 18+
- A [Google AI Studio](https://ai.google.dev/) API key (Gemini)
- A [Groq](https://groq.com) API key *(optional fallback)*

---

### 1️⃣ Configure Environment

Create a `.env` file in the root of your project:

```env
# AI Configuration
GOOGLE_AI_API_KEY="your_google_gemini_key_here"
GROQ_API_KEY="your_groq_api_key_here"

# Server Config
PORT=8000
HOST=0.0.0.0
GATEWAY_PORT=3000
BACKEND_URL="http://localhost:8000"

# Database (Optional for prototype)
SUPABASE_URL="https://your-project.supabase.co"
SUPABASE_KEY="your_supabase_anon_key"
```

---

### 2️⃣ Backend — Python FastAPI

```bash
cd backend

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# Install dependencies
pip install fastapi uvicorn groq google-generativeai pydantic python-multipart supabase

# Start the backend (reads .env from project root)
uvicorn app:app --reload --env-file ../.env
```

> ✅ Backend running at `http://127.0.0.1:8000`

---

### 3️⃣ API Gateway — Node.js

```bash
cd node_gateway

# Install dependencies
npm install express cors dotenv axios multer form-data

# Start the gateway
node server.js
```

> ✅ Gateway running at `http://localhost:3000` — proxies to `:8000` and serves the frontend.

---

### 4️⃣ Frontend Dashboards

Open your browser and navigate to:

👉 **`http://localhost:3000/dashboards/user.html`**

| Dashboard | File Path |
|-----------|-----------|
| 👤 User | `/dashboards/user.html` |
| 🧑‍💼 HR Consultant | `/dashboards/hr.html` |
| 🛡️ Admin | `/dashboards/admin.html` |
| 📄 Licensing | `/dashboards/licensing.html` |

---

## 🤖 How the AI Pipeline Works

```
Your Resume (PDF / DOCX)
        │
        ▼
┌───────────────────┐
│  SkillExtractor   │  ← Parses resume, identifies skills, titles, experience levels
│      Agent        │
└────────┬──────────┘
         │  Structured skill set
         ▼
┌───────────────────┐
│  QueryGenerator   │  ← Builds Boolean logic: (Python OR Django) AND "Machine Learning"
│      Agent        │
└────────┬──────────┘
         │  Raw Boolean query
         ▼
┌───────────────────┐
│  PlatformAdapter  │  ← Translates to LinkedIn, Naukri, Indeed syntax and more
│      Agent        │
└────────┬──────────┘
         │
         ▼
  6 Platform-Ready Search Queries ✅
```

---

## 🛠️ Tech Stack

**Agentic Backend**
- `FastAPI` — async Python REST API
- `Google Generative AI SDK` — primary LLM inference (Gemini 1.5 Flash)
- `Groq SDK` — fallback LLM inference (Llama 3.3)
- `Supabase Python` — persistent data and storage

**Gateway**
- `Node.js` + `Express` — API proxy and static file server
- `Axios` + `Multer` — forwarding multipart form data (CV parsing)

**Frontend**
- Vanilla `HTML5` / `CSS3` / `JavaScript` — lightweight, zero-framework, dark-mode native dashboards with Glassmorphism UI

---

## 🤝 Contributing

Contributions are what make open source amazing!

```bash
# 1. Fork the repository
# 2. Create your feature branch
git checkout -b feature/AmazingFeature

# 3. Commit your changes
git commit -m 'Add some AmazingFeature'

# 4. Push to the branch
git push origin feature/AmazingFeature

# 5. Open a Pull Request 🎉
```

---

## 📄 License

Distributed under the **MIT License**. See [`LICENSE`](LICENSE) for details.

---

## 👨‍💻 Author

**Varun Dubey**

[![GitHub](https://img.shields.io/badge/GitHub-varundubey2804-181717?style=for-the-badge&logo=github)](https://github.com/varundubey2804)

---

<div align="center">

*If JSO helped you — or your client — land that dream job, drop a ⭐ on the repo!*

**Built with ❤️, Agentic Workflows, and way too many Boolean operators.**

</div>
