# Simple Referral System

This project is a simple referral system built with FastAPI, SQLAlchemy, and Redis. It allows users to generate, retrieve, and delete referral codes, as well as manage referrals.

## Features

- Generate referral codes
- Retrieve referral codes by user ID or email
- Delete referral codes
- Manage user referrals

## Project Structure

- `src/schemas/referral.py`: Defines the Pydantic models for the referral system.
- `src/api/referral.py`: Contains the API endpoints for managing referrals and referral codes.
- `Dockerfile`: Docker configuration for building and running the application.

## Installation

1. Clone the repository:
    ```sh
    git clone git@github.com:Azeasy/FastAPI_referral.git
    ```

2. Build the Docker image (It may take a few minutes while all dependencies and images are being downloaded):
    ```sh
    docker-compose up -d
    ```

## API Endpoints

- `GET /`: Retrieve all referrals for the current user.
- `GET /get_by_id`: Retrieve referrals by user ID.
- `POST /code/`: Generate a referral code.
- `GET /code/`: Retrieve the current user's referral code.
- `DELETE /code/`: Delete the current user's referral code.
- `GET /code/get_by_email`: Retrieve a referral code by email.

## Environment Variables

- `src`: The root directory for the application.

## Dependencies

- Python 3.11
- FastAPI
- SQLAlchemy
- Redis
- Poetry

## Running Migrations

To run database migrations, use Alembic:
```sh
alembic upgrade head
