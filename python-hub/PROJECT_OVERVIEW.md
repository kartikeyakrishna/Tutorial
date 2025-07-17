# PROJECT_OVERVIEW.md

## 1. Project Vision & Core Principles

**Mission:**
> To create a high-quality, accessible Python learning platform that empowers users of all backgrounds to master Python through interactive content and a vibrant community.

**Guiding Principles:**
- **Accessibility First:** The platform is designed to meet WCAG 2.1 AA standards, ensuring usability for everyone, including those with disabilities.
- **Security by Design:** Security is integrated at every layer, from the database to the frontend, not added as an afterthought.
- **Phased, MVP-First Rollout:** The project follows a strategic, phased approach—delivering a polished, high-quality core product before expanding to advanced features.

---

## 2. Architecture Overview

| Layer         | Technology Stack                                                                 |
|--------------|----------------------------------------------------------------------------------|
| **Backend**  | Flask 3 (Factory Pattern), PostgreSQL (SQLAlchemy), Meilisearch, JWT Auth, Celery/Redis |
| **Frontend** | React 18 (TypeScript), Vite, Tailwind CSS, TanStack Query, Zustand                |
| **Infra/DevOps** | Docker Compose (local), Railway (backend hosting), Netlify (frontend hosting), GitHub Actions (CI/CD) |

---

## 3. Getting Started (Local Development Guide)

1. **Prerequisites:**
   - Docker & Docker Compose
   - Node.js (v18+)
   - Python (v3.10+)
2. **Environment Setup:**
   - Clone the repository.
   - In the `backend/` directory, copy the instructions from `README_ENV.md` to create a `.env` file and fill in your local configuration (use `localhost` for the database host).
3. **Launch Services:**
   - From the project root, run:
     ```sh
     docker-compose up --build
     ```
4. **Run Frontend:**
   - In a new terminal, navigate to `frontend/` and run:
     ```sh
     npm install
     npm run dev
     ```
5. **Access Points:**
   - **Frontend:** [http://localhost:5173](http://localhost:5173)
   - **Backend API:** [http://localhost:5000](http://localhost:5000)
   - **API Docs (Swagger):** [http://localhost:5000/apidocs](http://localhost:5000/apidocs)
6. **Database Migration:**
   - To apply the latest database schema, run:
     ```sh
     docker-compose exec backend flask db upgrade
     ```
   - This ensures your database is up to date with the latest models.

---

## 4. Current Project Status

### **Backend (Feature-Complete)**
- Flask 3 foundation using the Factory Pattern for scalability and maintainability.
- Comprehensive API endpoints for Users, Content (Tutorials, Articles, Code Snippets), Community (Comments, Votes), Progress Tracking, and Bookmarks.
- Production-ready JWT authentication (refresh tokens, bcrypt, email verification, social login stubs).
- Meilisearch integration for instant, faceted search across all content, with real-time indexing.
- Structured, rotating JSON logging for application monitoring and debugging.
- Centralized error handling with consistent JSON responses.
- Live, interactive API documentation via Flasgger (`/apidocs`).
- Pytest-based testing framework with example tests.

### **Frontend (Foundation Complete)**
- React 18 + TypeScript (strict mode, no JavaScript allowed), Vite for fast development.
- Tailwind CSS fully configured for rapid, accessible UI development.
- All primary pages scaffolded: `HomePage`, `TutorialListPage`, `TutorialDetailPage`, `ArticleListPage`, `ProfilePage`, `AuthPage`, `SearchPage`.
- State management and data fetching libraries (TanStack Query, Zustand, React Hook Form, DOMPurify) installed and ready.
- Vite dev server proxies `/api` requests to the backend for seamless integration.

---

## 5. Actionable Roadmap: Next Steps

### **Priority 1: Frontend Implementation**
- **Component Library:**
  - Build: `Header`, `SearchBar` (with Meilisearch logic), `TutorialCard`, `ArticleCard`, `AuthForm`, `ProgressBar`, `LoadingSpinner`, `ErrorBoundary`.
- **API Integration:**
  - Create custom hooks and services in `src/hooks/` and `src/services/` to connect to backend endpoints (auth, content, progress, search, etc.).
- **Routing & Layout:**
  - Assemble all components and pages in `App.tsx` using React Router v6.

### **Priority 2: Backend Polish & DevOps**
- **Expand Test Coverage:**
  - Write comprehensive unit and integration tests for all backend endpoints and services.
- **Enrich API Docs:**
  - Add detailed docstrings to all Flask endpoints for richer Swagger documentation.
- **CI/CD Pipeline:**
  - Set up GitHub Actions to run tests and linters on every push and pull request.

### **Priority 3: Pre-Launch & Deployment**
- **Accessibility Audit:**
  - Perform a full accessibility review to ensure WCAG 2.1 AA compliance.
- **Finalize Deployment:**
  - Prepare for production using `railway.json` (backend) and `netlify.toml` (frontend).
- **Content Seeding:**
  - Develop and implement a plan for initial high-quality tutorials and articles to populate the platform at launch.

---

**This document is your single source of truth for onboarding, context, and next steps. If you have questions or need to clarify requirements, refer here first!**

--- 