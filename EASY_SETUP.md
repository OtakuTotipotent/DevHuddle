# DevHuddle — Windows 11 Setup Guide

## 1. Scope

This guide is for running the supplied DevHuddle source on Windows 11 for local development, FYP demonstration, and partner collaboration.

### Audited project stack

- Python / Django 6.0.6
- Django Channels 4.3.2
- Daphne 4.2.2
- SQLite3
- Tailwind CSS 4.3.1
- Vanilla JavaScript
- Google Gemini API
- Stripe Checkout
- Gmail SMTP
- Node.js + npm

---

# 2. Important security warning before sharing the ZIP

The supplied archive contains:

```text
.env
db.sqlite3
media/
```

The `.gitignore` correctly lists these as local/private files, but they are nevertheless present in the ZIP you supplied.

### Before giving the ZIP to anyone else:

- remove `.env`;
- remove `db.sqlite3` unless the evaluator explicitly requires the demo database;
- remove private `media/` content where appropriate;
- remove `__pycache__/` folders;
- provide `.env.example` instead.

The repository's `settings.py` also contains a hard-coded Django `SECRET_KEY`. Treat this as a credential/security issue and replace it with an environment-loaded key before any public sharing or deployment.

If a real secret has already been exposed to an untrusted person or public repository, **rotate/revoke it**, do not merely delete the file.

---

# 3. Recommended clean submission package

Create:

```text
DevHuddle/
├── config/
├── users/
├── feed/
├── intelligence/
├── communication/
├── templates/
├── static/
├── manage.py
├── requirements.txt
├── package.json
├── package-lock.json
├── .env.example
├── README.md
├── NOTES.md
├── SETUP.md
├── DOCUMENTATION.md
└── PROFESSION.md
```

Do not include:

```text
.env
db.sqlite3
__pycache__/
*.pyc
node_modules/
personal uploaded media/
local logs/
```

Whether `db.sqlite3` and sample media should be included in the official university submission depends on the university's submission policy. For a clean software handoff, source + migrations + environment template is normally safer.

---

# 4. Prerequisites on Windows 11

Install:

- Python supported by the pinned Django version;
- Node.js and npm;
- Git;
- VS Code.

Verify:

```powershell
python --version
pip --version
node --version
npm --version
git --version
```

Use a Python version supported by the Django release pinned in `requirements.txt`.

---

# 5. Get the project

From a terminal:

```powershell
git clone <YOUR-REPOSITORY-URL>
cd DevHuddle
```

For a ZIP:

```powershell
Expand-Archive .\DevHuddle.zip -DestinationPath .
cd .\DevHuddle
```

Make sure you are inside the folder containing:

```text
manage.py
requirements.txt
package.json
```

---

# 6. Create Python virtual environment

Recommended:

```powershell
py -m venv .venv
```

Activate:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution for your current user, you can use Command Prompt:

```cmd
.venv\Scripts\activate.bat
```

Verify:

```powershell
python --version
where.exe python
```

The Python path should point into `.venv`.

---

# 7. Upgrade pip

```powershell
python -m pip install --upgrade pip
```

---

# 8. Install backend dependencies

```powershell
pip install -r requirements.txt
```

This installs Django, Channels, Daphne, Pillow, Gemini, Stripe, formatting/linting tools, and their dependencies.

---

# 9. Install frontend dependencies

```powershell
npm install
```

Do not manually create `node_modules`.

`npm install` uses `package.json` and `package-lock.json`.

---

# 10. Configure environment

Copy the example:

```powershell
Copy-Item .env.example .env
```

The current `.env.example` includes Gemini and email variables.

The settings file also supports Stripe variables. Add them to your local `.env`:

```dotenv
GEMINI_API_KEY=your_key
EMAIL_HOST_USER=your_email
EMAIL_HOST_PASSWORD=your_gmail_app_password

STRIPE_PUBLIC_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...
```

### Do not commit `.env`.

Never paste real secrets into:

- GitHub issues;
- presentation slides;
- screenshots;
- Zoom chat;
- README files;
- public source code.

---

# 11. Database setup

For a clean environment:

```powershell
python manage.py makemigrations
python manage.py migrate
```

Because the project already contains migrations, `migrate` is the important command for applying them.

### Do not routinely run `makemigrations` just because you are starting the project.

Use it after changing model definitions.

For an untouched checkout:

```powershell
python manage.py migrate
```

is normally sufficient.

---

# 12. Create an admin user

```powershell
python manage.py createsuperuser
```

Follow the prompts.

Then admin should be reachable at:

```text
http://127.0.0.1:8000/admin/
```

---

# 13. Start Tailwind

Open Terminal 1:

```powershell
npm run tailwind
```

This watches:

```text
static/css/input.css
```

and compiles:

```text
static/css/output.css
```

Do not close this terminal while changing Tailwind-driven templates.

---

# 14. Start Django / ASGI development server

Open Terminal 2.

Activate the virtual environment again if needed:

```powershell
.\.venv\Scripts\Activate.ps1
```

Then:

