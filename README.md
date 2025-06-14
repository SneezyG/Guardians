# Guardians – Crisis Alert & Safety Management System

**Guardians** is a real-time crisis response platform for organizations, combining location-aware alerts, multi-channel notifications, and an admin dashboard. Built to demonstrate advanced backend architecture, system design, and full-stack integration.

---

## 🚨 Core Features

- **Real-Time Alerts**: WebSocket-based instant updates.
- **Multi-Channel Notifications**: Web, Email, SMS.
- **Zone-Based Location Tracking**: Live tracking with predefined geo-boundaries.
- **Audit Trail**: Tracks all alert activities for transparency.
- **Automatic Escalation**: Time-based escalation logic.
- **Embedded Safety Tips**: In-app safety recommendations.
- **Admin Interface**: Manage alerts, users, roles, and safety tips.

---

## 🏗️ System Architecture

**Frontend (React):**
- Real-time UI with WebSockets.
- Mobile-responsive dashboard.
- Storybook-driven UI documentation.

**Backend (Python/Django):**
- RESTful API with JWT authentication.
- PostgreSQL for data storage.
- Celery + Redis for async notifications.
- WebSockets for alert and location updates.

---

## 🔐 Security Highlights

- **Role-Based Access Control (RBAC)**
- **JWT Authentication** (short-lived tokens + refresh)
- **Input Sanitization** & CSRF/XSS Protection
- **WebSocket Authentication**
- **Rate-Limiting & IP Whitelisting** for admin endpoints
- **CORS Restrictions** for trusted frontend origins

---

## 🧪 Testing & Documentation

- **Unit/Integration Testing**: `pytest`, `Jest`, Postman
- **API Docs**: `drf-spectacular` (OpenAPI)
- **UI Docs**: `Storybook` (React Components)

---

## 🚀 DevOps & Deployment

- **Dockerized**: Isolated service containers
- **CI/CD**: GitHub Actions for automated builds/tests
- **Monitoring**: Prometheus, Grafana, and Logstash
- **Cloud-Ready**: Scalable for production environments

---

## 📂 API Highlights

| Method | Endpoint                   | Description                    |
|--------|----------------------------|--------------------------------|
| POST   | `/alerts/create`           | Create a new alert             |
| GET    | `/alerts/latest`           | Get today's alerts             |
| PUT    | `/alerts/{id}/update`      | Update a specific alert        |
| POST   | `/auth/token`              | JWT login                      |
| GET    | `/audit`                   | Search audit logs              |
| GET    | `/safety_tips`             | Fetch current safety tips      |
| WS     | `/ws/alerts`               | Real-time alert channel        |

---

## 📌 Data Modeling (Simplified)

- **Users**: Roles, contact info, login history
- **Alerts**: Severity, status, location, history
- **Notifications**: Linked to alerts & users
- **Audit Logs**: Track all actions on alerts
- **Safety Tips**: Categorized prevention messages

---

> 🔍 Built with enterprise-grade scalability, real-time systems, and safety in mind.
