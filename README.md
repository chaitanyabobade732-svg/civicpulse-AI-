# CivicPulse AI 🇮🇳
### AI-Powered Civic Intelligence & Public Grievance Resolution Platform for India
> *"Every Complaint Matters. Every Action Counts."*

[![Python](https://img.shields.io/badge/Python-3.14+-3776AB?logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.1+-000000?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-39FF88)](LICENSE)
[![Theme](https://img.shields.io/badge/Theme-Black%20%7C%20Neon%20Green%20%7C%20Alert%20Red-141816)]()

---

## 🏛️ Executive Summary

**CivicPulse AI** is a centralized public grievance redressal and civic intelligence platform built specifically for Indian public infrastructure and municipal administration. The platform empowers citizens to report civic problems—such as potholes, open manholes, exposed live wiring, pipeline bursts, and garbage overflows—while enforcing statutory accountability across government departments through an **Automated Day 2 / Day 4 Escalation Engine**.

---

## 🎨 Mandatory Brand & Visual Design System

The platform strictly implements the hackathon-mandated high-contrast palette:
- **Near-Black (`#0B0D0C`)**: Main background providing immersive dark mode.
- **Dark Charcoal (`#141816` / `#1B221E`)**: Elevated cards, table rows, and modal containers.
- **Neon Green (`#39FF88`)**: Primary action buttons, positive statuses (Resolved, Satisfied, Active), and pulse glowing beacons.
- **Deep Green (`#123D2A`)**: Status pills, accent backgrounds, and subtle glows.
- **Alert Red (`#FF3B46`)**: Urgent public hazards, SLA breaches, overdue notices, and executive escalation warnings.
- **White (`#FFFFFF`) & Muted Slate (`#94A3B8`)**: High-contrast, WCAG AAA-compliant readable text.

---

## 🚀 Key Functional Modules

### 1. Five Distinct Role-Based Portals
| Portal | Primary User | Core Capabilities |
| :--- | :--- | :--- |
| **Citizen Portal** | Indian Citizens | File geotagged complaints with photos, receive human-readable IDs (`CP-2026-XXXXX`), track live status, review department completion proof, confirm resolution or request reopening. |
| **Department Portal** | Verified Field / Desk Officials | Restricted to authorized department & jurisdiction. Review complaints, acknowledge within 48h SLA, adjust priority, assign field workers, upload completion photos, transfer wrong-category issues. |
| **Supervisor Portal** | Zonal Supervisors | Monitored Day 2 escalations (48h breach), unassigned queues, dispatch field directives, record delay rationales, or escalate to Head. |
| **Department Head Portal**| Chief Engineers / Commissioners | Monitored Day 4 escalations (96h unresolved), manage critical hazards, issue executive orders, grant justified SLA extensions without erasing audit history. |
| **Administration Portal** | System Administrators | Review & verify department applicants (prevents self-declared official accounts), manage departments & routing, monitor audit trails & AI diagnostics, trigger escalation checks, export CSV reports. |

### 2. Multi-Tier Security & Verification Model
- **Department Registration Gate**: Self-registered government accounts are assigned `pending` status by default. They **cannot** access departmental data until verified and approved by a System Administrator.
- **Protected Direct URL Access**: All endpoints enforce server-side role and departmental membership verification (`@department_verified_required`, `@supervisor_required`, `@dept_head_required`, `@admin_required`).
- **Privacy Shield on Public Maps**: Public map feeds omit personal citizen names, mobile numbers, and personal residential addresses, revealing only civic landmarks and problem categories.

### 3. Transparent AI Triage & Rule-Based Fallback
- Reusable `AIComplaintAnalyzer` service with provider independence.
- When `GEMINI_API_KEY` is present, executes multimodal assessment.
- When external API is absent or offline, executes **CivicNLP Deterministic Rule Engine** and transparently labels the result as:  
  `"Rule-based analysis (External AI key not configured)"`. Never claims an AI model analyzed an image if it was not performed.
- Assesses urgency: flags life perils (sparking transformers, open manholes) as **Urgent Hazard**, high public disruptions as **High**, and routine maintenance as **Medium/Low**.

### 4. Automated Day 2 / Day 4 Statutory Escalation System
- **Day 0**: Complaint registered, category classified, 48h & 96h deadlines computed in Indian Standard Time (IST).
- **Day 2 (48 Hours)**: If no departmental action is recorded, automatically triggers Level 1 escalation to the Zonal Supervisor and alerts the citizen.
- **Day 4 (96 Hours)**: If unresolved, escalates to Level 2 (Department Head) with mandatory executive remediation.
- **Idempotent Execution**: Cron jobs and manual admin triggers can run repeatedly without creating duplicate escalation rows.

### 5. Geospatial & Semantic Duplicate Detection
- Compares incoming complaints against existing reports using **Jaccard Token Text Similarity**, **Haversine Geographic Radius (< 300m)**, and **Temporal Recency Window (14–30 days)**.
- Provides real-time pre-submission warnings as the citizen types the title, reducing redundant reports.

### 6. Interactive Leaflet Maps & Hotspot Analytics
- OpenStreetMap integration with custom urgency-coded markers (Red = Urgent, Orange = High, Green = Routine).
- Dynamic filtering by category, priority, and status.

### 7. Multilingual Support
- Native session language switcher supporting:
  - **English (EN)**
  - **हिन्दी (HI)**
  - **मराठी (MR)**

---

## 📋 Technology Stack

- **Backend**: Python 3.14+, Flask 3.1+, Flask-SQLAlchemy 3.1+, Flask-Login, Flask-WTF (CSRF Protection), Werkzeug.
- **Database**: SQLite (Local development; compatible with PostgreSQL in production).
- **Frontend**: HTML5, CSS3, JavaScript (ES6), Jinja2 templates, Bootstrap 5.3, Bootstrap Icons, Leaflet 1.9, Chart.js.
- **Timezone**: Indian Standard Time (IST, UTC+5:30) used for all citizen-facing timestamps.

---

## 🛠️ Installation & Setup Guide

### 1. Clone & Navigate to Project Directory
```powershell
cd C:\Users\chait\.gemini\antigravity\scratch\civicpulse-ai
```

### 2. Activate Virtual Environment
```powershell
# Windows PowerShell
.\venv\Scripts\Activate.ps1
```

### 3. Install Dependencies
```powershell
pip install -r requirements.txt
```

### 4. Configure Environment
Copy `.env.example` to `.env`:
```powershell
Copy-Item .env.example .env
```

### 5. Seed Database with Realistic Demo Data
Run the seeding command to automatically generate departments, administrative hierarchies, and sample complaints across all stages:
```powershell
python run.py seed-data
```

### 6. Run the Application
```powershell
python run.py
```
Open your browser at: **`http://127.0.0.1:5000`**

---

## 👤 Pre-Configured Demo Credentials

Use these verified accounts to immediately test and evaluate each role:

| Role | Email | Password | Access Capabilities |
| :--- | :--- | :--- | :--- |
| **System Administrator** | `admin@civicpulse.gov.in` | `Admin@CivicPulse2026` | Approve department applications, audit logs, AI diagnostics, escalation triggers, CSV export. |
| **Department Head** | `head.pwd@civicpulse.gov.in` | `DeptHead@2026` | Day 4 critical escalations, public perils, approve revised deadlines with reason. |
| **Zonal Supervisor** | `supervisor.pwd@civicpulse.gov.in` | `Supervisor@2026` | Day 2 escalations (48h breach), supervisory directives, forward cases to Head. |
| **Department Official** | `engineer.pwd@civicpulse.gov.in` | `Official@2026` | PWD operational queue, acknowledge tickets, change statuses, upload resolution photo proof. |
| **Citizen Account** | `citizen@civicpulse.in` | `Citizen@2026` | Submit grievances, track personal tickets, confirm resolution or request reopening. |
| **Pending Official** | `applicant.sanitation@civicpulse.in` | `Applicant@2026` | Tests pending verification screen (cannot access department dashboard until Admin approves). |

---

## ⚙️ Running Background Escalation Scheduler

To run the automated background worker that polls complaints for Day 2 and Day 4 statutory breaches:

```powershell
python run_scheduler.py
```
*Note: You can also manually trigger an instant escalation audit at any time via the Admin Dashboard by clicking **"Run Escalation Check Now"** or via CLI: `python run.py check-escalations`.*

---

## 🧪 Automated Testing

CivicPulse AI includes a test suite covering authentication, role-based protection, department verification security, AI fallback, duplicate detection, and escalation idempotency:

```powershell
python -m unittest discover -s tests -p "test_*.py"
```

All 10 tests execute against an isolated in-memory test database and pass cleanly.

---

## 🔒 Security & Privacy Features

- **Password Hashing**: Werkzeug scrypt hashing. Plaintext passwords are never stored.
- **CSRF Tokens**: Enforced on all POST forms via Flask-WTF.
- **Anti-Tampering File Storage**: Uploaded photos receive cryptographically randomized UUID filenames in sanitized subdirectories.
- **Role Isolation**: Strict server-side route decorators prevent privilege escalation.
- **Citizen Shield**: Citizen phone numbers and exact residential addresses are hidden on public maps and public explore endpoints.

---

## 📄 License
This project is developed for the National Civic Innovation Hackathon. Licensed under the MIT License.
