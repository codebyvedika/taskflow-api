# TaskFlow API

**Live api**: https://taskflow-api-1-r9ex.onrender.com/docs


A team task and project management API — organize work into projects, track tasks through a status workflow, collaborate via comments, and see a full audit trail of everything that happened on a task.

## What This Solves

Every team that ships work needs the same core loop: create a project, break it into tasks, assign and prioritize them, move them through stages (todo → in progress → review → done), and communicate about them. This project implements that loop cleanly — the foundation behind tools like Trello, Linear, or Asana.

## Features

- Projects — create, update, delete; live stats (total tasks, completed tasks) computed on read
- Tasks — full CRUD, with status workflow (todo → in_progress → in_review → done) and priority levels (low/medium/high/urgent)
- Filtering — list tasks by status or priority within a project
- Comments — threaded discussion per task
- Activity Feed — every task creation, status change, field update, and comment is automatically logged with a timestamp
- Cascade Deletes — deleting a project cleanly removes its tasks (and their comments/activity)
- Tested — Pytest suite covering projects, task workflow, comments, and the activity log

## Tech Stack

| Layer | Technology |
|---|---|
| Framework | FastAPI |
| Database | PostgreSQL + SQLAlchemy 2.0 |
| Testing | Pytest + SQLite in-memory DB |

## Setup Instructions

    python -m venv venv
    venv\Scripts\activate
    pip install -r requirements.txt
    cp .env.example .env
    uvicorn app.main:app --reload

API live at http://localhost:8000,docs at http://localhost:8000/docs.

A Dockerfile is also included for containerized deployment.

## Running Tests

    pytest -v

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | /api/v1/projects | Create a project |
| GET | /api/v1/projects | List projects |
| GET | /api/v1/projects/{id} | Get project + task stats |
| PATCH | /api/v1/projects/{id} | Update a project |
| DELETE | /api/v1/projects/{id} | Delete a project (cascades) |
| POST | /api/v1/projects/{id}/tasks | Create a task in a project |
| GET | /api/v1/projects/{id}/tasks | List tasks (filter by status/priority) |
| GET | /api/v1/tasks/{id} | Get a task |
| PATCH | /api/v1/tasks/{id} | Update task fields |
| PATCH | /api/v1/tasks/{id}/status | Move task through the workflow |
| DELETE | /api/v1/tasks/{id} | Delete a task |
| POST | /api/v1/tasks/{id}/comments | Add a comment |
| GET | /api/v1/tasks/{id}/comments | List comments |
| GET | /api/v1/tasks/{id}/activity | Full activity feed for the task |

Full interactive docs at /docs.

## Design Notes

- Activity logging is centralized (app/services/activity.py) and called from each route after a mutation.
- Stats are computed on read, not cached, so total_tasks/done_tasks are always accurate.
- Cascade deletes are defined at the ORM relationship level, so deleting a project or task automatically cleans up its children.

## Possible Extensions

- WebSocket-based live updates when a task changes (real-time board view)
- User accounts and per-user task assignment (reuse the RBAC pattern from the SecureAuth API project)
- File attachments on tasks
- Kanban-style drag-and-drop ordering