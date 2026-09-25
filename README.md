# FastAPI AWS RDS Deployment

A simple FastAPI application built to learn and demonstrate an end-to-end cloud deployment workflow using **AWS RDS, Docker, Docker Hub, EC2, and GitHub Actions CI/CD**.

The project implements a basic user management API with a simple HTML frontend.

---

## Architecture

```text
                         GitHub
                           │
                           │ push
                           ▼
                    GitHub Actions
                           │
                    ┌──────┴──────┐
                    │             │
                  pytest      Docker Build
                    │             │
                    │             ▼
                    │        Docker Hub
                    │             │
                    └─────────────┘
                                  │
                                  │ docker pull
                                  ▼
                            AWS EC2
                         ┌────────────┐
                         │   Docker   │
                         │            │
                         │  FastAPI   │
                         │   :8000    │
                         └─────┬──────┘
                               │
                         MySQL :3306
                               │
                               ▼
                         AWS RDS MySQL
                               │
                         ┌─────┴─────┐
                         │ simple_app │
                         │   users    │
                         └────────────┘
```

---

## Features

* Simple HTML frontend
* FastAPI backend
* REST API
* Create users
* List users
* Delete users
* MySQL database
* AWS RDS MySQL
* Dockerized application
* Docker Hub image
* AWS EC2 deployment
* GitHub Actions CI
* Automated Docker image build and push
* Environment-based database configuration

---

## API Endpoints

| Method   | Endpoint      | Description              |
| -------- | ------------- | ------------------------ |
| `GET`    | `/`           | Serves the HTML frontend |
| `GET`    | `/users`      | Returns all users        |
| `POST`   | `/users`      | Creates a user           |
| `DELETE` | `/users/{id}` | Deletes a user           |

---

## Project Structure

```text
simple-fastapi-app/
│
├── .github/
│   └── workflows/
│       └── deploy.yml
│
├── static/
│   └── index.html
│
├── main.py
├── test_main.py
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── .gitignore
└── README.md
```

---

# Application

The backend is built with **FastAPI** and uses **SQLAlchemy** to communicate with MySQL.

The database model is:

```text
users
├── id
└── username
```

SQLAlchemy maps the Python `User` model to the MySQL `users` table.

```python
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(100), nullable=False)
```

---

# AWS RDS

The application uses **Amazon RDS for MySQL** as its database server.

The application does not contain the database itself.

```text
FastAPI
   │
   │ SQL
   ▼
RDS MySQL
   │
   └── simple_app
        └── users
```

The application connects to RDS using a SQLAlchemy database URL:

```text
mysql+pymysql://USERNAME:PASSWORD@RDS_ENDPOINT:3306/simple_app
```

The database URL is supplied through the `DATABASE_URL` environment variable.

Credentials are **not stored in the source code**.

---

# Local Development

Create a virtual environment:

```bash
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```env
DATABASE_URL="mysql+pymysql://USERNAME:PASSWORD@RDS_ENDPOINT:3306/simple_app"
```

Run FastAPI:

```bash
uvicorn main:app --reload
```

The application will be available at:

```text
http://localhost:8000
```

---

# Testing

The project contains a minimal API test:

```python
def test_get_users():
    response = client.get("/users")
    assert response.status_code == 200
```

Run tests locally:

```bash
pytest
```

The test verifies that the `/users` endpoint successfully responds with HTTP `200`.

---

# Docker

The application is packaged into a Docker image containing:

```text
Python
├── FastAPI
├── Uvicorn
├── SQLAlchemy
├── PyMySQL
├── application code
└── static frontend
```

The local virtual environment is **not** copied into the image.

Build the image:

```bash
docker build -t simple-fastapi-app:1.0 .
```

Run locally:

```bash
docker run \
  -p 8000:8000 \
  --env-file .env \
  simple-fastapi-app:1.0
```

The container listens on port `8000`.

---

# Docker Hub

The Docker image is published to Docker Hub:

```text
mimranbuttcodes/simple-fastapi-app
```

Example:

```bash
docker login
```

Tag:

```bash
docker tag simple-fastapi-app:1.0 \
  mimranbuttcodes/simple-fastapi-app:1.0
```

Push:

```bash
docker push mimranbuttcodes/simple-fastapi-app:1.0
```

---

# AWS EC2 Deployment

The Docker image is pulled onto an Amazon Linux EC2 instance.

```bash
sudo docker pull mimranbuttcodes/simple-fastapi-app:1.0
```

The container is started with the RDS connection string supplied as an environment variable:

```bash
sudo docker run -d \
  --name server1 \
  -p 80:8000 \
  -e DATABASE_URL="..." \
  mimranbuttcodes/simple-fastapi-app:1.0
```

The port mapping is:

```text
EC2 port 80
     │
     ▼
