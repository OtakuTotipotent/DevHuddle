# DevHuddle — Professional Technical Documentation

## 1. Document control

| Item | Value |
|---|---|
| Project | DevHuddle |
| Type | Full-stack Django web application |
| Academic context | BSIT Final Year Project |
| Primary runtime | Python / Django |
| Realtime | Django Channels + WebSockets |
| Frontend | Django Templates + Tailwind CSS + Vanilla JavaScript |
| Database | SQLite3 |
| AI | Google Gemini |
| Payments | Stripe Checkout |
| Email | Gmail SMTP |
| Status | FYP/demo-ready; production hardening remains |
| Supplied version | 1.0.0 according to project README |

---

# 2. Executive Summary

DevHuddle is a developer-focused professional social networking and marketplace platform.

It combines professional identity, technical community interaction, project portfolios, job discovery, proposal management, communication, AI-assisted analysis, monetization, and moderation.

The platform supports three principal user roles:

- Developer;
- Client / Hirer;
- Organization.

Its main architectural goal is to provide one ecosystem in which developers can:

```text
Build identity
   ↓
Show skills + projects
   ↓
Build network
   ↓
Publish technical content
   ↓
Discover jobs
   ↓
Submit proposals
   ↓
Communicate
   ↓
Use AI analysis
   ↓
Increase professional visibility
```

---

# 3. Problem Statement

Software developers commonly use different platforms for:

- professional networking;
- portfolio presentation;
- technical discussion;
- freelance opportunities;
- direct communication;
- career analysis.

This fragmentation creates a product opportunity for a developer-specific ecosystem.

DevHuddle addresses this by combining the professional/social/community aspects of a network with marketplace functionality.

---

# 4. Objectives

The implementation targets these objectives:

1. Provide role-based developer/client/organization accounts.
2. Provide developer profiles and portfolios.
3. Support social networking.
4. Support technical content and engagement.
5. Support job posting and proposal submission.
6. Rank developers using a weighted score.
7. Provide real-time communication.
8. Integrate generative AI.
9. Integrate online payments.
10. Provide content reporting and moderation.
11. Provide account recovery/deletion lifecycle controls.

---

# 5. Technology Stack

## Backend

| Technology | Role |
|---|---|
| Python | Application language |
| Django 6.0.6 | Web framework |
| Django Channels 4.3.2 | WebSockets/realtime |
| Daphne 4.2.2 | ASGI server |
| SQLite3 | Development database |
| django-environ | Environment variables |
| Pillow 12.2.0 | Image processing/validation |
| Markdown 3.10.2 | Markdown rendering |
| Stripe 15.3.0 | Payment integration |
| google-genai 2.10.0 | Gemini integration |

## Frontend

| Technology | Role |
|---|---|
| Django Templates | Server-rendered HTML |
| Tailwind CSS 4.3.1 | Styling |
| Vanilla JavaScript | AJAX, UI, WebSockets |

---

# 6. Architectural Pattern

The project uses Django's **Model-View-Template (MVT)** approach.

```text
                 ┌───────────────┐
                 │    Browser    │
                 └───────┬───────┘
                         │
                  HTTP / WebSocket
                         │
             ┌───────────▼───────────┐
             │       ASGI/Daphne     │
             └───────────┬───────────┘
                         │
              ┌──────────▼──────────┐
              │ Django routing layer│
              └────┬─────┬─────┬────┘
                   │     │     │
                users   feed  intelligence
                   │     │     │
                   └─────┴─────┴─────┐
                                     │
                              ┌──────▼──────┐
                              │   ORM/DB    │
                              └──────┬──────┘
                                     │
                    ┌────────────────┼────────────────┐
                    │                │                │
                  Gemini           Stripe           SMTP
```

---

# 7. Django applications

## `config`

Contains system-wide configuration:

- `settings.py`;
- root URL routing;
- ASGI;
- WSGI.

## `users`

Handles:

- authentication;
- user profile;
- roles;
- skills;
- projects;
- experience;
- following;
- blocking;
- store;
- subscription/boost logic.

## `feed`

Handles:

- Huddles;
- jobs;
- advertisements;
- comments;
- proposals;
- notifications;
- direct messages;
- bookmarks;
- reports;
- dashboards;
- search;
- moderation.

## `intelligence`

Handles:

- AI reports;
- Gemini calls;
- prompt/context construction;
- 7-day report caching;
- AI report dashboard.

## `communication`

Handles:

- ChatConsumer;
- NotificationConsumer;
- WebSocket routes.

It does not contain the primary database models; persistent message data remains in `feed.models.Message`.

---