```powershell
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

---

# 15. Run the Django deployment/security check

For production-oriented review:

```powershell
python manage.py check --deploy
```

For normal development:

```powershell
python manage.py check
```

### Note about this supplied ZIP audit

The isolated audit environment used for this documentation did not have Django installed, so `python manage.py check` could not be executed there. Python bytecode compilation with `python -m compileall` completed successfully.

That means:

- Python syntax compilation was checked;
- full Django runtime validation still needs to be performed on a machine with the project dependencies installed.

---

# 16. If the Tailwind command fails

Check:

```powershell
node --version
npm --version
```

Then:

```powershell
npm install
```

Confirm `package.json` contains the `tailwind` script.

If `node_modules` is corrupted:

```powershell
Remove-Item -Recurse -Force .\node_modules
npm ci
```

`npm ci` is preferable when you want an install based exactly on the lockfile.

---

# 17. If Django cannot start

Check:

```powershell
python --version
python -m pip show Django
```

If Django is missing:

```powershell
pip install -r requirements.txt
```

Check your current folder:

```powershell
dir
```

You must see `manage.py`.

---

# 18. If environment-variable errors occur

Common examples:

```text
GEMINI_API_KEY
EMAIL_HOST_USER
EMAIL_HOST_PASSWORD
```

Check that `.env` exists:

```powershell
Test-Path .\.env
```

Check variable names carefully.

Do not print secret values to the terminal during screen sharing.

---

# 19. AI feature setup

You need a valid Gemini API key in `.env`:

```dotenv
GEMINI_API_KEY=...
```

Then test:

1. log in;
2. open a profile;
3. trigger profile analysis;
4. open an AI report;
5. test post analysis.

### Before presentation

Verify the model names configured in:

```text
intelligence/services.py
```

The current code uses:

```text
gemini-3.5-flash
gemini-2.5-flash
```

External AI model names and availability can change, so do not discover a model failure for the first time during the FYP presentation.

---

# 20. Stripe setup

Use Stripe **test mode** for demonstrations.

Configure local `.env` values:

```dotenv
STRIPE_PUBLIC_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...
```

Then:

1. log in;
2. open Store;
3. select a product;
4. confirm redirect to Stripe Checkout;
5. use a Stripe test payment method;
6. return to the success URL;
7. verify premium/boost state.

Do not use live payment credentials for a classroom demonstration.

---

# 21. Email setup

The project is configured for Gmail SMTP.

Current settings include:

```text
smtp.gmail.com
port 587
TLS enabled
```

Use a dedicated email/account setup and an app password rather than exposing your normal Gmail password.

---

# 22. WebSocket testing

DevHuddle has:

```text
/ws/chat/<username>/
/ws/notifications/
```

Test with two browser sessions.

Recommended:

```text
Browser A = Developer
Browser B = Client
```

Send a message from A to B.

Verify:

- message appears live;
- notification appears;
- unread indicator changes;
- opening the inbox works.

### Why two users?

A real-time multi-user feature is hard to demonstrate convincingly with one account.

---

# 23. Production vs FYP environment

### FYP/demo

Acceptable choices include:

- SQLite;
- local media;
- development server;
- in-memory Channels layer;
- Stripe test mode.

### Production

Plan to move toward:

- PostgreSQL;
- Redis/shared channel layer;
- real deployment ASGI server;
- HTTPS;
- `DEBUG=False`;
- strict `ALLOWED_HOSTS`;
- environment-managed secrets;
- backups;
- logging;
- monitoring;
- automated tests;
- payment webhooks/idempotency;
- managed media/object storage;
- CI/CD.

---

# 24. Clean collaboration workflow for Afnan + Saad

Use Git as the source of truth.

Recommended branches:

```text
main
develop
feature/...
fix/...
docs/...
```

### Daily workflow

```text
git pull
  |
create/update branch
  |
make small changes
  |
git add
  |
git commit
  |
git push
  |
Pull Request / review
  |
merge
```

### Commit examples

Good:

```text
feat: add proposal submission flow
fix: prevent duplicate job applications
fix: validate uploaded image size
docs: add FYP setup guide
refactor: isolate Gemini service facade
```

Bad:

```text
changes
final
final2
working
new
important
```

---

# 25. Zoom workflow

### Afnan's screen

Keep only these visible:

1. VS Code.
2. Terminal.
3. Browser.
4. Notes/documentation.

### Never screen-share:

- `.env`;
- password manager;
- private email;
- API dashboard with secrets visible;
- personal files;
- browser tabs containing private information.

### Recommended rehearsal structure

```text
10 min — architecture
15 min — feature tour
15 min — code explanation
15 min — examiner questions
10 min — demo failure drills
```

Record at least one complete rehearsal locally if permitted by all participants.

---

# 26. Backup strategy

Before final submission:

```text
Backup A = Git repository
Backup B = clean ZIP
Backup C = external drive
Backup D = trusted cloud storage
```

Also keep:

- screenshots;
- presentation PDF;
- demo data notes;
- environment variable template;
- installation instructions;
- database migration files.

---

# 27. Final smoke test

Run this before every important demo:

```text
[ ] Server starts
[ ] Home page loads
[ ] Login works
[ ] Signup works
[ ] Profile works
[ ] Huddle creation works
[ ] Like works
[ ] Comment works
[ ] Bookmark works
[ ] Follow works
[ ] Search works
[ ] Job creation works
[ ] Proposal submission works
[ ] Client dashboard works
[ ] Proposal accept/reject works
[ ] Chat works
[ ] Live notification works
[ ] AI profile analysis works
[ ] AI post analysis works
[ ] Stripe test checkout works
[ ] Moderation works
[ ] Account deletion flow is explainable
```

---

# 28. Disaster recovery for the presentation

Have screenshots or a short recording of:

- homepage;
- developer profile;
- developer directory;
- job;
- proposal;
- chat;
- notification;
- AI report;
- Stripe checkout;
- moderation dashboard.

This does not replace a live demonstration. It is a backup against:

- internet failure;
- Gemini API outage;
- Stripe issue;
- local configuration error;
- projector/browser problems.