Container port 8000
     │
     ▼
Uvicorn / FastAPI
```

The browser therefore accesses the application through:

```text
http://EC2_PUBLIC_IP
```

---

# Final Request Flow

When a user creates a user through the web application:

```text
Browser
   │
   │ HTTP POST /users
   ▼
EC2 :80
   │
   ▼
Docker Container :8000
   │
   ▼
FastAPI
   │
   │ SQL INSERT
   ▼
RDS MySQL :3306
   │
   ▼
simple_app.users
```

For reading users:

```text
Browser
   │
   │ GET /users
   ▼
FastAPI
   │
   │ SELECT
   ▼
RDS MySQL
   │
   ▼
users table
   │
   ▼
FastAPI
   │
   ▼
Browser
```

---

# GitHub Actions CI

The repository contains a GitHub Actions workflow:

```text
.github/workflows/deploy.yml
```

The workflow runs whenever code is pushed to `main`.

```text
git push
    │
    ▼
GitHub Actions
    │
    ▼
Checkout repository
    │
    ▼
Install Python 3.12
    │
    ▼
Install dependencies
    │
    ▼
Run pytest
    │
    ├── FAIL → Stop
    │
    └── PASS
          │
          ▼
     Build Docker image
          │
          ▼
     Push to Docker Hub
```

The Docker build only happens when the tests pass.

---

# GitHub Secrets

Sensitive information is stored using GitHub repository secrets rather than being committed to the repository.

Current secrets include:

```text
DATABASE_URL
DOCKERHUB_USERNAME
DOCKERHUB_TOKEN
```

The workflow accesses the database URL using:

```yaml
env:
  DATABASE_URL: ${{ secrets.DATABASE_URL }}
```

The RDS password should never be committed to Git.

---

# CI/CD Status

Current implementation:

```text
CI
├── GitHub Actions
├── pytest
├── Docker build
└── Docker Hub push
```

Deployment infrastructure:

```text
CD infrastructure
├── Docker Hub
├── EC2
└── RDS MySQL
```

The next step for full continuous deployment is to connect GitHub Actions to EC2 so that a successful build automatically:

```text
GitHub
   ↓
GitHub Actions
   ↓
Tests
   ↓
Docker Build
   ↓
Docker Hub
   ↓
EC2
   ↓
docker pull
   ↓
replace running container
```

---

# AWS Services Used

### EC2

Provides the virtual server that runs the Docker container.

### RDS

Provides the managed MySQL database.

### EBS

Provides persistent block storage for the EC2 instance.

### VPC

Provides the underlying AWS network.

### Security Groups

Control network access between the application and database.

---

# Technologies

* Python
* FastAPI
* SQLAlchemy
* PyMySQL
* MySQL
* AWS RDS
* AWS EC2
* Docker
* Docker Hub
* GitHub Actions
* HTML
* JavaScript
* pytest

---

# Key Concepts Learned

This project demonstrates the complete relationship between:

```text
Application
     ↓
FastAPI
     ↓
Docker
     ↓
Docker Hub
     ↓
EC2
     ↓
RDS
```

It also demonstrates:

* REST APIs
* Environment variables
* Database connection strings
* SQLAlchemy ORM
* Docker images and containers
* Docker port mapping
* Container-to-database communication
* AWS EC2 deployment
* Managed databases with RDS
* GitHub Actions
* CI pipelines
* Automated Docker image publishing
* GitHub Secrets
* Basic cloud deployment architecture

---

# Security Notes

Never commit:

```text
.env
```

or database credentials to Git.

The `.gitignore` file excludes sensitive configuration such as:

```text
.venv/
.env
.env.*
__pycache__/
```

For production, the RDS security group should **not** allow MySQL port `3306` from the entire Internet.

Instead:

```text
Internet
   │
   ▼
Application
   │
   ▼
RDS :3306
```

The RDS security group should allow database access only from the application's security group or appropriate trusted network.

---

# Future Production Architecture

The current project intentionally keeps the architecture simple for learning.

A more complete production architecture could become:

```text
                     Route 53
                         │
                         ▼
                    CloudFront
                         │
                         ▼
                       ALB
                         │
              ┌──────────┴──────────┐
              ▼                     ▼
            EC2                   EC2
         FastAPI                 FastAPI
              │                     │
              └──────────┬──────────┘
                         │
                         ▼
                    RDS MySQL
                         │
                         ▼
                       S3
```

With:

```text
ASG        → manages EC2 instances
ALB        → distributes traffic
RDS        → managed database
S3         → object/file storage
CloudFront → CDN
Route 53   → DNS
IAM        → permissions
CloudWatch → monitoring
ECR        → container registry
```

This repository represents the smaller foundational version of that architecture.
