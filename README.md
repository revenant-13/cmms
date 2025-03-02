# CMMS Project

This repository contains the source code for a web-based **Computerized Maintenance Management System (CMMS)** application. The application is designed to manage maintenance tasks, equipment, parts inventory, scheduling, and reporting, with role-based access control (RBAC) and a dashboard.

---

## Table of Contents
- [App Details](#app-details)
- [Hierarchy and Data Structures](#hierarchy-and-data-structures)
- [Development Timeline](#development-timeline)
- [Technology Stack](#technology-stack)
- [Installation and Setup](#installation-and-setup)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
- [Contact Information](#contact-information)

---

## App Details
The CMMS application is being developed to meet the following core requirements:
- **Equipment Management**: Manage hierarchical equipment and sub-equipment.
- **Parts Management**: Track dynamic parts linked to equipment or sub-equipment.
- **Maintenance Tasks**: Assign and schedule planned maintenance tasks.
- **Scheduling**: Manage task scheduling with due dates, completion tracking, and history logging.
- **Role-Based Access Control (RBAC)**: Implement grid-based permissions for different user roles (e.g., Administrator, Manager, Maintenance, Operator).
- **Dashboard**: Provide a dashboard for task tracking, due schedules, and historical data.
- **Scalability, Security, and User-Friendliness**: Ensure the application is scalable, secure, and easy to use.

---

## Hierarchy and Data Structures
The application’s data model is structured as follows to ensure efficient management of relationships:

### Entities and Relationships
- **Equipment**: Self-referential for hierarchical structure (parent-child relationships).
  - Attributes: `name`, `model`, `serial`, `parent` (references another Equipment).
- **Parts**: Linked to Equipment.
  - Attributes: `part_number`, `status`, `last_updated`, `equipment` (foreign key to Equipment).
- **Tasks**: Assigned to Equipment.
  - Attributes: `description`, `frequency` (e.g., daily, monthly), `equipment` (foreign key to Equipment), `start_date`.
- **Schedules**: Linked to Tasks.
  - Attributes: `task` (foreign key to Task), `due_date`, `completion_date`, `status`, `history_log`.
- **Users and Roles**:
  - Users are assigned to roles (groups in Django).
  - Roles have permissions (e.g., can edit equipment, view tasks).

### Database Schema (PostgreSQL via Django ORM)
- **Equipment Table**: Uses `django-mptt` for hierarchy management.
- **Parts Table**: Linked to Equipment via foreign key.
- **Tasks Table**: Linked to Equipment via foreign key.
- **Schedules Table**: Linked to Tasks via foreign key.
- **Authentication Tables**: Django’s built-in `auth_user`, `auth_group`, `auth_permission` for RBAC.

This structure supports hierarchical equipment management and efficient querying.

---

## Development Timeline
The project is divided into the following phases to keep development organized:

1. **Data Modeling** (Completed)
   - Created Django models and PostgreSQL schema.
2. **Backend Development** (In Progress)
   - Set up Django REST Framework APIs.
   - Implement scheduling logic and RBAC.
3. **Frontend Development**
   - Build UI components using React or Vue.js.
4. **Integration and Testing**
   - Test backend, frontend, and API integration.
5. **Deployment**
   - Deploy the application to a hosting platform.

Tracking these phases will help us stay on schedule.

---

## Technology Stack
Here’s the tech stack we’re using, which will guide setup and troubleshooting:
- **Backend**: Django (Python)
  - Purpose: APIs, business logic, authentication, ORM.
- **Database**: PostgreSQL
  - Purpose: Relational data storage, complex queries, reporting.
- **Frontend**: React or Vue.js (TBD)
  - Purpose: Dynamic UI with component-based design.
- **Additional Tools**:
  - `django-mptt`: For managing hierarchical equipment.
  - `psycopg2`: PostgreSQL adapter for Django.
  - Git and GitHub for version control.

---

## Installation and Setup
To set up the development environment locally:

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/cmms.git
   cd cmms
