# INKFLOW Blog Platform - PRD

## Overview
A full-stack blog application built with Django DRF (backend), React (frontend), and PostgreSQL (database). Named "INKFLOW", it's a premium editorial writing platform.

## Architecture
- **Backend**: Django 5.2 + Django REST Framework + PostgreSQL
- **Frontend**: React 19 + Tailwind CSS + Framer Motion
- **Database**: PostgreSQL 15
- **AI**: OpenAI gpt-5.4 via Emergent LLM key
- **Auth**: JWT via djangorestframework-simplejwt
- **Server**: Uvicorn (ASGI) running Django

## User Personas
- **Admin**: Full platform control (manage users, posts, categories)
- **Author/Reader**: Create, edit, comment on posts

## Core Requirements (Static)
1. User authentication (register/login/logout)
2. Blog post CRUD with rich text editor
3. Categories and Tags for posts
4. Comments system
5. Search and category filtering
6. AI writing assistance and summarization
7. Cover image upload
8. Multiple user roles (admin, author, reader)
9. Pagination for post listings
10. Admin dashboard

## What's Been Implemented (June 28, 2026) — v2 Architectural Refactor

### Backend (4-layer Architecture)
- Refactored to strict API View → Service → Repository → Serializer layers
- Apps: core, accounts, posts, ai (each with their own API/service/repository/serializer dirs)
- Cookie-based JWT authentication (CookieJWTAuthentication) — httpOnly cookies, no localStorage
- Login/register set httpOnly cookies; /auth/me/ restores session on init
- Ruff linting config in pyproject.toml (E, W, F, I, B, N, UP, SIM rules enforced)

### Frontend (Zustand + HTTPOnly Cookies)
- Migrated from AuthContext/localStorage to Zustand useAuthStore + httpOnly cookies
- Auth.js, PostDetail.js, Profile.js, CommentSection.js all use useAuthStore
- CSS compilation fixed: @import moved before @tailwind directives; @layer removed from App.css
- Tailwind design tokens: canvas, surface, ink, accent, edge, wash configured

## P0 Backlog (Critical)
- [ ] Password reset functionality
- [ ] User avatar upload
- [ ] Post read time estimate
- [x] Ruff: run ruff check . --fix and format — DONE (0 violations)

## P1 Backlog (Important)
- [ ] Post bookmarking/favorites
- [ ] Email notifications for comments
- [ ] Related posts section
- [ ] Social sharing buttons
- [ ] SEO meta tags per post

## P2 Backlog (Nice to have)
- [ ] Markdown support option in editor
- [ ] Post series/collections
- [ ] Author follow system
- [ ] Newsletter subscription
- [ ] Analytics dashboard for authors
- [ ] Multiple image attachments per post