# 8. Data Model

The supplied implementation contains 12 primary models.

## `CustomUser`

Extends Django `AbstractUser`.

Important properties:

- username;
- email;
- bio;
- avatar;
- social URLs;
- role;
- tech stack;
- following;
- blocked users;
- premium expiration;
- profile boosts;
- deletion schedule.

### Computed premium state

```python
is_premium
```

is determined from the expiration timestamp.

---

## `Skill`

A reusable skill entity with many-to-many relationships to users.

---

## `Project`

Portfolio project owned by a user.

Contains:

- title;
- description;
- live URL;
- GitHub URL;
- optional image;
- creation date.

---

## `Experience`

Represents a user's professional experience.

Contains:

- company;
- role;
- start date;
- end date;
- current-status flag;
- description.

---

## `Post`

Central content entity.

Supported types:

```text
huddle
job
ad
```

Also contains:

- body;
- image;
- likes;
- deadline;
- target URL;
- tags;
- boost state.

---

## `Comment`

Supports:

- post comments;
- nested replies;
- soft deletion.

The `parent` self-reference enables threaded discussions.

---

## `Proposal`

Connects:

```text
Developer -> Job
```

Contains:

- applicant;
- cover letter;
- bid amount;
- status;
- timestamp.

Statuses:

```text
pending
accepted
rejected
```

The database contains a uniqueness rule so a developer cannot submit multiple applications to the same job.

---

## `Notification`

Represents application-level notifications.

Examples include:

- likes;
- comments;
- follows;
- direct messages;
- proposal decisions;
- premium activation;
- boosts;
- reports;
- moderation events.

A save signal broadcasts new notifications over WebSockets.

---

## `Message`

Persistent direct-message entity.

Contains:

- sender;
- recipient;
- body;
- read state;
- timestamp.

---

## `Bookmark`

Private user-to-post save relation.

A uniqueness rule prevents the same user from bookmarking the same post more than once.

---

## `Report`

Community content report.

Contains:

- reporter;
- post;
- reason;
- resolution status;
- timestamp.

---

## `AIReport`

Stores generated AI output.

It identifies:

- report type;
- requester;
- target user or target post;
- generated content;
- creation time.

---

# 9. User Access Control

## Role matrix

| Function | Developer | Client | Org | Staff/Superuser |
|---|---:|---:|---:|---:|
| Huddle post | Yes | Yes | Yes | Yes |
| Job post | No | Yes | Yes | Yes |
| Ad post | No | Yes | Yes | Yes |
| Apply for job | Yes | No | No | — |
| Developer dashboard | Yes | No | No | — |
| Client dashboard | No | Yes | Yes | — |
| Moderate reports | No | No | No | Yes |
| Edit own content | Yes | Yes | Yes | Yes |

Authorization is implemented through:

- Django authentication;
- `LoginRequiredMixin`;
- `UserPassesTestMixin`;
- explicit role tests;
- ownership checks;
- form restrictions;
- unique DB constraints.

---

# 10. Core User Journeys

## Developer journey

```text
Signup
  ↓
Create profile
  ↓
Add skills
  ↓
Add projects
  ↓
Add experience
  ↓
Follow developers
  ↓
Publish Huddles
  ↓
Browse jobs
  ↓
Apply
  ↓
Receive proposal status
  ↓
Communicate
```

## Client journey

```text
Signup
  ↓
Create profile
  ↓
Publish job
  ↓
Receive proposals
  ↓
Review candidates
  ↓
Accept/reject
  ↓
Communicate
```

---

# 11. Feed Architecture

Home page supports four conceptual feed contexts.

### Fellows

Displays Huddle posts from followed users.

### Business

Displays jobs.

### Ads

Displays advertisements.

### Global

Displays mixed content using engagement ranking.

### Block filtering

Authenticated feeds exclude:

- users blocked by the current user;
- users who have blocked the current user.

---

# 12. Algorithms

## 12.1 Developer ranking

Main weighted structure:

```text
(followers × 2)
+
(projects × 3)
+
(profile_boosts × 7)
+
(premium bonus)
```

Implemented through Django ORM annotation and database-side expressions.

### Design intent

The system rewards:

- social reach;
- portfolio completeness;
- purchased visibility;
- premium participation.

---

## 12.2 Global feed ranking

```text
engagement_score =
    (likes × 2)
    +
    (comments × 3)
```

The feed also gives priority to boosted content.

---

## 12.3 Search

Search covers:

### Users

- username;
- first name;
- last name;
- biography;
- skills.

### Huddles / jobs

- body;
- tags.

User results are follower-ranked; Huddles are engagement-ranked; jobs are recent.

