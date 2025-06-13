# Anime Trading Social Media Platform – Local Development Plan

## 1. Overview

Create a personal full-stack web app for trading anime items (merchandise, manga, collectibles) with social features (profiles, reviews, messaging). The goal is to learn frontend (React), backend (Django + DRF), and APIs on a small scale with **local development** focus.

## 2. Objectives

- **Learning Focus**: Build core CRUD flows, user authentication, and local development workflows.
- **MVP Scope**: Essential trading marketplace and user profiles with infinite scrolling feeds. Leave real-time chat, notifications, and admin dashboard for later.
- **Best Practices**: Use version control, environment management, basic testing, and local development best practices.

## 3. Tech Stack

- **Frontend**: React with Axios, `react-infinite-scroll-component` for feeds, `react-router-dom` for routing.
- **Backend**: Django + Django REST Framework (DRF).
- **Database**: PostgreSQL (local installation for production-like development).
- **Media Storage**: Local file storage with Django's `MEDIA_ROOT` and `MEDIA_URL`.
- **Auth**: DjangoSimpleJWT for JWT-based authentication.
- **Optional Future**: Django Channels for real-time chat.
- **Version Control**: Git + GitHub.
- **Testing**: Django Test Framework + pytest (backend), Jest + React Testing Library (frontend).
- **Development**: Local development servers (Django dev server + React dev server).
- **Env Management**: python-decouple (backend), `.env` (frontend).

## 4. Core Features (MVP)

1. **Authentication & User Management**
    - Sign up and login with JWT (`LoginPage`, `SignupPage`).
    - Password reset and email verification (optional).
2. **Marketplace**
    - **List & View**: Browse all trade items on `MarketplacePage` with infinite scrolling (no numbered pagination buttons), search, and category filters; view details on `TradeDetailsPage`.
    - **Create & Manage**: Post new trade offers, update, or delete own offers via `TradeForm`.
    - **Trade Item Model**: title, description, image upload (local storage), interests, status (Available/Traded), owner, timestamps.
3. **User Profiles**
    - Display avatar, bio, favorite genres, listed items (infinite scrolling feed), wishlist, and reviews on `ProfilePage`.
    - Wishlist: Add/remove items via buttons on `TradeItemCard`.
    - Reviews: Rate other users (1–5 stars) with comments, displayed on `ProfilePage`.

## 5. Secondary Features (Phase 2+)

- Real-time or REST-based messaging between users.
- Notifications for new messages or trade proposals.
- Admin dashboard for user/report moderation.
- Reputation badges or system.

## 6. Local Development Setup

### Prerequisites

- Python 3.8+ and pip
- Node.js 16+ and npm/yarn
- Git

### Backend Setup

```bash
# Create virtual environment
python -m venv anime_market_env
source anime_market_env/bin/activate  # On Windows: anime_market_env\Scripts\activate

# Install Django and dependencies
pip install django djangorestframework django-cors-headers python-decouple djangorestframework-simplejwt Pillow psycopg2-binary

# Create PostgreSQL database
createdb anime_market_db  # or use pgAdmin/psql

# Create Django project
django-admin startproject anime_market_backend
cd anime_market_backend
python manage.py startapp market_api

# Run migrations and create superuser
python manage.py migrate
python manage.py createsuperuser

# Start development server
python manage.py runserver  # Runs on http://localhost:8000

```

### Frontend Setup

```bash
# Create React app
npx create-react-app anime-market-frontend
cd anime-market-frontend

# Install dependencies
npm install axios react-router-dom react-infinite-scroll-component

# Start development server
npm start  # Runs on http://localhost:3000

```

## 7. Folder Structure

### Frontend (`anime-market-frontend/`)

```
public/
  ├ index.html
  └ favicon.ico
src/
  ├ api.js                   # Axios config with base URL (http://localhost:8000)
  ├ App.jsx                 # Main app with routes
  ├ index.jsx               # Entry point
  ├ assets/                 # Images, fonts (if needed)
  ├ components/             # Reusable components
  │   ├ Header.jsx          # Navigation bar
  │   ├ TradeItemCard.jsx   # Item card for feeds
  │   ├ TradeForm.jsx       # Form for creating/editing items
  │   ├ ProfileCard.jsx     # User profile summary
  │   ├ ReviewCard.jsx      # Review display
  │   └ LoadingSpinner.jsx  # Spinner for infinite scroll
  ├ pages/                  # Page components
  │   ├ HomePage.jsx        # Landing page with featured items
  │   ├ MarketplacePage.jsx # Infinite scrolling feed with filters
  │   ├ TradeDetailsPage.jsx# Item details and actions
  │   ├ ProfilePage.jsx     # User profile, items, wishlist, reviews
  │   ├ LoginPage.jsx       # Login form
  │   └ SignupPage.jsx      # Signup form
  ├ styles/                 # Global and component-specific CSS
  │   ├ App.css
  │   └ components/
  └ utils/                  # Helper functions
      └ auth.js             # JWT token management
.env                        # REACT_APP_API_BASE_URL=http://localhost:8000
package.json
README.md

```

### Backend (`anime-market-backend/`)

```
anime_market/      # Django project settings
  ├ settings.py
  ├ urls.py
market_api/        # Core app
  ├ models.py
  ├ serializers.py
  ├ views.py
  ├ urls.py
  ├ permissions.py  # Owner-only updates, etc.
  └ tests/          # pytest + Django tests
media/             # Local media files (images)
  └ uploads/
    ├ profiles/
    └ trade_items/
static/            # Static files (CSS, JS if needed)
manage.py
.env               # SECRET_KEY, DEBUG=True, ALLOWED_HOSTS=localhost,127.0.0.1
requirements.txt   # pip freeze > requirements.txt

```

