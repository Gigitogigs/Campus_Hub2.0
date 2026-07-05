# Campus Hub — MVP Requirements Document
**Phase 1 Scope: Events Tab + Foundation**
**Stack:** Django + Django REST Framework (backend), PostgreSQL (database), React Native (mobile)

---

## 1. Project Overview

Campus Hub is a student-only mobile platform that centralizes campus communication and discovery. Phase 1 builds the foundation (auth, accounts, orgs) and the **Events tab** — a unified timeline where verified organizations, clubs, and groups post announcements and events to the student body.

The platform is 100% free for students. Revenue comes later from anonymized data insights and B2B advertising — meaning the database must separate **PII** from **user actions** from day one, even though analytics/ads are not built in this phase.

---

## 2. User Roles

| Role | Description | Permissions |
|---|---|---|
| **Student (Individual)** | Default account for any verified student | Browse, search, RSVP/save events, follow orgs. Cannot post. |
| **Organization / Club / Group** | Created by a student, represents an entity | Post events, edit own posts, manage own follower base |
| **University Admin** *(scaffold only, not active in MVP)* | Reserved role for future verified official channel | Not built in Phase 1, but schema must allow adding it later without migration pain |

**Note:** A student account can create and manage one or more Organization accounts (e.g., a student runs both their personal account and their club's account).

---

## 3. Functional Requirements

### 3.1 Authentication & Onboarding
- Student signs up with **university email** (e.g., `@students.ku.ac.ke` or similar domain)
- Email verification via 6-digit code sent to inbox (no ID upload in MVP — deferred to post-launch)
- Signup collects: full name, university email, password, year of study, course/department
- Login via email + password
- Password reset flow (email-based)
- JWT-based session auth (mobile-friendly, stateless)

### 3.2 Account Management
- Student can create an **Organization/Club/Group profile** from their account
  - Fields: name, type (org/club/group), description, logo/cover image, category (e.g., Sports, Tech, Faith, Business)
  - Creator becomes the default admin of that org
- Org profile is publicly viewable by all students
- Student can follow/unfollow orgs
- Student can edit their own personal profile (name, year, course, profile picture)

### 3.3 Events Tab (Core Feature)
- **Unified timeline** — shows events from all orgs the student follows, plus a "Discover" section for orgs they don't follow yet
- Only Organization/Club/Group accounts can create posts (individuals cannot post)
- **Event Post fields:**
  - Title
  - Description
  - Cover image (single image for MVP)
  - Date & time
  - Location (free text for MVP — no map integration yet)
  - Category/tag (e.g., Workshop, Social, Sports, Career)
  - Posted by (org reference)
- Students can:
  - View event feed (chronological, most recent first)
  - Tap into an event for full details
  - Save/bookmark an event
  - Filter feed by category
  - Search events by keyword
- Org can:
  - Create, edit, delete their own posts
  - View basic post count (no analytics dashboard in MVP)

### 3.4 Discovery
- Students can browse a directory of all Organizations/Clubs/Groups (searchable, filterable by category)
- Students can view an org's profile page showing their upcoming and past events

---

## 4. Non-Functional Requirements

- **Free-tier deployable:** Must run on free/low-cost infrastructure initially (e.g., Railway, Render, or AWS free tier for Django; free tier Postgres instance)
- **Data separation is mandatory, not optional:** PII must live separately from behavioral/action data, even if analytics isn't built yet — retrofitting this later is expensive
- **Mobile-first, offline-tolerant UI:** Feed should cache last-loaded content for poor connectivity (common on campus Wi-Fi/data)
- **Fast to ship:** No payment integration, no ID-verification pipeline, no map/geolocation in Phase 1
- **Scalable schema:** Adding Marketplace and University Admin roles later should not require breaking changes

---

## 5. Data Architecture

```
users_pii
├─ id (UUID, PK)
├─ full_name
├─ university_email (unique)
├─ password_hash
├─ phone (optional)
├─ created_at

users_public
├─ id (UUID, PK)
├─ pii_id (FK → users_pii, write-only reference, never joined in analytics queries)
├─ anonymized_id (UUID, used for tracking — decoupled identifier)
├─ username / display_name
├─ year_of_study
├─ course
├─ profile_image_url
├─ created_at

organizations
├─ id (UUID, PK)
├─ name
├─ type (enum: club, group, organization)
├─ category (enum: sports, tech, faith, business, arts, other)
├─ description
├─ logo_url
├─ cover_image_url
├─ created_by (FK → users_public)
├─ created_at

organization_members
├─ id (PK)
├─ organization_id (FK)
├─ user_id (FK → users_public)
├─ role (admin, member) — admin can post, member cannot (MVP: only admin used)

posts
├─ id (UUID, PK)
├─ organization_id (FK → organizations)
├─ type (enum: event) — kept as enum now so 'product'/'service' can be added later for Marketplace without schema change
├─ title
├─ description
├─ image_url
├─ event_date
├─ location_text
├─ category
├─ created_at
├─ updated_at

follows
├─ id (PK)
├─ user_id (FK → users_public)
├─ organization_id (FK → organizations)
├─ created_at

saved_posts
├─ id (PK)
├─ user_id (FK → users_public)
├─ post_id (FK → posts)
├─ created_at

user_actions  (write-only log, not queried in MVP but captured from day one)
├─ id (PK)
├─ anonymized_id (FK → users_public.anonymized_id)
├─ action_type (enum: viewed_post, followed_org, saved_post, searched)
├─ metadata (JSON — e.g., {"post_id": ..., "category": ...})
├─ timestamp
```

**Key rule:** No API endpoint or query should ever join `users_pii` directly to `posts`, `user_actions`, or any engagement table. All engagement is tied through `users_public.anonymized_id`.

---

## 6. API Endpoints (Phase 1 Scope)

### Auth
- `POST /api/auth/signup/`
- `POST /api/auth/verify-email/`
- `POST /api/auth/login/`
- `POST /api/auth/password-reset/`
- `POST /api/auth/token/refresh/`

### Users
- `GET /api/users/me/`
- `PATCH /api/users/me/`

### Organizations
- `POST /api/organizations/` (create org — becomes admin)
- `GET /api/organizations/` (list/search/filter by category)
- `GET /api/organizations/{id}/`
- `PATCH /api/organizations/{id}/` (admin only)
- `POST /api/organizations/{id}/follow/`
- `DELETE /api/organizations/{id}/follow/`

### Posts (Events)
- `POST /api/posts/` (org admin only)
- `GET /api/posts/` (feed — filterable by category, org, following-only)
- `GET /api/posts/{id}/`
- `PATCH /api/posts/{id}/` (org admin only)
- `DELETE /api/posts/{id}/` (org admin only)
- `POST /api/posts/{id}/save/`
- `DELETE /api/posts/{id}/save/`

### Search
- `GET /api/search/organizations/?q=`
- `GET /api/search/posts/?q=&category=`

---

## 7. Mobile App Screens (React Native)

1. **Splash / Onboarding** — value prop screens
2. **Signup** — email, password, name, year, course
3. **Email Verification** — 6-digit code input
4. **Login**
5. **Home Feed** — Events timeline (following + discover)
6. **Post Detail** — full event view, save button
7. **Org Directory** — searchable/filterable list of all orgs
8. **Org Profile** — org info + their events
9. **Create Org** — form for students to register a club/group/org
10. **Create Post** — form for org admins to post an event
11. **Profile** — own profile, saved events, orgs managed/followed
12. **Search** — unified search bar (orgs + events)

---

## 8. Explicitly Out of Scope for Phase 1

- Marketplace (products/services)
- ID/document verification pipeline
- Payments or transaction handling of any kind
- Map/geolocation integration
- Push notifications (nice-to-have, not blocking)
- Analytics dashboard / ad platform / Campus Pulse Reports
- University Admin active role (schema-ready only)
- Multi-image posts, video, or rich media beyond single cover image

---

## 9. Build Order

1. Django project setup + PostgreSQL config + free-tier deployment pipeline
2. `users_pii` / `users_public` models + auth (signup, email verification, login, JWT)
3. `organizations` model + create/list/follow endpoints
4. `posts` model + create/list/filter/save endpoints
5. `user_actions` logging middleware (fire-and-forget, no queries needed yet)
6. React Native scaffold: navigation, auth screens, API client
7. Feed screen + Post Detail screen
8. Org Directory + Org Profile screens
9. Create Org + Create Post screens (org admin flows)
10. Search + Profile screens
11. Internal test with a small group of real students at Kenyatta University
12. Iterate → begin Marketplace (Phase 2)