---

# 13. AJAX Layer

The system deliberately does not use Django REST Framework.

Instead, selected operations provide small JSON responses to Vanilla JavaScript.

Examples:

```text
POST /post/like/<pk>/
POST /post/<pk>/bookmark/
POST /post/<pk>/report/
POST /users/follow/<username>/
```

This gives:

- simpler client integration;
- smaller response payloads;
- partial page updates.

---

# 14. Real-Time Layer

## ASGI

`config/asgi.py` routes both:

- HTTP;
- WebSocket.

## WebSocket endpoints

```text
/ws/chat/<username>/
/ws/notifications/
```

## Chat groups

The consumer creates deterministic chat room names based on sorted user IDs.

Conceptually:

```text
chat_<smaller-user-id>_<larger-user-id>
```

## Notification groups

```text
notifications_<user-id>
```

## Channel layer

Current implementation:

```text
InMemoryChannelLayer
```

Recommended production direction:

```text
Redis / shared channel backend
```

---

# 15. Signal Architecture

Signals are used for automatic side effects.

## Users signals

- delete old/new avatars where necessary;
- create welcome notifications;
- cancel deletion when the user logs back in.

## Feed signals

- delete old post images;
- broadcast newly-created notifications over WebSockets.

This is useful because business logic such as notification broadcasting does not have to be duplicated in every UI action.

---

# 16. AI Architecture

```text
User
 ↓
Analyzer View
 ↓
DevHuddleAIEngine
 ↓
Check 7-day cache
 ├── valid → return cached report
 └── expired/missing
       ↓
Build structured context
       ↓
Gemini API
       ↓
Fallback model on failure
       ↓
Save AIReport
       ↓
Render Markdown
```

The service acts as a facade over the external AI provider.

---

# 17. AI Profile Analysis

Context includes:

```text
identity
network
expertise
```

The AI prompt requests:

- Core Identity & Strengths;
- Areas for Growth;
- Market Viability.

---

# 18. AI Post Analysis

Context includes:

```text
post
author
engagement
```

The AI prompt requests:

- Technical Breakdown;
- Engagement Analysis;
- Suggested Follow-up.

---

# 19. AI Caching

A recent report may be reused for up to **7 days**.

Benefits:

- fewer external API calls;
- lower quota consumption;
- faster repeated views.

---

# 20. Payment Architecture

Stripe is used via hosted Checkout.

Products encoded in the backend currently include:

```text
premium
boost_1
boost_5
```

The server creates a Checkout Session, redirects the user to Stripe, then retrieves the session from Stripe before fulfilling a paid order.

### Important design point

The application checks:

```text
payment_status == "paid"
```

before granting premium/boost benefits.

---

# 21. Account Deletion Architecture

A deletion request sets:

```text
deletion_scheduled_at
```

to three days in the future.

A later login cancels the schedule.

The command:

```text
python manage.py sweep_accounts
```

permanently deletes accounts whose grace period has expired.

---

# 22. Media Handling

User and post uploads are stored under:

```text
media/
```

Examples:

```text
media/avatar/
media/post/
media/projects/
```

Image validation includes:

- size limit;
- extension restrictions.

### Production recommendation

Use managed object storage/CDN rather than local disk when scaling.

---

# 23. Security Implementation

Present features include:

- CSRF middleware;
- session authentication;
- password validation;
- role-based authorization;
- object ownership checks;
- file validation;
- server-side payment verification;
- report/moderation system;
- blocking;
- secret values expected through `.env`;
- unique database constraints.

---

# 24. Security Gaps Found in the Supplied Source

The following should be described honestly.

### Development configuration

Current source contains:

```text
DEBUG = True
ALLOWED_HOSTS = ["*"]
```

### Hard-coded secret

A Django `SECRET_KEY` is present directly in `config/settings.py`.

This should be moved to an environment variable before public deployment.

### Database

SQLite is adequate for a small local demo but is not the preferred production database for a scalable application.

### WebSocket scaling

The in-memory channel layer is not the right shared backend for horizontally scaled instances.

### Automated testing

The supplied repository contains no `tests.py` / `test_*.py` files.

### Payment architecture

A stronger production implementation should include:

- webhook-based fulfillment;
- idempotency/order records;
- protection against repeated fulfillment.

### AI availability

External model identifiers/API availability must be verified before a demo.

### Notification verb consistency

The source contains an AI notification creation path using `verb="ai"` while the visible `Notification.VERB_CHOICES` list does not contain `ai`. This should be fixed/tested before relying on the AI notification path.

---

# 25. API-style endpoints

