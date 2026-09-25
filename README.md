# FastAPI + AWS RDS Deployment Test

A small FastAPI application built as a hands-on learning project for understanding **AWS RDS, Docker, Docker Hub, and EC2 deployment**.

The application provides a simple user-management API and connects to a **MySQL database hosted on Amazon RDS**.

This project is intentionally simple. The main goal is to understand how an application moves from local development to a containerized deployment on AWS.

## Architecture

```text
Browser
   │
   ▼
EC2 Instance
   │
   ▼
Docker Container
   │
   ▼
FastAPI
   │
   ▼
AWS RDS (MySQL)
```

Development and deployment flow:

```text
Local Development
      │
      ▼
FastAPI + MySQL (AWS RDS)
      │
      ▼
Docker Image
      │
      ▼
Docker Hub
      │
      ▼
AWS EC2
      │
      ▼
Docker Container
      │
      ▼
AWS RDS
```

## What This Project Demonstrates

* FastAPI REST API development
* SQLAlchemy ORM
* MySQL database integration
* Connecting an application to **Amazon RDS**
* Environment variables for database configuration
* Dockerizing a FastAPI application
* Docker image creation
* Docker Hub image publishing
* Running the same application in an AWS EC2 environment
* Connecting a Docker container running on EC2 to RDS

## Features

The application provides basic user management:

* Create a user
* View all users
* Delete a user
* Simple HTML frontend
* REST API backend

### API Endpoints

| Method | Endpoint      | Description   |
| ------ | ------------- | ------------- |
| GET    | `/users`      | Get all users |
| POST   | `/users`      | Create a user |
| DELETE | `/users/{id}` | Delete a user |

## Tech Stack

* **Python**
* **FastAPI**
* **Uvicorn**
* **SQLAlchemy**
* **PyMySQL**
* **MySQL**
* **Amazon RDS**
* **Docker**
* **Docker Hub**
* **Amazon EC2**

## Project Structure

```text
simple-fastapi-app/
│
├── main.py
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── .gitignore
│
└── static/
    └── index.html
```

## Environment Variables

The application reads the database connection from:

```text
DATABASE_URL
```

Example:

```text
DATABASE_URL=mysql+pymysql://username:password@host:3306/database
```

The `.env` file is intentionally excluded from Git and the Docker image because it contains sensitive configuration.

For local development:

```bash
uvicorn main:app --reload
```

For Docker:

```bash
docker run --env-file .env ...
```

## Docker

Build the image:

```bash
docker build -t simple-fastapi-app:1.0 .
```

Run locally:

```bash
docker run -d \
  --name simple-fastapi-app \
  -p 8000:8000 \
  --env-file .env \
  simple-fastapi-app:1.0
```

## Docker Hub

The image can be tagged and pushed to Docker Hub:

```bash
docker tag simple-fastapi-app:1.0 YOUR_USERNAME/simple-fastapi-app:1.0
```

```bash
docker push YOUR_USERNAME/simple-fastapi-app:1.0
```

The image can then be pulled from another machine:

```bash
docker pull YOUR_USERNAME/simple-fastapi-app:1.0
```

## AWS Deployment

The intended deployment architecture is:

```text
                   AWS
┌─────────────────────────────────────┐
│                                     │
│   EC2                             RDS│
│  ┌──────────────┐              ┌───────┐
│  │   Docker     │              │ MySQL │
│  │              │─────────────▶│       │
│  │   FastAPI    │   TCP 3306   │  DB   │
│  └──────────────┘              └───────┘
│                                     │
└─────────────────────────────────────┘
```

The EC2 instance runs the Docker container, while Amazon RDS manages the MySQL database.

The application does **not** need to run MySQL inside the Docker container.

## Learning Goals

This project is part of a hands-on exploration of AWS and DevOps concepts.

The primary goal is to understand the separation between:

```text
EC2       → Compute
Docker    → Application containerization
Docker Hub → Container image registry
RDS       → Managed relational database
```

It also demonstrates how environment-specific configuration can be supplied at runtime rather than being hard-coded into the application or Docker image.

## Status

🚧 **Learning / Deployment Experiment**

This project is intentionally simple and is not intended to represent a production-ready application. Its purpose is to experiment with AWS infrastructure, Docker, database connectivity, and deployment workflows.
