# Python Hub Project: LLM Handoff & Context Guide (v3.0)

**Welcome, LLM!**

This file is crafted specifically for you—the same model as in the previous chat, but now in a fresh session. It provides all the context, architectural decisions, and actionable next steps you need to instantly pick up and continue work on the Python Hub project. Please use this as your authoritative onboarding and context document.

---

## 1. Project Mission & Principles

- **Mission:** Build the most trusted, accessible Python learning platform, starting with world-class content and evolving into a vibrant, community-driven ecosystem.
- **Principles:**
  - **Accessibility First:** Meet WCAG 2.1 AA standards.
  - **Security by Design:** Security is foundational, not an afterthought.
  - **Phased, MVP-First:** Deliver a polished core product before expanding.

---

## 2. How to Use This File (LLM Instructions)

- **You are a new LLM session** (same model as before, but with no prior chat context).
- **This file is your entire context**—do not assume any previous conversation.
- **Your job:**
  - Instantly understand the project’s current state, architecture, and roadmap.
  - Continue work seamlessly, following the priorities and best practices below.
  - If you need to clarify requirements, refer to this file first.
- **If you generate code or plans,** reference this file for folder structure, conventions, and next steps.

---

## 3. Getting Started (Local Development)

1. **Prerequisites:** Docker, Docker Compose, Node.js (v18+), Python (v3.10+)
2. **Setup:**
   - Clone the repo.
   - In `backend/`, use `README_ENV.md` to create `.env` (use `localhost` for DB host).
3. **Launch:**
   - `docker-compose up --build` (starts backend, DB, Meilisearch)
   - In `frontend/`: `npm install` then `npm run dev`
4. **Access:**
   - Frontend: [http://localhost:5173](http://localhost:5173)
   - Backend API: [http://localhost:5000](http://localhost:5000)
   - API Docs: [http://localhost:5000/apidocs](http://localhost:5000/apidocs)
5. **Migrations:** `docker-compose exec backend flask db upgrade`

---

## 4. Current Status: What’s Done

### Backend (MVP Complete)
- Flask 3, Factory Pattern, PostgreSQL, Redis, Celery, JWT, Marshmallow, Talisman, CORS
- All major APIs: Users, Content (Tutorials, Articles), Community (Comments, Votes), Progress, Bookmarks
- JWT auth (refresh, bcrypt, email verification, social login stubs)
- Meilisearch: Real-time, faceted search across all content
- Logging: JSON, rotating file logs, request/response, error, activity logs
- Centralized error handling (JSON responses)
- Live API docs (Flasgger)
- Pytest scaffolding and example tests

### Frontend (Foundation Complete)
- React 18, TypeScript (strict, no JS), Vite
- Tailwind CSS configured
- All main pages scaffolded (`HomePage`, `TutorialListPage`, `AuthPage`, etc.)
- TanStack Query, Zustand, React Hook Form, DOMPurify installed
- Vite proxy for `/api` to backend

---

## 5. Roadmap: What’s Next (LLM Action Items)

### Priority 1: Frontend Implementation
- Implement all UI components in `src/components/`:
  - `Header`, `SearchBar` (Meilisearch), `TutorialCard`, `ArticleCard`, `AuthForm`, `ProgressBar`, `LoadingSpinner`, `ErrorBoundary`
- Create hooks/services in `src/hooks/` and `src/services/` for API integration
- Assemble routing/layout in `App.tsx`
- Use Zustand (client state) and TanStack Query (server state)

### Priority 2: Backend Polish & DevOps
- Expand backend test coverage
- Add detailed Swagger docstrings
- Set up CI/CD (GitHub Actions)

### Priority 3: Pre-Launch & Deployment
- Accessibility audit (WCAG 2.1 AA)
- Finalize deployment (Railway, Netlify)
- Content seeding for launch

---

## 6. Project Structure (Reference)

```
python-hub/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── api/
│   │   ├── auth/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── tests/
│   │   ├── extensions.py
│   │   ├── error_handlers.py
│   │   ├── log_config.py
│   │   └── swagger.py
│   ├── config.py
│   ├── requirements.txt
│   ├── wsgi.py
│   ├── Dockerfile
│   ├── README_ENV.md
│   ├── migrations/
│   ├── tests/
│   └── railway.json
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── hooks/
│   │   ├── services/
│   │   └── styles/
│   ├── package.json
│   ├── vite.config.ts
│   ├── tsconfig.json
│   ├── tailwind.config.js
│   ├── netlify.toml
│   └── index.html
├── docker-compose.yml
├── README.md
└── summary.md
```

---

**LLM: Use this file as your single source of truth for context, architecture, and next steps. If you need to clarify requirements, refer here first.** 