DevHuddle is primarily server-rendered and does not provide a full REST API.

Important JSON endpoints include:

```text
POST /post/like/<pk>/
POST /post/<pk>/bookmark/
POST /post/<pk>/report/
POST /users/follow/<username>/
```

---

# 26. Important HTTP routes

## Users

```text
/users/login/
/users/logout/
/users/signup/
/users/password-reset/
/users/edit/
/users/delete/
/users/profile/<username>/
/users/developers/
/users/store/
/users/store/checkout/
/users/store/checkout/success/
```

## Feed

```text
/
/about/
/documentation/
/post/new/
/post/<pk>/
/post/<pk>/edit/
/post/<pk>/delete/
/search/
/notifications/
/explore/
/support/
/job/<pk>/apply/
/dashboard/client/
/dashboard/dev/
/inbox/
/moderation/
```

## AI

```text
/ai/dashboard/
/ai/analyze/profile/<username>/
/ai/analyze/post/<pk>/
/ai/delete/<pk>/
```

---

# 27. Frontend JavaScript modules

| File | Responsibility |
|---|---|
| `interactions.js` | interaction-related AJAX/UI |
| `websockets.js` | chat + notifications |
| `follow_logic.js` | follow/unfollow |
| `menu_toggle.js` | menus/dropdowns |
| `feed_controller.js` | feed UI |
| `post_upload_validator.js` | client-side upload validation |
| `searching.js` | UI search-related behavior |

---

# 28. Template organization

The project uses reusable template sections and components.

Main structure:

```text
templates/
├── base.html
├── pages/
├── components/
├── sections/
├── users/
└── intelligence/
```

This reduces duplication and centralizes shared UI.

---

# 29. Database and business-rule examples

### Duplicate proposals

Database uniqueness:

```text
(job, applicant)
```

### Duplicate bookmarks

Database uniqueness:

```text
(user, post)
```

### Role restrictions

Enforced in views/forms.

### Object ownership

Examples:

- only project owner can edit;
- only post author can edit;
- only the job owner can accept/reject its proposals;
- only the report requester can delete an AI report.

---

# 30. Testing status of supplied project

Based on repository inspection:

| Test type | State |
|---|---|
| Unit tests | Not present |
| Integration tests | Not present |
| E2E tests | Not present |
| Manual testing | Used during development |
| NPM automated test command | Placeholder |

### Recommended minimum before final submission

Manually validate every critical user journey and create a test-case document containing:

```text
Test ID
Feature
Precondition
Steps
Expected result
Actual result
Pass/Fail
```

---

# 31. Deployment direction

A production architecture should become:

```text
Browser
  ↓ HTTPS
Reverse Proxy / Load Balancer
  ↓
Django ASGI
  ↓
PostgreSQL
Redis
Object Storage
  ↓
Gemini
Stripe
Email Provider
```

With:

- `DEBUG=False`;
- strict hosts;
- secret management;
- HTTPS;
- database backups;
- logging;
- monitoring;
- CI/CD;
- automated tests.

---

# 32. Known limitations

1. No full REST API.
2. SQLite development database.
3. In-memory Channels backend.
4. No automated test suite.
5. Development-oriented security settings remain.
6. Local media storage.
7. Payment fulfillment needs stronger production-grade idempotency/webhook handling.
8. AI provider availability is external.
9. Some notification/AI paths need consistency testing.
10. Production deployment infrastructure is not part of the current FYP scope.

---

# 33. Future enhancements

High-value next steps:

- PostgreSQL migration;
- Redis;
- REST/GraphQL API;
- automated tests;
- CI/CD;
- stronger RBAC;
- moderation analytics;
- recruiter/client premium tooling;
- transaction-fee marketplace;
- recommendation engine;
- better AI personalization;
- email notification management;
- object storage/CDN;
- audit logs;
- observability;
- rate limiting;
- stronger content sanitization;
- production payment webhooks.

---

# 34. Recommended presentation message

> "DevHuddle demonstrates an end-to-end software product architecture in which social networking, professional identity, job-marketplace workflows, real-time messaging, AI services, payments, and moderation are implemented within a modular Django application. The project deliberately separates current FYP functionality from the hardening required for a production deployment."

---

# 35. Reference material

Official technical guidance used when preparing the engineering recommendations:

- Django deployment checklist: https://docs.djangoproject.com/en/6.1/howto/deployment/checklist/
- GitHub guidance for sensitive data: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository
- WIPO copyright FAQ: https://www.wipo.int/en/web/copyright/faq-copyright
- WIPO copyright protection overview: https://www.wipo.int/en/web/copyright/protection
