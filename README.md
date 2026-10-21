# Cars Dealership Full-Stack Capstone Web Application

![CI/CD Pipeline](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-blue?logo=githubactions)
![Django](https://img.shields.io/badge/Django-5.1%20LTS-092E20?logo=django)
![DRF](https://img.shields.io/badge/Django_REST-Framework-red)
![React](https://img.shields.io/badge/React-18-61DAFB?logo=react)
![Vite](https://img.shields.io/badge/Vite-5-646CFF?logo=vite)
![Python](https://img.shields.io/badge/Python-3.13-3776AB?logo=python)
![License](https://img.shields.io/badge/License-MIT-green)

A comprehensive, production-grade automotive dealership platform built for the **Full-Stack Development Capstone Project**. The platform enables customers to discover certified dealerships across the United States, filter branches by state (including Kansas), view detailed dealer inventory, read customer feedback, submit verified reviews, and benefit from real-time natural language sentiment analysis.

---

## 🚀 Key Features

1. **Nationwide Dealership Directory**: Search and filter certified dealerships across multiple US states (Kansas, California, Texas, New York, Florida, Illinois, Washington, Colorado).
2. **State-Level Filtering**: High-performance backend filtering for states including `Kansas` with case-insensitive query support (`/api/dealers/?state=Kansas`).
3. **Vehicle Inventory & Makes**: Integration of car manufacturers (Toyota, Ford, Honda, Chevrolet, Tesla, BMW, Audi, Hyundai) and associated models (Sedans, SUVs, Trucks, EVs).
4. **Verified Customer Reviews**: Secure review submission system with dealer binding, purchase confirmation, and database persistence.
5. **Deterministic Sentiment Analysis**: Integrated natural language sentiment scoring pipeline evaluating review text (such as `"Fantastic services"` with reproducible positive classification and compound score).
6. **Authentication & Session Security**: Secure user registration with 5 required fields, Django password hashing, persistent session management, and CSRF protection.
7. **Administrative Management**: Configured Django Admin portal for managing Dealers, Reviews, Car Makes, and Car Models.
8. **DevOps & Containerization**: Multi-stage production `Dockerfile`, `docker-compose.yml`, Kubernetes manifests (`k8s/`), and automated GitHub Actions CI/CD workflow.

---

## 📁 Project Directory Structure

```text
cars-dealership-capstone/
├── README.md                           # Master Project Documentation & Quickstart
├── .gitignore                          # Git Ignore Rules for Python, Node, & Secrets
├── .env.example                        # Environment Configuration Template
├── requirements.txt                    # Pinned Python Dependencies
├── manage.py                           # Django CLI Management Utility
├── server/                             # Django Backend Application Root
│   ├── config/                         # Core Project Configuration & URL Routing
│   │   ├── settings.py                 # Application Settings, Middleware, CORS
│   │   ├── urls.py                     # API Routing & Static Page Handlers
│   │   ├── auth_views.py               # Register, Login, Logout, Session Handlers
│   │   ├── static_views.py             # About, Contact, and Frontend Asset Servicing
│   │   ├── wsgi.py                     # WSGI Production Entrypoint
│   │   └── asgi.py                     # ASGI Production Entrypoint
│   ├── dealerships/                    # Dealerships & Car Inventory App
│   │   ├── models.py                   # Dealer, CarMake, CarModel Models
│   │   ├── serializers.py              # DRF Model Serializers
│   │   ├── views.py                    # List, Detail, State Filter Views
│   │   ├── urls.py                     # Dealership Endpoints
│   │   └── admin.py                    # Django Admin Model Registrations
│   ├── reviews/                        # Customer Reviews & Rating App
│   │   ├── models.py                   # Review Model with Sentiment Fields
│   │   ├── serializers.py              # Review Serializers
│   │   ├── views.py                    # Review Retrieval & Authenticated Submission
│   │   ├── urls.py                     # Review API Routing
│   │   └── admin.py                    # Review Admin Interface
│   ├── sentiment/                      # Sentiment Analysis App
│   │   ├── services.py                 # VADER Sentiment & Lexical Fallback Analyzer
│   │   ├── views.py                    # POST /api/analyze-review/
│   │   └── urls.py                     # Sentiment Routing
│   ├── frontend/                       # Graded Static HTML & React Deliverables
│   │   ├── static/
│   │   │   ├── About.html              # Task 3: Responsive About Us Page
│   │   │   ├── Contact.html            # Task 4: Responsive Contact Us Page
│   │   │   └── style.css               # Shared Static Stylesheet
│   │   └── src/
│   │       └── components/
│   │           └── Register/
│   │               ├── Register.jsx    # Task 7: 5-Field React Registration Component
│   │               └── Register.css    # Registration Component Styling
│   └── tests/
│       └── test_full_stack.py          # 19 Automated Backend Integration Tests
├── frontend/                           # Production React Single-Page Application (Vite)
│   ├── package.json                    # Node.js Dependencies & Build Scripts
│   ├── vite.config.js                  # Vite Config with Backend Proxy
│   ├── index.html                      # HTML5 Entrypoint with Meta & Fonts
│   └── src/
│       ├── App.jsx                     # Root React Application & State
│       ├── main.jsx                    # React 18 DOM Render Root
│       ├── index.css                   # Glassmorphic Design System Tokens
│       └── components/
│           ├── Navbar/                 # Brand Logo, Navigation, User Menu
│           ├── DealerList/             # Search, State Filter, Dealer Cards
│           ├── DealerDetail/           # Dealer Header, Vehicles, Reviews List
│           ├── ReviewForm/             # Review Submission with Sentiment Preview
│           ├── LoginModal/             # Interactive Authentication Modal
│           └── Register/               # User Registration Form
├── scripts/
│   ├── seed_data.py                    # Automated Database Seeding Script
│   ├── generate_curl_evidence.py       # API Evidence Extraction Script
│   ├── capture_screenshots.py          # Automated Browser Screenshot Capture
│   └── deploy_ibm_cloud.sh             # IBM Cloud Code Engine Deployment Automation
├── submission_evidence/
│   ├── commands/                       # 11 Verified cURL Command Output Files
│   └── screenshots/                    # 8 Verified High-Resolution PNG Screenshots
├── .github/
│   └── workflows/
│       └── ci.yml                      # GitHub Actions Automated CI/CD Pipeline
├── Dockerfile                          # Multi-Stage Production Containerfile
├── docker-compose.yml                  # Local Container Orchestration Config
├── k8s/
│   └── deployment.yaml                 # Kubernetes Deployment, Service, Ingress
├── SUBMISSION_AUDIT.md                 # 28-Task Assessment Audit & Verification Matrix
├── FINAL_SUBMISSION_GUIDE.md           # Step-by-Step Assignment Submission Guide
└── FINAL_QA_REPORT.md                  # Quality Assurance & Verification Report
```

---

## 🛠️ Technology Stack

| Layer | Technologies |
|---|---|
| **Backend Framework** | Python 3.13 / 3.11, Django 5.1 LTS, Django REST Framework |
| **Authentication** | Django Session Authentication, PBKDF2 Password Hashing |
| **Database** | SQLite (development/local) with Django ORM & Migrations |
| **Frontend Framework** | React 18, Vite 5, Modern Vanilla CSS Design System |
| **Natural Language Processing** | VADER Sentiment Analyzer with Deterministic Lexical Fallback |
| **Testing** | Django Test Framework, Playwright Browser Automation |
| **DevOps & Containers** | Docker (Multi-stage build), Docker Compose, Kubernetes |
| **CI/CD** | GitHub Actions Automated Test & Build Workflow |

---

## ⚙️ Local Development Setup

### 1. Prerequisites
- **Python 3.11+** installed
- **Node.js 18+** and npm installed
- **Git** installed

### 2. Clone and Setup Environment
```bash
git clone <YOUR_REPOSITORY_URL>
cd "Full Stack project"

# Create Python virtual environment
python -m venv .venv

# Activate virtual environment
# Windows PowerShell:
.\.venv\Scripts\Activate.ps1
# macOS / Linux:
source .venv/bin/activate

# Install backend dependencies
pip install -r requirements.txt

# Copy environment variables
cp .env.example .env
```

### 3. Initialize Database and Seed Data
```bash
# Apply database migrations
python manage.py migrate

# Seed realistic dealerships, car makes, models, reviews, and test accounts
python manage.py seed_dealerships
```

### 4. Build React Frontend
```bash
cd frontend
npm install
npm run build
cd ..
```

### 5. Start Application Server
```bash
python manage.py runserver 127.0.0.1:8000
```
Visit **http://127.0.0.1:8000/** to view the live full-stack application!

---

## 🔐 Demonstration Credentials

| Role | Username | Password | Email | Purpose |
|---|---|---|---|---|
| **Administrator** | `admin` | `AdminSecurePassword123!` | `admin@dealerships.example.com` | Django Admin Portal (`/admin/`) |
| **Test User** | `testuser` | `TestUserPassword123!` | `testuser@dealerships.example.com` | Frontend login & review submission |

---

## 📡 Backend REST API Reference

| Method | Endpoint | Description | Status Code |
|---|---|---|---|
| `POST` | `/api/auth/register/` | Register new user (5 fields: username, first_name, last_name, email, password) | `201 Created` |
| `POST` | `/api/auth/login/` | Authenticate user credentials and start session | `200 OK` |
| `POST` | `/api/auth/logout/` | Terminate user session | `200 OK` |
| `GET` | `/api/auth/me/` | Retrieve current authenticated user details | `200 OK` |
| `GET` | `/api/dealers/` | Retrieve all nationwide dealerships | `200 OK` |
| `GET` | `/api/dealers/{id}/` | Retrieve specific dealership details by ID | `200 OK` |
| `GET` | `/api/dealers/?state=Kansas` | Filter dealerships by state (Kansas) | `200 OK` |
| `GET` | `/api/dealers/{id}/reviews/` | Retrieve customer reviews for dealership | `200 OK` |
| `POST` | `/api/dealers/{id}/reviews/` | Submit new review for dealership (Authenticated) | `201 Created` |
| `GET` | `/api/car-makes/` | Retrieve car manufacturers and models | `200 OK` |
| `POST` | `/api/analyze-review/` | Deterministic review sentiment analysis | `200 OK` |

---

## 🧪 Automated Testing

Execute the complete 19-test automated test suite:
```bash
python manage.py test server.tests
```
**Test Results:**
```text
Creating test database for alias 'default'...
Found 19 test(s).
System check identified no issues (0 silenced).
...................
----------------------------------------------------------------------
Ran 19 tests in 32.273s

OK
Destroying test database for alias 'default'...
```

---

## 🐳 Docker and Kubernetes

### Run with Docker Compose:
```bash
docker-compose up --build
```
Access at `http://localhost:8000/`.

### Deploy to Kubernetes:
```bash
kubectl apply -f k8s/deployment.yaml
```

---

## 📄 License
This project is licensed under the MIT License for educational and demonstration purposes.
