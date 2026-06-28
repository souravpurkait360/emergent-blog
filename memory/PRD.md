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

## What's Been Implemented (June 28, 2026)

### Backend (Django DRF)
- Custom User model with roles (admin/author/reader)
- JWT authentication with djangorestframework-simplejwt
- Post model with slug, cover image, categories, tags, ai_summary
- Comment model with author/post relationships
- Category and Tag models with auto-slug generation
- AI endpoints: /api/ai/assist/ and /api/ai/summarize/
- Media file serving at /api/media/
- Pagination (9 posts per page)
- Admin Django panel at /api/admin/
- Automatic migrations on startup via subprocess

### Frontend (React)
- Swiss & High-Contrast design (Outfit + IBM Plex Sans fonts)
- Hero section with search
- Bento-style asymmetric post grid
- Category filter buttons
- Rich text editor (contenteditable with toolbar)
- Post detail with AI summary block
- Comment section with add/delete
- Auth page (login/register tabs)
- Profile page with stats and posts list
- Admin dashboard (posts/users/categories tabs)
- Framer Motion animations

### Sample Data
- 4 categories: Technology, Design, Writing, Business
- 6 tags: python, django, react, css, ai, productivity
- 3 sample posts from admin user

## Admin Credentials
- Email: admin@blog.com
- Password: admin123

## P0 Backlog (Critical)
- [ ] Password reset functionality
- [ ] User avatar upload
- [ ] Post read time estimate

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

## Next Tasks
1. Add post read time calculation
2. Add SEO meta tags
3. Implement password reset via email
4. Add post bookmarking feature
5. Add related posts to post detail page
