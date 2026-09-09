# How to setup DevHuddle locally

## Environment & Configuration

### Environment Variables (`.env`)

```env
# AI
GEMINI_API_KEY=your_gemini_api_key

# Email (Gmail SMTP)
EMAIL_HOST_USER=your_host_email_address
EMAIL_HOST_PASSWORD=your_host_email_app_password

# Stripe (optional defaults in settings)
STRIPE_PUBLIC_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...
```

## Installation & Setup

### Prerequisites

- Python 3.x
- Node.js & npm
- Git

### Step-by-Step Setup

```bash
# 1. Clone repository
git clone https://github.com/OtakuTotipotent/DevHuddle.git
cd DevHuddle

# 2. Create and activate virtual environment
python -m venv .venv
.venv\Scripts\Activate        # Windows
# source .venv/bin/activate   # Linux/Mac

# 3. Install Python dependencies
pip install -r requirements.txt

# 4. Install frontend dependencies
npm install

# 5. Configure environment
cp .env.example .env
# Edit .env with your API keys

# 6. Run database migrations
python manage.py makemigrations
python manage.py migrate

# 7. Create admin superuser
python manage.py createsuperuser

# 8. Start Tailwind CSS watcher (separate terminal)
npm run tailwind

# 9. Start development server
python manage.py runserver
```

### VS Code Extensions (Recommended)

- djLint — Django template linting
- Python Extension Pack
- TailwindCSS IntelliSense
- Django extension
