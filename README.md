# DevHuddle — Project Documentation

> **Social Media for Software Engineers**  
> A dual-sided, algorithmic marketplace connecting developers, clients, and organizations.

| Field | Value |
|-------|-------|
| **Project Name** | DevHuddle |
| **Type** | Full-stack Django Web Application |
| **Repository** | [github.com/OtakuTotipotent/DevHuddle](https://github.com/OtakuTotipotent/DevHuddle) |
| **Version** | 1.0.0 |
| **Timezone** | Asia/Karachi |
| **Status** | Under maintenance / active development |

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Problem Statement & Objectives](#2-problem-statement--objectives)
3. [Technology Stack](#3-technology-stack)
4. [System Architecture](#4-system-architecture)
5. [Project Structure](#5-project-structure)
6. [Features](#6-features)
7. [User Roles & Access Control (RBAC)](#7-user-roles--access-control-rbac)
8. [Database Schema](#8-database-schema)
9. [Pages & User Interface](#9-pages--user-interface)
10. [Theme & Design System](#10-theme--design-system)
11. [HTTP Routes & Endpoints](#11-http-routes--endpoints)
12. [AJAX & WebSocket APIs](#12-ajax--websocket-apis)
13. [Core Algorithms](#13-core-algorithms)
14. [AI Intelligence Module](#14-ai-intelligence-module)
15. [Monetization (Stripe)](#15-monetization-stripe)
16. [Real-Time Communication](#16-real-time-communication)
17. [Security Measures & Patches](#17-security-measures--patches)
18. [Signals & Background Tasks](#18-signals--background-tasks)
19. [Forms & Validation](#19-forms--validation)
20. [Environment & Configuration](#20-environment--configuration)
21. [Installation & Setup](#21-installation--setup)
22. [Testing Status](#22-testing-status)
23. [Known Limitations & Future Work](#23-known-limitations--future-work)

---

## Preview

![Homepage](./static/images/unauthorized.png/ "Unauthorized User Homepage view")
![Homepage](./static/images/homepage.png/ "Authorized User Homepage view")
![Homepage](./static/images/devs-directory.png/ "Developers Leaderboard view")
![Homepage](./static/images/messages.png/ "Inbox/Messenger view")
![Homepage](./static/images/notifications.png/ "Notifications view")
![Homepage](./static/images/profile.png/ "User Profile view")
![Homepage](./static/images/workspace.png/ "Clients view")
![Homepage](./static/images/dashboard.png/ "Dashboard view")
![Homepage](./static/images/subscriptions.png/ "Store/Subscriptions page view")
![Homepage](./static/images/mobile.png/ "Small Screen/Mobile Phone view")

## 1. Executive Summary

**DevHuddle** is a developer-centric social networking and job marketplace platform built as a Bachelor-level IT final-year project. It combines the social engagement patterns of platforms like LinkedIn and Twitter with a structured job/proposal workflow similar to freelance marketplaces.

The platform serves three distinct user personas:

- **Developers (`dev`)** — build portfolios, share technical huddles, apply to jobs, network, and rank on a leaderboard.
- **Clients (`client`)** — post job offers, review proposals, and hire talent.
- **Organizations (`org`)** — same capabilities as clients, representing companies or teams.

Key differentiators include:

- **Algorithmic Dev Score** — real-time developer ranking based on portfolio, engagement, and premium status.
- **Google Gemini AI integration** — automated profile analysis and post code review.
- **Real-time messaging & notifications** — powered by Django Channels and WebSockets.
- **Stripe monetization** — Pro subscriptions and profile boosts.
- **Community moderation** — user reporting and staff moderation dashboard.

---

## 2. Problem Statement & Objectives

### Problem Statement

Software engineers lack a dedicated platform that combines professional networking, portfolio showcasing, job discovery, and AI-assisted career insights in a single ecosystem. General-purpose social media does not cater to technical collaboration, and job boards lack community engagement features.

### Project Objectives

| # | Objective | Implementation |
|---|-----------|----------------|
| 1 | Build a role-based social platform for developers | Custom user model with `dev`, `client`, `org` roles |
| 2 | Enable job posting and proposal workflow | `Post` (job type) + `Proposal` model with accept/reject flow |
| 3 | Rank developers algorithmically | Dev Score formula with DB-level annotations |
| 4 | Provide real-time communication | Django Channels WebSocket consumers |
| 5 | Integrate Generative AI for career insights | Google Gemini via `intelligence` app |
| 6 | Monetize via subscriptions and boosts | Stripe Checkout Sessions |
| 7 | Ensure platform safety | Report system + staff moderation dashboard |
| 8 | Support account lifecycle management | 3-day deletion grace period with `sweep_accounts` command |

---

## 3. Technology Stack

### Backend

| Technology | Version | Purpose |
|------------|---------|---------|
| **Python** | 3.x | Runtime |
| **Django** | 6.0.6 | Web framework (MVT pattern) |
| **Django Channels** | 4.3.2 | WebSocket / ASGI support |
| **Daphne** | 4.2.2 | ASGI server |
| **SQLite3** | — | Relational database (development) |
| **django-environ** | 0.14.0 | Environment variable management |
| **Pillow** | 12.2.0 | Image upload processing |
| **Markdown** | 3.10.2 | Post body & AI report rendering |

### External Services

| Service | Package | Purpose |
|---------|---------|---------|
| **Google Gemini** | `google-genai` 2.10.0 | AI profile analysis & post review |
| **Stripe** | `stripe` 15.3.0 | Payment processing |
| **Gmail SMTP** | Django email backend | Password reset & account deletion emails |

### Frontend

| Technology | Version | Purpose |
|------------|---------|---------|
| **Django Templates** | — | Server-side HTML rendering |
| **Tailwind CSS** | 4.3.1 | Utility-first CSS framework |
| **Vanilla JavaScript** | — | AJAX interactions, WebSockets, UI toggles |
| **@tailwindcss/forms** | 0.5.11 | Form styling plugin |
| **@tailwindcss/typography** | 0.5.20 | Markdown prose styling |
| **@tailwindcss/aspect-ratio** | 0.4.2 | Responsive media ratios |

### Development Tools

| Tool | Purpose |
|------|---------|
| **black** 26.5.1 | Python code formatting |
| **djlint** 1.39.4 | Django template linting |
| **VS Code extensions** | djLint, Python, Django, TailwindCSS IntelliSense |

### Architecture Pattern

- **MVT (Model-View-Template)** — Django's standard pattern
- **Class-Based Views (CBVs)** — primary view layer (`ListView`, `CreateView`, `DetailView`, etc.)
- **Signal-driven side effects** — notifications, file cleanup, WebSocket broadcasts
- **Facade pattern** — `DevHuddleAIEngine` for AI service abstraction
- **No REST API** — server-rendered with selective JSON endpoints for AJAX

---

## 4. System Architecture

### High-Level Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                         CLIENT (Browser)                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────────┐  │
│  │ Django HTML  │  │  Tailwind    │  │  Vanilla JS (fetch/WS)   │  │
│  │  Templates   │  │  CSS (v4)    │  │  interactions.js, etc.   │  │
│  └──────────────┘  └──────────────┘  └──────────────────────────┘  │
└────────────────────────────┬────────────────────────────────────────┘
                             │ HTTP / WebSocket
┌────────────────────────────▼────────────────────────────────────────┐
│                    ASGI Application (Daphne)                        │
│  ┌─────────────────────────┐  ┌────────────────────────────────┐ │
│  │  HTTP → Django WSGI/ASGI│  │  WebSocket → Channels Router   │ │
│  │  (Views, Forms, Auth)   │  │  (ChatConsumer, NotificationCon.)│ │
│  └─────────────────────────┘  └────────────────────────────────┘ │
└────────────────────────────┬────────────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────────────┐
│                      Django Application Layer                       │
│  ┌────────┐  ┌────────┐  ┌──────────────┐  ┌──────────────────┐   │
│  │ users  │  │  feed  │  │ intelligence │  │  communication   │   │
│  │ (Auth, │  │ (Posts,│  │ (Gemini AI)  │  │  (WS Consumers)  │   │
│  │Profile)│  │ Jobs)  │  │              │  │                  │   │
│  └────────┘  └────────┘  └──────────────┘  └──────────────────┘   │
└────────────────────────────┬────────────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────────────┐
│                         Data & External Layer                       │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────────┐   │
│  │ SQLite3  │  │  Media/  │  │  Gemini  │  │  Stripe Payments │   │
│  │ Database │  │  Uploads │  │  API     │  │  Gateway         │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

### Application Modules

| App | Responsibility |
|-----|----------------|
| **config** | Project settings, root URL routing, ASGI/WSGI configuration |
| **users** | Authentication, profiles, portfolio, skills, monetization, social graph |
| **feed** | Posts, comments, jobs, proposals, notifications, DMs, bookmarks, reports |
| **intelligence** | Google Gemini AI engine, AI report storage and caching |
| **communication** | WebSocket consumers for chat and live notifications (no DB models) |

### Request Flow (HTTP)

1. Browser sends HTTP request → Daphne ASGI server
2. Django middleware stack processes request (security, session, CSRF, auth)
3. URL router dispatches to appropriate view (CBV or function view)
4. View queries models, applies business logic, returns template response
5. Context processors inject global data (unread notification count, user rank)

### Request Flow (WebSocket)

1. Browser opens WebSocket connection (`ws/chat/<username>/` or `ws/notifications/`)
2. `AuthMiddlewareStack` authenticates user from session cookie
3. Consumer joins channel group (sorted user IDs for chat, user ID for notifications)
4. Messages are persisted to DB (chat) and broadcast to group members
5. Notification consumer receives real-time toast payloads

---

## 5. Project Structure

```
DevHuddle/
├── config/                         # Django project configuration
│   ├── settings.py                 # All project settings
│   ├── urls.py                     # Root URL router
│   ├── asgi.py                     # ASGI + Channels WebSocket routing
│   └── wsgi.py                     # WSGI entry point
│
├── users/                          # User management app
│   ├── models.py                   # CustomUser, Skill, Project, Experience
│   ├── views.py                    # Auth, profile, store, social actions
│   ├── forms.py                    # Signup, profile, portfolio forms
│   ├── urls.py                     # /users/* routes
│   ├── signals.py                  # Welcome notification, avatar cleanup
│   ├── validators.py               # Username, file size, image extension
│   ├── admin.py                    # Django admin registration
│   └── management/commands/
│       └── sweep_accounts.py       # Permanent account deletion cron
│
├── feed/                           # Social feed & marketplace app
│   ├── models.py                   # Post, Comment, Proposal, Notification, etc.
│   ├── views.py                    # Feed, dashboards, moderation, search
│   ├── forms.py                    # Post, comment, proposal forms (RBAC)
│   ├── urls.py                     # Root / routes
│   ├── signals.py                  # Image cleanup, WS notification broadcast
│   ├── context_processors.py       # Global unread counts & user rank
│   ├── templatetags/
│   │   └── markdown_extras.py      # Custom Markdown template filter
│   └── admin.py
│
├── intelligence/                   # AI analysis app
│   ├── models.py                   # AIReport
│   ├── views.py                    # Profile/post analyzer views
│   ├── services.py                 # DevHuddleAIEngine (Gemini facade)
│   └── urls.py                     # /ai/* routes
│
├── communication/                  # Real-time WebSocket app
│   ├── consumers.py                # ChatConsumer, NotificationConsumer
│   ├── routing.py                  # WebSocket URL patterns
│   └── views.py                    # (empty stub)
│
├── templates/                      # 55 HTML templates
│   ├── base.html                   # Master layout
│   ├── sections/                   # navbar, footer, pagination
│   ├── pages/                      # Full page templates
│   ├── components/                 # Reusable UI components
│   ├── users/                      # Auth & profile templates
│   └── intelligence/               # AI dashboard & report templates
│
├── static/
│   ├── css/
│   │   ├── input.css               # Tailwind v4 source
│   │   └── output.css              # Compiled CSS (generated)
│   ├── js/                         # 6 JavaScript modules
│   └── images/                     # Favicon, screenshots
│
├── media/                          # User uploads (gitignored)
├── manage.py
├── requirements.txt                # Python dependencies (66 packages)
├── package.json                    # NPM / Tailwind toolchain
├── .env.example                    # Environment variable template
├── README.md                       # Developer setup notes
└── ABOUT.md                        # This document
```

---

## 6. Features

### 6.1 Authentication & Account Management

| Feature | Description |
|---------|-------------|
| **User Registration** | Signup with username, email, password, and role selection |
| **Login / Logout** | Django session-based authentication |
| **Password Reset** | Full email pipeline with custom Tailwind-styled templates |
| **Profile Editing** | Bio, avatar, social URLs, role, tech stack |
| **Account Deletion** | 3-day grace period; cancelled on re-login; permanent purge via `sweep_accounts` |
| **Username Validation** | Reserved words blocked, alphanumeric + `.`/`_`, no platform name |

### 6.2 Social Networking

| Feature | Description |
|---------|-------------|
| **Follow / Unfollow** | AJAX toggle with follower count update |
| **Block / Unblock** | Mutual unfollow on block; content hidden from feeds |
| **Network Page** | View followers, following, and blocked users |
| **Developer Directory** | Leaderboard ranked by Dev Score with skill filtering (`?skill=Python`) |
| **Profile Visits** | Public profile pages with portfolio, experience, skills |

### 6.3 Content & Feed System

| Feature | Description |
|---------|-------------|
| **Multi-Tab Feed** | Fellows (following), Business (jobs), Ads, Global (ranked) |
| **Huddle Posts** | Standard social posts with Markdown, images, likes, comments |
| **Job Posts** | Clients/orgs post job offers with deadlines |
| **Ad Posts** | Promotional posts with target URLs and deadlines |
| **Nested Comments** | Threaded replies with soft-delete (`is_deleted` flag) |
| **Like System** | Toggle like with real-time count (AJAX) |
| **Bookmarks** | Save posts to private vault (AJAX toggle) |
| **Content Reports** | Flag inappropriate posts; one report per user per post |
| **Search** | Unified search across users, huddles, and jobs |
| **Markdown Support** | Post bodies rendered via custom template filter |

### 6.4 Job Marketplace

| Feature | Description |
|---------|-------------|
| **Job Posting** | Clients/orgs create job-type posts |
| **Job Applications** | Developers submit proposals with cover letter and optional bid |
| **Proposal Management** | Clients accept or reject proposals from dashboard |
| **Unique Constraint** | One application per developer per job (DB-level) |
| **Ecosystem Explorer** | `/explore/` — browse jobs, top clients, featured projects |

### 6.5 Dashboards

| Dashboard | Access | Content |
|-----------|--------|---------|
| **Developer Dashboard** | `dev` role | Submitted proposals, application status |
| **Client Dashboard** | `client` / `org` role | Posted jobs, received proposals |
| **Moderation Dashboard** | Staff / superuser | Pending content reports, dismiss/delete actions |
| **AI Dashboard** | Authenticated | History of AI-generated reports |

### 6.6 Messaging & Notifications

| Feature | Description |
|---------|-------------|
| **Direct Messages** | HTTP form submission + WebSocket live delivery |
| **Inbox** | Conversation list with unread indicators |
| **Notifications** | 20+ notification types with themed UI (color palettes + emojis) |
| **Real-Time Toasts** | WebSocket push to browser toast container |
| **Auto Mark-Read** | Notifications marked read when visiting notifications page |

### 6.7 AI Intelligence

| Feature | Description |
|---------|-------------|
| **Profile Analysis** | Gemini-powered recruiter-style Markdown report |
| **Post Review** | Technical breakdown, engagement analysis, follow-up suggestions |
| **7-Day Cache** | Reduces API quota by reusing recent reports |
| **Fallback Cascade** | `gemini-3.5-flash` → `gemini-2.5-flash` → graceful error |
| **Loading Overlay** | Full-screen AI computation animation |

### 6.8 Monetization

| Feature | Description |
|---------|-------------|
| **DevHuddle Pro** | $15/month premium subscription (30-day expiry) |
| **Profile Boosts** | Purchasable boosts that increase Dev Score ranking |
| **Boost Transfer** | Gift boosts to other users from profile page |
| **Stripe Checkout** | Secure hosted payment page with server-side verification |

### 6.9 Moderation & Safety

| Feature | Description |
|---------|-------------|
| **User Reports** | Community-driven content flagging |
| **Staff Dashboard** | Review reports, dismiss false positives, delete violating posts |
| **Block System** | Users can block others to prevent interaction |
| **File Validation** | 5 MB max, `.jpg`/`.jpeg`/`.png` only |

---

## 7. User Roles & Access Control (RBAC)

### Role Definitions

| Role | Code | Capabilities |
|------|------|-------------|
| **Developer** | `dev` | Post huddles, apply to jobs, dev dashboard, AI analysis |
| **Client** | `client` | Post huddles + jobs + ads, client dashboard, manage proposals |
| **Organization** | `org` | Same as client |
| **Staff** | `is_staff=True` | Moderation dashboard access |
| **Superuser** | `is_superuser=True` | Django admin + moderation |

### Access Control Matrix

| Action | dev | client | org | staff | anonymous |
|--------|-----|--------|-----|-------|-----------|
| View home (limited) | ✅ | ✅ | ✅ | ✅ | ✅ (public feed) |
| Post huddle | ✅ | ✅ | ✅ | ✅ | ❌ |
| Post job/ad | ❌ | ✅ | ✅ | ✅ | ❌ |
| Apply to job | ✅ | ❌ | ❌ | — | ❌ |
| Accept/reject proposal | ❌ | ✅ | ✅ | — | ❌ |
| Dev dashboard | ✅ | ❌ | ❌ | — | ❌ |
| Client dashboard | ❌ | ✅ | ✅ | — | ❌ |
| Moderation | ❌ | ❌ | ❌ | ✅ | ❌ |
| Edit own content | ✅ | ✅ | ✅ | ✅ | ❌ |
| Edit others' content | ❌ | ❌ | ❌ | ❌ | ❌ |

### Enforcement Mechanisms

- **`LoginRequiredMixin`** — redirects unauthenticated users to login
- **`UserPassesTestMixin`** — custom `test_func()` for role/ownership checks
- **Form-level RBAC** — `PostForm.__init__()` restricts post types by role
- **DB constraints** — `unique_together` on proposals and bookmarks

---

## 8. Database Schema

### Entity-Relationship Overview

```
┌─────────────┐       M2M        ┌─────────────┐
│  CustomUser │◄────────────────►│  CustomUser │  (following/followers)
│             │◄────────────────►│  CustomUser │  (blocked_users)
└──────┬──────┘                  └─────────────┘
       │
       │ 1:N
       ├──────────────────┬──────────────────┬──────────────────┐
       ▼                  ▼                  ▼                  ▼
┌─────────────┐   ┌─────────────┐   ┌─────────────┐   ┌─────────────┐
│   Project   │   │ Experience  │   │    Post     │   │  AIReport   │
└─────────────┘   └─────────────┘   └──────┬──────┘   └─────────────┘
                                           │
       ┌───────────┬───────────┬───────────┼───────────┬───────────┐
       ▼           ▼           ▼           ▼           ▼           ▼
┌───────────┐ ┌─────────┐ ┌──────────┐ ┌─────────┐ ┌─────────┐ ┌────────┐
│  Comment  │ │Proposal │ │Notificat.│ │ Message │ │Bookmark │ │ Report │
└───────────┘ └─────────┘ └──────────┘ └─────────┘ └─────────┘ └────────┘

┌─────────────┐       M2M        ┌─────────────┐
│    Skill    │◄────────────────►│  CustomUser │
└─────────────┘                  └─────────────┘
```

### 8.1 `users.CustomUser` (extends `AbstractUser`)

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `username` | CharField(20) | unique, min 3 chars, custom validator | Display name |
| `email` | EmailField | unique | Login identifier |
| `bio` | TextField | nullable | User biography |
| `avatar` | ImageField | max 5MB, jpg/png | Profile picture |
| `github_url` | URLField | nullable | GitHub profile link |
| `linkedin_url` | URLField | nullable | LinkedIn profile link |
| `twitter_url` | URLField | nullable | X/Twitter profile link |
| `stackoverflow_url` | URLField | nullable | StackOverflow link |
| `portfolio_url` | URLField | nullable | Personal website |
| `fiver_url` | URLField | nullable | Fiverr profile |
| `upwork_url` | URLField | nullable | Upwork profile |
| `following` | M2M(self) | symmetrical=False | Users this user follows |
| `blocked_users` | M2M(self) | symmetrical=False | Blocked user list |
| `role` | CharField(10) | choices: dev/client/org | User persona |
| `tech_stack` | CharField(255) | comma-separated | Raw skill string |
| `premium_expires_at` | DateTimeField | nullable | Pro subscription expiry |
| `profile_boosts` | IntegerField | default=0 | Purchased boost count |
| `deletion_scheduled_at` | DateTimeField | nullable | Account deletion timer |

**Computed Property:** `is_premium` → `premium_expires_at > now()`

### 8.2 `users.Skill`

| Field | Type | Constraints |
|-------|------|-------------|
| `name` | CharField(50) | unique |
| `users` | M2M(CustomUser) | related_name="skills" |

### 8.3 `users.Project`

| Field | Type | Constraints |
|-------|------|-------------|
| `user` | FK(CustomUser) | CASCADE, related_name="projects" |
| `title` | CharField(100) | — |
| `description` | TextField(1000) | — |
| `live_url` | URLField | nullable |
| `github_url` | URLField | nullable |
| `image` | ImageField | nullable, validated |
| `created_at` | DateTimeField | auto_now_add |

### 8.4 `users.Experience`

| Field | Type | Constraints |
|-------|------|-------------|
| `user` | FK(CustomUser) | CASCADE, related_name="experiences" |
| `company` | CharField(100) | — |
| `role` | CharField(100) | — |
| `start_date` | DateField | — |
| `end_date` | DateField | nullable |
| `is_current` | BooleanField | default=False |
| `description` | TextField(1000) | blank |

### 8.5 `feed.Post`

| Field | Type | Constraints |
|-------|------|-------------|
| `author` | FK(CustomUser) | CASCADE |
| `body` | TextField(500) | Markdown content |
| `image` | ImageField | nullable, auto-renamed |
| `created_at` | DateTimeField | auto_now_add |
| `post_type` | CharField(10) | huddle / job / ad |
| `is_boosted` | BooleanField | default=False |
| `likes` | M2M(CustomUser) | related_name="liked_posts" |
| `deadline` | DateTimeField | nullable (jobs/ads) |
| `target_url` | URLField | nullable (ads) |
| `tags` | CharField(100) | comma-separated hashtags |

### 8.6 `feed.Comment`

| Field | Type | Constraints |
|-------|------|-------------|
| `post` | FK(Post) | CASCADE, related_name="comments" |
| `author` | FK(CustomUser) | CASCADE |
| `body` | TextField(200) | — |
| `parent` | FK(self) | nullable (nested replies) |
| `is_deleted` | BooleanField | soft-delete flag |
| `created_at` | DateTimeField | auto_now_add |

### 8.7 `feed.Proposal`

| Field | Type | Constraints |
|-------|------|-------------|
| `job` | FK(Post) | CASCADE, limit_choices_to post_type="job" |
| `applicant` | FK(CustomUser) | CASCADE |
| `cover_letter` | TextField(1500) | — |
| `bid_amount` | DecimalField(10,2) | nullable |
| `status` | CharField(10) | pending / accepted / rejected |
| `created_at` | DateTimeField | auto_now_add |
| **unique_together** | — | (job, applicant) |

### 8.8 `feed.Notification`

| Field | Type | Constraints |
|-------|------|-------------|
| `recipient` | FK(CustomUser) | CASCADE |
| `actor` | FK(CustomUser) | CASCADE |
| `verb` | CharField(26) | 20+ predefined verbs |
| `post` | FK(Post) | nullable |
| `is_read` | BooleanField | default=False |
| `created_at` | DateTimeField | auto_now_add |

**Notification Verbs:** welcome, premium, congrats, beware, alert, like, comment, reply, dm, connect, follow, unfollow, block, boost, hire, accept, reject, visit, profile, post, delete, report_submitted, post_reported

### 8.9 `feed.Message`

| Field | Type | Constraints |
|-------|------|-------------|
| `sender` | FK(CustomUser) | CASCADE |
| `recipient` | FK(CustomUser) | CASCADE |
| `body` | TextField(2000) | — |
| `is_read` | BooleanField | default=False |
| `created_at` | DateTimeField | auto_now_add |

### 8.10 `feed.Bookmark`

| Field | Type | Constraints |
|-------|------|-------------|
| `user` | FK(CustomUser) | CASCADE |
| `post` | FK(Post) | CASCADE |
| `created_at` | DateTimeField | auto_now_add |
| **unique_together** | — | (user, post) |

### 8.11 `feed.Report`

| Field | Type | Constraints |
|-------|------|-------------|
| `reporter` | FK(CustomUser) | CASCADE |
| `post` | FK(Post) | CASCADE |
| `reason` | CharField(255) | default="Inappropriate Content or Spam" |
| `is_resolved` | BooleanField | default=False |
| `created_at` | DateTimeField | auto_now_add |

### 8.12 `intelligence.AIReport`

| Field | Type | Constraints |
|-------|------|-------------|
| `report_type` | CharField(10) | profile / post |
| `requester` | FK(CustomUser) | CASCADE |
| `target_user` | FK(CustomUser) | nullable |
| `target_post` | FK(Post) | nullable |
| `content` | TextField | Markdown AI response |
| `created_at` | DateTimeField | auto_now_add |

### Database Migrations

| App | Migrations |
|-----|------------|
| users | `0001_initial`, `0002_customuser_blocked_users`, `0003_customuser_deletion_scheduled_at` |
| feed | `0001_initial`, `0002_initial` |
| intelligence | `0001_initial`, `0002_initial` |
| communication | (empty — no models) |

---

## 9. Pages & User Interface

### 9.1 Public Pages (No Login Required)

| Page | URL | Template | Description |
|------|-----|----------|-------------|
| Home (Guest) | `/` | `pages/home.html` | Landing page with limited public feed |
| About | `/about/` | `pages/about.html` | Platform overview, staff, roadmap, live stats |
| Support | `/support/` | `pages/support.html` | Help & knowledge base |

### 9.2 Authenticated Pages

| Page | URL | Template | Description |
|------|-----|----------|-------------|
| Home (Feed) | `/?feed=fellows` | `pages/home.html` | 3-column feed with sidebars |
| Post Detail | `/post/<pk>/` | `components/posts/view.html` | Single post with comments |
| Post Create | `/post/new/` | `components/posts/create.html` | New post form |
| Post Edit | `/post/<pk>/edit/` | `components/posts/update.html` | Edit own post |
| Search | `/search/?q=` | `pages/search_results.html` | Users, huddles, jobs |
| Notifications | `/notifications/` | `pages/notifications.html` | Notification inbox |
| Inbox | `/inbox/` | `pages/inbox.html` | DM conversation list |
| Chat Thread | `/inbox/<username>/` | `pages/chat_thread.html` | Live chat with user |
| Explore | `/explore/` | `pages/jobs_clients.html` | Jobs, clients, projects |
| Dev Dashboard | `/dashboard/dev/` | `pages/dev_dashboard.html` | Developer workspace |
| Client Dashboard | `/dashboard/client/` | `pages/client_dashboard.html` | Client workspace |
| Developers | `/users/developers/` | `pages/developers.html` | Leaderboard directory |
| Store | `/users/store/` | `pages/store.html` | Monetization storefront |
| Moderation | `/moderation/` | `pages/moderation_dashboard.html` | Staff moderation queue |
| AI Dashboard | `/ai/dashboard/` | `intelligence/dashboard.html` | AI report history |
| AI Report | `/ai/analyze/*` | `intelligence/report.html` | Generated AI analysis |

### 9.3 Profile & Auth Pages

| Page | URL | Template |
|------|-----|----------|
| Login | `/users/login/` | `users/auth/login.html` |
| Signup | `/users/signup/` | `users/auth/signup.html` |
| Password Reset | `/users/password-reset/` | `users/auth/password_reset_form.html` |
| Profile View | `/users/profile/<username>/` | `users/profile/view.html` |
| Profile Edit | `/users/edit/` | `users/profile/edit.html` |
| Profile Delete | `/users/delete/` | `users/profile/delete.html` |
| Network | `/users/profile/<username>/network/` | `users/profile/network.html` |
| Skills Edit | `/users/profile/skills/edit/` | `users/profile/skill_form.html` |
| Project Form | `/users/profile/project/new/` | `users/profile/project_form.html` |
| Experience Form | `/users/profile/experience/new/` | `users/profile/experience_form.html` |

### 9.4 Reusable Components

| Component | Path | Usage |
|-----------|------|-------|
| Navbar | `sections/navbar.html` | Global navigation |
| Footer | `sections/footer.html` | Global footer |
| Post Card | `components/feed/post_card.html` | Feed item rendering |
| Feed Tabs | `components/feed/feed_tabs.html` | Fellows/Business/Ads/Global tabs |
| Search Bar | `components/searchbar/` | Big & small search inputs |
| Landing Sections | `components/landing/` | Intro, features, sidebars for guest home |
| User Dropdown | `components/menu/user_profile.html` | Profile menu |
| Mobile Menu | `components/menu/mobile_screen.html` | Responsive navigation |

### 9.5 Layout Structure

```
┌─────────────────────────────────────────────────────┐
│                    NAVBAR (h-14)                     │
├─────────────────────────────────────────────────────┤
│                                                     │
│                   MAIN CONTENT                       │
│              (flex-1, overflow-auto)                 │
│                                                     │
│  ┌──────────┐  ┌──────────────┐  ┌──────────┐     │
│  │  Left    │  │   Center     │  │  Right   │     │
│  │ Sidebar  │  │   Feed       │  │ Sidebar  │     │
│  │ (Jobs,   │  │   (Posts)    │  │ (Devs,   │     │
│  │ Projects)│  │              │  │  Stats)  │     │
│  └──────────┘  └──────────────┘  └──────────┘     │
│                                                     │
├─────────────────────────────────────────────────────┤
│                    FOOTER (h-14)                     │
└─────────────────────────────────────────────────────┘

Overlays: AI Loading Spinner | Toast Notifications (bottom-right)
```

---

## 10. Theme & Design System

### Design Philosophy

DevHuddle uses a **dark-only, developer-aesthetic UI** designed for extended screen time. The design emphasizes readability, glassmorphism effects, and semantic color coding.

### Color Palette

| Token | Tailwind Class | Usage |
|-------|---------------|-------|
| Background | `bg-gray-900` | Page background |
| Surface | `bg-gray-800` | Cards, panels |
| Border | `border-gray-700` | Dividers, card borders |
| Text Primary | `text-gray-300` | Body text |
| Text Muted | `text-gray-400` / `text-gray-500` | Secondary text |
| Primary Accent | `text-blue-500` / `bg-blue-600` | Links, buttons, CTAs |
| Secondary Accent | `text-purple-500` / `bg-purple-500` | AI features, gradients |
| Success | `text-green-500` / `bg-green-500` | Positive actions, accepted |
| Danger | `text-red-500` / `bg-red-500` | Errors, rejections, reports |
| Warning | `text-yellow-500` / `bg-yellow-500` | Boosts, premium badges |

### Typography

| Element | Style |
|---------|-------|
| Headings | `font-extrabold`, large sizes (text-5xl to text-7xl on hero) |
| Body | `font-sans antialiased` |
| Code/Mono | `font-mono` for tags, timestamps, AI status |
| Markdown Content | `@tailwindcss/typography` prose classes |

### UI Patterns

| Pattern | Implementation |
|---------|---------------|
| Cards | `rounded-2xl` / `rounded-3xl`, `border border-gray-700`, `shadow-xl` |
| Inputs | `rounded-full` or `rounded-xl`, dark backgrounds, blue focus ring |
| Buttons | `rounded-full`, solid blue primary, hover transitions |
| Avatars | `rounded-full`, border-2, fallback initial letter |
| Gradients | `bg-linear-to-r from-blue-400 to-purple-500` (text clips) |
| Glassmorphism | `backdrop-blur-md`, semi-transparent overlays |
| Scrollbars | Hidden via `::-webkit-scrollbar { width: 0 }` |
| Autofill | Custom dark autofill styling for form inputs |

### Notification Theme Mapping

Notifications use a semantic color system mapped from verb types:

| Category | Colors | Verbs |
|----------|--------|-------|
| Danger | Red | block, unfollow, delete, reject, post_reported |
| Brand | Yellow | boost, welcome |
| Success | Green | premium, congrats, hire, accept, report_submitted |
| Info | Purple | profile, connect, follow, post, dm |
| Neutral | Blue | like, comment, reply, visit |
| Warning | Gray | alert, beware |

### CSS Build Pipeline

```bash
# Source file
static/css/input.css

# Tailwind v4 directives
@import "tailwindcss";
@source "../../templates/**/*.html";
@source "../../**/*.py";
@source "../js/*.js";

# Build command
npm run tailwind
# → npx tailwindcss -i ./static/css/input.css -o ./static/css/output.css --watch

# Output
static/css/output.css  (linked in base.html)
```

---

## 11. HTTP Routes & Endpoints

### Root Router (`config/urls.py`)

| Prefix | App | Description |
|--------|-----|-------------|
| `/admin/` | Django Admin | Staff administration |
| `/users/` | users | Authentication & profiles |
| `/` | feed | Home, posts, dashboards |
| `/ai/` | intelligence | AI analysis |
| `/media/*` | Static (DEBUG only) | User uploads |

### Feed Routes (`feed/urls.py`)

| Method | URL | Name | View | Auth |
|--------|-----|------|------|------|
| GET | `/` | home | HomePageView | Public |
| GET | `/about/` | about | AboutPageView | Public |
| GET/POST | `/post/new/` | post_new | PostCreateView | Login |
| GET/POST | `/post/<pk>/edit/` | post_edit | PostUpdateView | Owner |
| GET/POST | `/post/<pk>/delete/` | post_delete | PostDeleteView | Owner |
| GET | `/post/<pk>/` | post_detail | PostDetailView | Login |
| POST | `/post/like/<pk>/` | like_post | like_post | Login (JSON) |
| GET/POST | `/comment/<pk>/edit/` | comment_edit | CommentUpdateView | Author |
| POST | `/comment/<pk>/delete/` | comment_delete | CommentDeleteView | Author |
| GET | `/search/` | search | search_results | Login |
| GET | `/notifications/` | notifications | NotificationListView | Login |
| GET | `/explore/` | jobs_clients | EcosystemDiscoveryView | Login |
| GET | `/support/` | support | HelpSupportView | Public |
| GET/POST | `/job/<pk>/apply/` | apply_job | ProposalCreateView | dev |
| POST | `/proposal/<pk>/<action>/` | proposal_action | ProposalActionView | Job author |
| GET | `/dashboard/client/` | client_dashboard | ClientDashboardView | client/org |
| GET | `/dashboard/dev/` | dev_dashboard | DeveloperDashboardView | dev |
| GET | `/inbox/` | inbox | InboxView | Login |
| GET/POST | `/inbox/<username>/` | chat_thread | ChatThreadView | Login |
| POST | `/post/<pk>/bookmark/` | toggle_bookmark | toggle_bookmark | Login (JSON) |
| POST | `/post/<pk>/report/` | submit_report | submit_report | Login (JSON) |
| GET | `/moderation/` | moderation_dashboard | ModerationDashboardView | Staff |
| POST | `/moderation/<pk>/<action>/` | moderation_action | ModerationActionView | Staff |

### Users Routes (`users/urls.py`)

| Method | URL | Name | View |
|--------|-----|------|------|
| GET/POST | `/users/login/` | login | LoginView |
| POST | `/users/logout/` | logout | LogoutView |
| GET/POST | `/users/signup/` | signup | SignUpView |
| GET/POST | `/users/password-reset/` | password_reset | PasswordResetView |
| GET | `/users/password-reset/done/` | password_reset_done | PasswordResetDoneView |
| GET/POST | `/users/password-reset-confirm/<uidb64>/<token>/` | password_reset_confirm | PasswordResetConfirmView |
| GET | `/users/password-reset-complete/` | password_reset_complete | PasswordResetCompleteView |
| GET/POST | `/users/edit/` | profile_edit | ProfileUpdateView |
| GET/POST | `/users/delete/` | profile_delete | ProfileDeleteView |
| GET | `/users/profile/<username>/` | user_profile | UserProfileView |
| GET/POST | `/users/profile/skills/edit/` | skill_edit | SkillUpdateView |
| GET | `/users/developers/` | developer_directory | DeveloperDirectoryView |
| POST | `/users/follow/<username>/` | follow_user | follow_user (JSON) |
| POST | `/users/profile/<username>/block/` | toggle_block | toggle_block |
| GET | `/users/profile/<username>/network/` | user_network | NetworkView |
| GET/POST | `/users/profile/project/new/` | project_create | ProjectCreateView |
| GET/POST | `/users/profile/project/<pk>/edit/` | project_edit | ProjectUpdateView |
| GET/POST | `/users/profile/project/<pk>/delete/` | project_delete | ProjectDeleteView |
| GET/POST | `/users/profile/experience/new/` | experience_create | ExperienceCreateView |
| GET/POST | `/users/profile/experience/<pk>/edit/` | experience_edit | ExperienceUpdateView |
| GET/POST | `/users/profile/experience/<pk>/delete/` | experience_delete | ExperienceDeleteView |
| GET | `/users/store/` | store | StoreView |
| POST | `/users/store/checkout/` | checkout | CreateStripeCheckoutSessionView |
| GET | `/users/store/checkout/success/` | checkout_success | PaymentSuccessView |
| POST | `/users/profile/<username>/boost/` | boost_user | BoostUserView |

### Intelligence Routes (`intelligence/urls.py`)

| Method | URL | Name | View |
|--------|-----|------|------|
| GET | `/ai/dashboard/` | ai_dashboard | AIDashboardView |
| GET | `/ai/analyze/profile/<username>/` | ai_analyze_profile | ProfileAnalyzerView |
| GET | `/ai/analyze/post/<pk>/` | ai_analyze_post | PostAnalyzerView |
| POST | `/ai/delete/<pk>/` | ai_delete | AIDeleteReportView |

---

## 12. AJAX & WebSocket APIs

> **Note:** DevHuddle does not expose a REST API (no Django REST Framework). The following are partial API-like endpoints used by frontend JavaScript.

### 12.1 AJAX Endpoints (JSON)

All require authentication and CSRF token in request headers.

#### Like Post

```
POST /post/like/<pk>/
Response: { "liked": true|false, "like_count": <int> }
```

#### Toggle Bookmark

```
POST /post/<pk>/bookmark/
Response: { "saved": true|false, "message": "<string>" }
```

#### Submit Report

```
POST /post/<pk>/report/
Response: { "reported": true|false, "message": "<string>" }
```

#### Follow User

```
POST /users/follow/<username>/
Response: { "is_following": true|false, "followers_count": <int>, "following_count": <int> }
```

### 12.2 WebSocket Endpoints

#### Chat WebSocket

```
URL: ws://<host>/ws/chat/<username>/
Auth: Session cookie (AuthMiddlewareStack)

Send:    { "message": "<text>" }
Receive: { "message": "<text>", "sender": "<username>", "time": "<formatted>" }
```

#### Notification WebSocket

```
URL: ws://<host>/ws/notifications/
Auth: Session cookie

Receive: { "verb": "<display text>", "actor": "<username>", "icon": "<emoji>" }
         { "is_dm": true, "actor": "<username>", "message_preview": "<text>" }
```

### 12.3 JavaScript Modules

| File | Responsibility |
|------|---------------|
| `interactions.js` | Likes, bookmarks, reports (fetch API), post expand/collapse |
| `websockets.js` | Notification + chat WebSocket connections, toast UI |
| `follow_logic.js` | Follow/unfollow AJAX |
| `menu_toggle.js` | Mobile menu & profile dropdown |
| `feed_controller.js` | Feed tab switching & UI |
| `post_upload_validator.js` | Client-side file validation before upload |

---

## 13. Core Algorithms

### 13.1 Dev Score (Developer Ranking)

Used in: Developer Directory, Profile sidebar, Home right sidebar, Context processor.

**Formula:**

```
dev_score = (followers × 2) + (projects × 3) + (profile_boosts × 7) + premium_bonus
```

**Premium Bonus:**

| Context | Bonus |
|---------|-------|
| Profile view / Home sidebar | +50 if `is_premium` |
| Developer directory | +20 if `is_premium` |

**Ordering:** `-dev_score`, then `-date_joined`

**Implementation:** Django ORM `annotate()` with `ExpressionWrapper`, `Count`, and `Case/When`.

### 13.2 Global Feed Engagement Score

Used in: Home feed when `?feed=global`.

**Formula:**

```
engagement_score = (likes × 2) + (comments × 3)
```

**Ordering:** `-is_boosted`, `-engagement_score`, `-created_at`

### 13.3 Feed Filtering Logic

| Tab | Filter |
|-----|--------|
| `fellows` (default) | Posts from followed users, type=huddle only |
| `business` | post_type=job |
| `ads` | post_type=ad |
| `global` | All types, ranked by engagement score |

**Block Filtering:** All authenticated feeds exclude users in `blocked_users` and `blocked_by` lists.

### 13.4 Search Algorithm

| Entity | Fields Searched | Ordering |
|--------|----------------|----------|
| Users | username, first_name, last_name, bio, skills | `-follower_count` (limit 10) |
| Huddles | body, tags | `-like_count`, `-created_at` (limit 15) |
| Jobs | body, tags | `-created_at` (limit 10) |

---

## 14. AI Intelligence Module

### Architecture

```
User clicks "Analyze" → ProfileAnalyzerView / PostAnalyzerView
                              │
                              ▼
                    DevHuddleAIEngine (Facade)
                              │
                    ┌─────────┴─────────┐
                    ▼                   ▼
              Check 7-day cache    Build context JSON
                    │                   │
                    ▼                   ▼
              Return cached      Call Gemini API
              report if valid    (3.5-flash → 2.5-flash)
                                        │
                                        ▼
                              Save AIReport to DB
                              Create notifications
                              Render Markdown report
```

### Profile Analysis Context Payload

```json
{
  "identity": { "username", "role", "bio" },
  "network": { "followers", "following", "is_premium" },
  "expertise": {
    "skills": ["Python", "Django", ...],
    "projects": [{ "title", "tech_details" }],
    "experiences": [{ "role", "company" }]
  }
}
```

### Post Review Context Payload

```json
{
  "post": { "body", "type", "age_in_days", "has_media" },
  "author": { "username", "role", "premium_status" },
  "engagement": { "likes", "comments" }
}
```

### AI Report Output Sections

**Profile Analysis:**

- Core Identity & Strengths
- Areas for Growth
- Market Viability

**Post Review:**

- Technical Breakdown
- Engagement Analysis
- Suggested Follow-up

### Caching Strategy

- Reports cached for **7 days** per target (user or post)
- Reduces Gemini API quota consumption
- User can delete reports from AI dashboard

---

## 15. Monetization (Stripe)

### Products

| Item Code | Name | Backend Price | Duration/Quantity |
|-----------|------|--------------|-------------------|
| `premium` | DevHuddle Pro (30 Days) | $15.00 (1500 cents) | 30-day subscription |
| `boost_1` | 1x Profile Boost | $2.00 (200 cents) | +1 boost |
| `boost_5` | 5x Profile Boosts | $8.00 (800 cents) | +5 boosts |

### Payment Flow

1. User selects item on Store page → POST to `/users/store/checkout/`
2. Server creates Stripe Checkout Session with dynamic `price_data`
3. User redirected to Stripe-hosted payment page
4. On success → redirect to `/users/store/checkout/success/?session_id=...&item=...`
5. Server verifies payment via `stripe.checkout.Session.retrieve()`
6. If `payment_status == "paid"` → fulfill order (extend premium, add boosts)
7. Create success notification

### Boost Transfer

- Users with `profile_boosts > 0` can gift a boost to another user
- POST to `/users/profile/<username>/boost/`
- Decrements sender, increments recipient
- Creates `boost` notification

---

## 16. Real-Time Communication

### Technology Stack

| Component | Technology |
|-----------|-----------|
| Protocol | WebSocket (via Django Channels) |
| Server | Daphne ASGI |
| Channel Layer | InMemoryChannelLayer (dev) / Redis (production recommended) |
| Auth | `AuthMiddlewareStack` (session cookie) |

### Chat Flow

1. User A opens chat with User B → WebSocket to `ws/chat/<username>/`
2. Consumer creates room: `chat_{min_id}_{max_id}` (sorted user IDs)
3. User A sends message → saved to `Message` model
4. Broadcast to room group → both users receive in real-time
5. Parallel broadcast to User B's notification group with DM preview

### Notification Flow

1. Any action creates `Notification` record in DB
2. `post_save` signal on Notification triggers WebSocket broadcast
3. `NotificationConsumer` for recipient receives payload
4. `websockets.js` renders toast in bottom-right container

### Channel Groups

| Group Name Pattern | Purpose |
|-------------------|---------|
| `chat_{id1}_{id2}` | Chat room (sorted IDs) |
| `notifications_{user_id}` | Per-user notification stream |

---

## 17. Security Measures & Patches

### Implemented Security Features

| Measure | Implementation | Status |
|---------|---------------|--------|
| **CSRF Protection** | `CsrfViewMiddleware` on all POST requests | ✅ Active |
| **Session Authentication** | Django session middleware, cookie-based | ✅ Active |
| **Password Validators** | All 4 Django defaults (similarity, length, common, numeric) | ✅ Active |
| **X-Frame-Options** | `XFrameOptionsMiddleware` (clickjacking prevention) | ✅ Active |
| **File Upload Validation** | 5MB max, jpg/png only, server-side validators | ✅ Active |
| **Username Restrictions** | Reserved words, pattern validation, no platform name | ✅ Active |
| **Object-Level Permissions** | `UserPassesTestMixin` for edit/delete ownership | ✅ Active |
| **Role-Based Access** | Form-level and view-level RBAC | ✅ Active |
| **Stripe Payment Verification** | Server-side session retrieval before fulfillment | ✅ Active |
| **Account Deletion Grace** | 3-day delay prevents accidental permanent loss | ✅ Active |
| **Block System** | Mutual unfollow, feed exclusion | ✅ Active |
| **Content Moderation** | User reports + staff review dashboard | ✅ Active |
| **Environment Secrets** | API keys in `.env` via django-environ | ✅ Active |
| **Soft Comment Delete** | `is_deleted` flag preserves thread integrity | ✅ Active |

### Security Configuration (Current)

| Setting | Value | Production Recommendation |
|---------|-------|------------------------|
| `DEBUG` | `True` | Set to `False` |
| `SECRET_KEY` | Hardcoded in settings.py | Move to `.env` |
| `ALLOWED_HOSTS` | `[]` (empty) | Configure domain names |
| `CHANNEL_LAYERS` | InMemoryChannelLayer | Use Redis |
| `DATABASE` | SQLite3 | PostgreSQL for production |

### Planned Security Patches (from README)

| Patch | Description | Status |
|-------|-------------|--------|
| Password Reset Security | Enhanced token validation and rate limiting | 🔲 Planned |
| RBAC Enhancement | Finer-grained permission system | 🔲 Planned |
| API Authentication | Token-based auth for future REST API | 🔲 Planned |
| HTTPS Enforcement | `SECURE_SSL_REDIRECT`, HSTS headers | 🔲 Planned |
| Secret Key Externalization | Move from settings.py to environment | 🔲 Planned |

### Middleware Stack

```python
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
```

---

## 18. Signals & Background Tasks

### User Signals (`users/signals.py`)

| Signal | Trigger | Action |
|--------|---------|--------|
| `post_save(CustomUser)` | New user created | Create welcome notification |
| `pre_save(CustomUser)` | Avatar updated | Delete old avatar file from disk |
| `post_delete(CustomUser)` | Account deleted | Delete avatar file from disk |
| `user_logged_in` | User logs in | Cancel scheduled deletion if set |

### Feed Signals (`feed/signals.py`)

| Signal | Trigger | Action |
|--------|---------|--------|
| `pre_save(Post)` | Post image updated | Delete old image file |
| `post_delete(Post)` | Post deleted | Delete image file from disk |
| `post_save(Notification)` | New notification | Broadcast via WebSocket to recipient |

### Management Commands

| Command | File | Purpose |
|---------|------|---------|
| `sweep_accounts` | `users/management/commands/sweep_accounts.py` | Permanently delete accounts past 3-day grace period |

**Usage:**

```bash
python manage.py sweep_accounts
```

**Process:**

1. Query users where `deletion_scheduled_at <= now()`
2. Send farewell email via SMTP
3. Delete user (cascades to posts, comments, proposals, etc.)
4. Log deleted usernames to stdout

**Production:** Schedule via cron job or task scheduler (daily recommended).

---

## 19. Forms & Validation

### User Forms (`users/forms.py`)

| Form | Model | Fields |
|------|-------|--------|
| `CustomUserCreationForm` | CustomUser | username, email, role, password |
| `CustomUserChangeForm` | CustomUser | bio, avatar, role, social URLs, email |
| `ProjectForm` | Project | title, description, live_url, github_url, image |
| `ExperienceForm` | Experience | company, role, dates, is_current, description |
| `SkillUpdateForm` | — (FormView) | Comma-separated skills → normalized Skill objects |
| `CustomPasswordResetForm` | — | email (styled) |
| `CustomSetPasswordForm` | — | new password (styled) |

### Feed Forms (`feed/forms.py`)

| Form | Model | Fields | RBAC |
|------|-------|--------|------|
| `PostForm` | Post | post_type, body, image, deadline, target_url, tags | Devs: huddle only |
| `ProposalForm` | Proposal | cover_letter, bid_amount | — |
| `CommentForm` | Comment | body | — |

### Custom Validators (`users/validators.py`)

| Validator | Rule |
|-----------|------|
| `validate_file_size` | Maximum 5 MB |
| `validate_image_extension` | Only `.jpg`, `.jpeg`, `.png` |
| `validate_username` | No reserved words, alphanumeric + `.`/`_`, no consecutive dots/underscores, no "devhuddle" in name |

**Reserved Usernames:** admin, superuser, staff, login, logout, signup, register, api, media, static, assets, help, about, contact, terms, privacy, settings, profile, dashboard, feed, notifications, messages, search, explore, huddle, dev, root, support

---

## 20. Environment & Configuration

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

### Django Settings Summary

| Setting | Value |
|---------|-------|
| `AUTH_USER_MODEL` | `users.CustomUser` |
| `LOGIN_URL` | `login` |
| `LOGIN_REDIRECT_URL` | `home` |
| `LOGOUT_REDIRECT_URL` | `home` |
| `ACCOUNT_DELETION_DELAY` | 3 days |
| `TIME_ZONE` | `Asia/Karachi` |
| `LANGUAGE_CODE` | `en-us` |
| `MEDIA_URL` | `/media/` |
| `STATIC_URL` | `static/` |
| `EMAIL_BACKEND` | SMTP (Gmail) |
| `DEFAULT_FROM_EMAIL` | `DevHuddle Security <no-reply@devhuddle.com>` |
| `ASGI_APPLICATION` | `config.asgi.application` |

### Context Processors

`feed.context_processors.unread_notifications_count` injects into every template:

- `unread_notifications_count` — unread notification badge count
- `unread_dm_count` — unread direct message count
- `user_rank` — current user's position on Dev Score leaderboard

---

## 21. Installation & Setup

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

---

## 22. Testing Status

| Category | Status | Details |
|----------|--------|---------|
| Unit Tests | ❌ Not implemented | No `tests.py` or `test_*.py` files |
| Integration Tests | ❌ Not implemented | — |
| E2E Tests | ❌ Not implemented | — |
| Manual Testing | ✅ Active | Via development server |
| NPM Test Script | ❌ Placeholder | `"test": "echo Error: no test specified"` |

**Recommendation for thesis:** Document manual test cases performed during development. Consider adding pytest-django tests for critical flows (auth, proposals, payments) before final submission.

---

## 23. Known Limitations & Future Work

### Current Limitations

| # | Limitation | Impact |
|---|-----------|--------|
| 1 | No REST API | Third-party integrations not possible |
| 2 | SQLite database | Not suitable for high-concurrency production |
| 3 | In-memory channel layer | WebSockets don't scale across processes |
| 4 | No automated tests | Quality assurance relies on manual testing |
| 5 | Hardcoded SECRET_KEY | Security risk in production |
| 6 | DEBUG=True | Exposes stack traces in errors |
| 7 | Dark theme only | No light mode toggle |
| 8 | AI notification verb mismatch | `verb="ai"` not in VERB_CHOICES (potential runtime error) |

### Planned Improvements (from README)

| # | Feature | Priority |
|---|---------|----------|
| 1 | Notification sound/music | Medium |
| 2 | Recycle bin (3-day data recovery) | Medium |
| 3 | Light theme implementation | Low |
| 4 | REST API endpoints for developers | High |
| 5 | Enhanced RBAC system | High |
| 6 | Password reset security patches | High |
| 7 | Comprehensive test suite | High |
| 8 | Production deployment (PostgreSQL, Redis, HTTPS) | High |

### Production Deployment Checklist

- [ ] Set `DEBUG = False`
- [ ] Move `SECRET_KEY` to environment variable
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Switch to PostgreSQL database
- [ ] Configure Redis for `CHANNEL_LAYERS`
- [ ] Enable HTTPS (`SECURE_SSL_REDIRECT`, `SESSION_COOKIE_SECURE`)
- [ ] Set up `sweep_accounts` cron job
- [ ] Configure production Stripe keys
- [ ] Set up static file serving (WhiteNoise or CDN)
- [ ] Configure proper logging

---

## Quick Reference Card

```cmd
Project:     DevHuddle — Social Media for Software Engineers
Framework:   Django 6.0.6 + Channels 4.3.2 + Tailwind CSS 4.3.1
Database:    SQLite3 (11 models across 3 apps)
Auth:        Custom User Model (dev/client/org roles)
AI:          Google Gemini (profile analysis + post review)
Payments:    Stripe Checkout Sessions
Real-time:   WebSocket (chat + notifications)
Theme:       Dark-only (gray-900 base, blue/purple accents)
Endpoints:   50+ HTTP routes, 4 AJAX JSON, 2 WebSocket
Security:    CSRF, RBAC, file validation, moderation, grace deletion
```

---

*All rights reserved. No rules & regulations are manipulated or distorted.*  
*Last updated: July 2026*
