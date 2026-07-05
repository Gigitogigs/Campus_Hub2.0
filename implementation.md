# Campus Hub — Implementation Plan
**Mode:** Solo build, a few hours at a time, no fixed dates — loose sprints, sequenced by dependency
**Target:** Working MVP (Events tab) by end of 2026
**Your profile:** Django/DRF — solid. React Native — starting from zero (new to JS/React too).

This document maps the *entire* build, not just Phase 1. Read it once fully, then we work through it sprint by sprint. Each sprint has a goal, tasks, and a "done when" checkpoint so you always know where you stand.

---

## How This Plan Is Structured

The backend comes first, start to finish, before any React Native work begins. You're solid on Django/DRF — that's your strength and your fastest path to a working, testable core. Once the entire API (auth, orgs, posts) is built and verified via Postman, you'll have a fully functional backend you can reason about independently of the frontend.

React Native — including the learning curve — starts only after the backend is done. That's a deliberate sequencing choice: you're learning JS, React, and RN from scratch, and mixing that learning curve with backend work would mean debugging two unfamiliar things at once. Finishing the backend first also means the RN learning sprint has a real, working API to practice against instead of a placeholder.

Everything is grouped into **Phases** (major milestones) → **Sprints** (chunks of focused work, no calendar dates — you move to the next sprint when the current one's "done when" is true).

---

## PHASE 0 — Backend Foundations

### Sprint 0.1: Environment & Project Skeleton
**Goal:** Django project running fully locally first — deployment comes only after the local build works end-to-end.

- [ ] Set up Django project + DRF
- [ ] Configure PostgreSQL locally
- [ ] Set up `.env` config for secrets (don't hardcode DB creds) — do this now even for local, so deployment later is just swapping env values, not restructuring config
- [ ] Confirm a "Hello World" endpoint responds on `localhost`
- [ ] Push to GitHub (version control from day one, deploy pipeline comes later)

**Done when:** You can hit a working API endpoint on localhost, with Postgres reading/writing correctly.

**Deployment (Railway/Render/Supabase — you already have accounts) is deliberately deferred.** We connect the deploy pipeline once the local build is solid — this avoids debugging deployment issues and Django issues at the same time. Revisit this once the backend (Phase 0 + Phase 1 API work) is complete and you need it reachable from a phone/emulator.

---

### Sprint 0.2: Django Data Models (Full Schema from the Requirements Doc)
**Goal:** All Phase 1 models built, migrated, and testable via Django Admin.

- [ ] `users_pii` / `users_public` split (custom user model)
- [ ] `organizations` model
- [ ] `organization_members` model
- [ ] `posts` model (with `type` enum ready for future Marketplace)
- [ ] `follows`, `saved_posts` models
- [ ] `user_actions` model (write-only, no logic yet — just the table)
- [ ] Django Admin registered for all models so you can manually test data by hand before the API exists

**Done when:** You can create a student, an org, and a post entirely through Django Admin and see the relationships hold correctly.

---

## PHASE 1 — Events API (Full Backend)

### Sprint 1.1: Auth API
**Goal:** Signup, email verification, login all work end-to-end via API (test with Postman/Insomnia, not the app yet).

- [ ] Signup endpoint (creates `users_pii` + `users_public`)
- [ ] Email verification (6-digit code, expiry, resend)
- [ ] Login (JWT issue)
- [ ] Token refresh
- [ ] Password reset flow

**Done when:** You can sign up, verify, log in, and get a valid JWT — fully tested via Postman.

---

### Sprint 1.2: Organizations API
- [ ] Create org (creator becomes admin)
- [ ] List/search/filter orgs by category
- [ ] Org detail view
- [ ] Follow/unfollow endpoints

**Done when:** A student can create an org and another student can follow it, verified via Postman.

---

### Sprint 1.3: Posts (Events) API
- [ ] Create post (org admin only — permission check matters here)
- [ ] Feed endpoint (following + discover, filterable by category)
- [ ] Post detail
- [ ] Edit/delete (admin only)
- [ ] Save/unsave post

**Done when:** Full event lifecycle works via API: an org posts an event, a student sees it in their feed, saves it.

**Backend is now complete.** Every endpoint from the requirements doc is built and verified via Postman. Everything from here on is frontend work — the RN learning sprint below is where that starts.

---

## PHASE 2 — React Native (Frontend)

### Sprint 2.1: React Native — Deliberate Learning Sprint
**Goal:** Get comfortable enough with JS + React + RN fundamentals to build simple screens without fighting the language itself.

This is *not* Campus Hub work yet — it's a dedicated skill sprint, and it's on you to work through it at your own pace. Suggested path:

- [ ] JS fundamentals refresher (variables, functions, arrays/objects, async/await, promises) — you'll use these constantly
- [ ] React core concepts: components, props, state (`useState`), effects (`useEffect`)
- [ ] React Native basics: `View`, `Text`, `FlatList`, `TouchableOpacity`, navigation (`react-navigation`)
- [ ] Build ONE throwaway practice app: a simple list screen that fetches data from a public API and displays it (this mirrors exactly what your Events feed will do) — you now have a real backend to practice against instead of a placeholder API

**Done when:** You can build a screen that fetches JSON from an API and renders it in a scrollable list, from memory, without copy-pasting.

**Open decision, doesn't affect the backend at all:** Expo vs. bare React Native. This only matters once you're actually starting RN, so it's fine to leave undecided until you get here.

---

### Sprint 2.2: RN Scaffold + Auth Screens
**Goal:** Now we connect the app to your live API for the first time.

- [ ] RN project setup, navigation structure
- [ ] API client (axios/fetch wrapper with token handling)
- [ ] Signup screen → hits real signup endpoint
- [ ] Email verification screen
- [ ] Login screen
- [ ] Token storage (secure storage, not plain state) + auto-login on app reopen

**Done when:** You can sign up and log in on your phone/emulator using the real backend.

---

### Sprint 2.3: Feed & Post Detail Screens
- [ ] Home feed screen (FlatList of events, following + discover sections)
- [ ] Category filter UI
- [ ] Post detail screen
- [ ] Save/bookmark button wired to API

**Done when:** You can scroll a real event feed pulled from your database on your phone.

---

### Sprint 2.4: Org Directory, Org Profile, Create Org/Post Screens
- [ ] Org directory (search + filter)
- [ ] Org profile screen (their events)
- [ ] Create org form
- [ ] Create post form (for org admins)

**Done when:** An org can be created and post an event, entirely from the app, no admin panel needed.

---

### Sprint 2.5: Search, Profile, Polish
- [ ] Unified search (orgs + events)
- [ ] Own profile screen (saved events, orgs managed/followed)
- [ ] Basic empty states, loading states, error handling
- [ ] App icon, splash screen, basic branding pass

**Done when:** The app feels like a real product, not a prototype — no dead-end screens or unhandled errors.

---

### Sprint 2.6: Internal Beta
**Goal:** Real students use it, not just you.

- [ ] Deploy backend to production-grade free tier
- [ ] Distribute app via TestFlight (iOS) / internal APK (Android) or Expo Go link
- [ ] Recruit a small group (5–15 students) at Kenyatta University — ideally a mix of regular students and a couple of club leaders
- [ ] Collect feedback: Is the feed useful? Do orgs actually post? Is signup friction too high?
- [ ] Fix critical bugs surfaced by real usage

**Done when:** At least one real club has posted a real event, and at least a few real students engaged with it (viewed/saved).

**This is your MVP finish line.** Phase 1 + 2 complete = you have a working, tested, real-world-validated Events product.

---

## PHASE 3 — Marketplace (After MVP Validation)

Not detailed sprint-by-sprint yet — sketched at a high level so you see what's coming. We'll break this down fully once the MVP is live and validated.

- Extend `posts` model: add `product` / `service` type with price, condition, availability fields
- Seller profile enhancements (ratings/reviews — decide if MVP-worthy or later)
- Marketplace-specific feed (separate from Events, or a toggle on the same feed — decision pending your beta feedback)
- "Contact seller" flow (off-platform: WhatsApp link, no in-app payment per your business model)
- Category taxonomy for goods/services distinct from event categories

**Key decision point before starting Phase 3:** Does MVP beta feedback suggest students want Marketplace inside the same app, or would splitting attention hurt the Events product? Revisit based on real data.

---

## PHASE 4 — Data & Monetization Layer (Post-Traction)

Not for MVP. Only relevant once you have real usage volume. Sketched for context so the schema decisions you're making now don't box you in later:

- Activate `user_actions` querying (currently just logging, unused)
- Build anonymized aggregation queries (never touching `users_pii`)
- Campus Pulse Reports (B2B insight reports)
- Ad placement system (sponsored posts in feed)
- University Admin verified channel (schema already supports adding this role)

---

## Cross-Cutting Concerns (Apply Throughout, Not a Separate Phase)

- **Data separation discipline:** Every time you add a feature, check — does this touch PII? If yes, it must go through `users_public`/`anonymized_id`, never direct joins to `users_pii`.
- **Git hygiene:** Feature branches, even solo — makes it easier to roll back when RN or Django surprises you.
- **Testing:** Not full test coverage for MVP, but at minimum: manual Postman testing for every API endpoint before building the screen that uses it. This isolates whether a bug is backend or frontend.
- **Scope discipline:** When you get an idea for a new feature mid-build (you will), write it in a `future_ideas.md` file and keep moving. Scope creep is the #1 killer of solo MVPs.

---

## Suggested Order of Operations (Summary)

```
0.1 Setup → 0.2 Django Models
  → 1.1 Auth API → 1.2 Orgs API → 1.3 Posts API   [BACKEND COMPLETE]
  → 2.1 Learn RN → 2.2 RN Auth Screens → 2.3 Feed → 2.4 Org/Post Screens → 2.5 Polish
  → 2.6 Internal Beta with real students   [MVP COMPLETE]
  → [VALIDATE] → Phase 3 Marketplace → Phase 4 Data/Monetization
```

---

## Open Questions for You (Answer When Ready — No Rush)

1. For beta testers in Sprint 2.6 — do you already know specific club leaders you'd recruit, or do we need a plan for finding them?
2. Expo vs. bare React Native — no need to decide now, this only matters once you reach Sprint 2.1.
