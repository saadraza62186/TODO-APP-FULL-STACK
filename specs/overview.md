# Todo App Overview

## Purpose
A todo application that evolves from console app to AI chatbot through three phases of development.

## Current Phase
**Phase II: Full-Stack Web Application**

## Tech Stack
- **Frontend**: Next.js 16+ (App Router), TypeScript, Tailwind CSS
- **Backend**: FastAPI, SQLModel, Neon PostgreSQL
- **Auth**: Better Auth with JWT tokens
- **ORM**: SQLModel
- **Database**: Neon Serverless PostgreSQL

## Features
- [x] Task CRUD operations
- [x] User authentication (Better Auth)
- [x] JWT-based API security
- [x] Multi-user support with data isolation
- [ ] Task filtering and sorting
- [ ] AI chatbot interface (Phase III)

## Architecture Overview
This is a monorepo with separate frontend and backend services:
- Frontend runs on port 3000 (Next.js)
- Backend runs on port 8000 (FastAPI)
- Communication via REST API with JWT authentication

## Security Model
- Better Auth handles user authentication on frontend
- JWT tokens issued on login
- Backend verifies JWT on every API request
- User data isolation enforced at API level