## 8. Data Models (`market_api/models.py`)

- **TradeItem**: title, description, image (ImageField with local storage), interests, status (Available/Traded), owner (ForeignKey to User), created_at.
- **UserProfile**: OneToOne with User, avatar (ImageField), bio, genres, wishlist (ManyToMany to TradeItem).
- **Review**: reviewer (ForeignKey to User), reviewee (ForeignKey to User), rating (1–5), comment, created_at.
- **(Optional)** Chat, ChatParticipant, Message models for future messaging.

## 9. Local Development Configuration

### Backend Settings (`settings.py`)

```python
import os
from decouple import config

# Basic settings
DEBUG = config('DEBUG', default=True, cast=bool)
SECRET_KEY = config('SECRET_KEY', default='your-secret-key-here')
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Database (PostgreSQL for local development)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME', default='anime_market_db'),
        'USER': config('DB_USER', default='your_username'),
        'PASSWORD': config('DB_PASSWORD', default='your_password'),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='5432'),
    }
}

# Media files (local storage)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Static files
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# CORS settings for React frontend
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

# DRF settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}

```

### Frontend API Configuration (`src/api.js`)

```jsx
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add JWT token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default api;

```

## 10. API Endpoints

| Method | Endpoint | Description | Auth |
| --- | --- | --- | --- |
| GET | `/api/items/` | List all trade items (paginated) | No |
| POST | `/api/items/` | Create trade item | Yes |
| GET | `/api/items/<id>/` | Retrieve specific item | No |
| PUT | `/api/items/<id>/` | Update (owner only) | Yes (owner) |
| DELETE | `/api/items/<id>/` | Delete (owner only) | Yes (owner) |
| POST | `/api/auth/register/` | User registration | No |
| POST | `/api/auth/login/` | Obtain JWT | No |
| GET | `/api/users/<id>/profile/` | View user profile | No |
| PUT | `/api/users/<id>/profile/` | Edit own profile | Yes (self) |
| GET | `/api/users/<id>/wishlist/` | View wishlist | No |
| POST | `/api/wishlist/<item_id>/add/` | Add to wishlist | Yes |
| DELETE | `/api/wishlist/<item_id>/remove/` | Remove from wishlist | Yes |
| POST | `/api/reviews/` | Submit review | Yes |
| GET | `/api/users/<id>/reviews/` | List user reviews | No |

## 11. Local Development Workflow

### Starting Development

```bash
# Terminal 1: Backend
cd anime-market-backend
source anime_market_env/bin/activate  # Activate virtual environment
python manage.py runserver

# Terminal 2: Frontend
cd anime-market-frontend
npm start

```

### Development URLs

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- Django Admin: http://localhost:8000/admin/
- API Browsable Interface: http://localhost:8000/api/

### File Upload Handling

- Images stored in `media/uploads/` directory
- Serve media files during development by adding to `urls.py`:

```python
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ... your URL patterns
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

```

## 12. Environment Files

### Backend `.env`

```
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DB_NAME=anime_market_db
DB_USER=your_postgres_username
DB_PASSWORD=your_postgres_password
DB_HOST=localhost
DB_PORT=5432

```

### Frontend `.env`

```
REACT_APP_API_BASE_URL=http://localhost:8000

```

## 13. Testing & Quality

- **Backend**: Unit tests for models, serializers, views (pytest, Django Test Framework).
- **Frontend**: Unit tests for components and API integration (Jest, React Testing Library).
- **Local Testing**: Use Django's test database and React's test environment.
- **Test Data**: Create fixtures or use Django's management commands to populate test data.

## 14. Version Control

### Git Setup

```bash
# Initialize repositories
git init anime-market-frontend
git init anime-market-backend

# Create .gitignore files
# Backend: Include db.sqlite3, media/, __pycache__/, .env
# Frontend: Include node_modules/, build/, .env

```

### Recommended `.gitignore` files

**Backend:**

```
*.pyc
__pycache__/
.env
media/
venv/
anime_market_env/

```

**Frontend:**

```
node_modules/
build/
.env
.env.local
.env.development.local
.env.test.local
.env.production.local

```

## 15. Timeline Summary (4–6 Weeks for Local Development)

- **Week 1**: Setup local environment, create basic models and auth pages
- **Weeks 2–3**: Build marketplace feed, item details, and backend API endpoints
- **Weeks 4–5**: Implement profile pages, trade forms, and complete CRUD operations
- **Week 6**: Testing, polish, and documentation

## 16. Next Steps

1. Set up local development environment
2. Create virtual environment and install dependencies
3. Initialize Django project and React app
4. Set up basic models and authentication
5. Create simple login/signup pages
6. Build basic marketplace functionality

## 17. Benefits of Local Development

- **Faster iteration**: No deployment delays
- **Easier debugging**: Direct access to logs and databases
- **Cost-effective**: No hosting costs during development
- **Learning focused**: Concentrate on code rather than deployment issues
- **Database access**: Easy to inspect and modify SQLite database
- **File uploads**: Simple local file storage without cloud configuration

## 18. Future Migration to Production

When ready to deploy:

- Switch from SQLite to PostgreSQL
- Move from local file storage to cloud storage (Cloudinary)
- Update environment variables for production
- Configure production hosting (Vercel, Heroku, etc.)
- Set up CI/CD pipeline
