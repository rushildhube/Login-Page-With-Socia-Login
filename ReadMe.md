# Custom Authentication Service with Social Login & RBAC

![Python](https://img.shields.io/badge/python-3.11-blue.svg) ![FastAPI](https://img.shields.io/badge/FastAPI-0.103-green.svg) ![MongoDB](https://img.shields.io/badge/MongoDB-7.0-brightgreen.svg) ![JWT](https://img.shields.io/badge/Auth-JWT-orange.svg)

This project is a complete, full-stack authentication system built to be secure, scalable, and easy to integrate. It provides a robust backend API using FastAPI and a clean, responsive frontend using vanilla HTML, CSS, and JavaScript. The service supports traditional email/password registration, social logins (Google & GitHub), and includes advanced features like refresh tokens, role-based access control, email verification, and password resets.

---

## 🏗️ System Architecture

The application follows a classic client-server architecture with a decoupled frontend and backend. The authentication flow involves communication with third-party OAuth providers.

![alt text](<resources/Untitled diagram _ Mermaid Chart-2025-08-15-075905.png>)

---

## ✨ Features

-   **Modern UI:** A clean, responsive, and user-friendly "glassmorphism" interface.
-   **Secure Email/Password Authentication:**
    -   Password hashing using industry-standard `bcrypt`.
    -   **Email Verification:** New users are sent a verification email and cannot log in until their email is confirmed.
    -   **Password Reset:** A secure "Forgot Password" flow that sends a time-limited reset link via email.
-   **Social Logins:**
    -   Seamless, one-click authentication with Google and GitHub.
-   **Advanced Token-Based Security:**
    -   **JWT Access Tokens:** Short-lived (30 min) JWTs for accessing protected resources.
    -   **Refresh Tokens:** Long-lived (7 days) refresh tokens for a smooth user experience.
    -   Automatic token refresh handling on the frontend.
-   **Role-Based Access Control (RBAC):**
    -   `user` and `admin` roles are supported.
    -   Protected API endpoints that can only be accessed by administrators.
-   **Admin Dashboard:**
    -   A dedicated, protected dashboard for administrators.
    -   View a list of all registered users in the system.
    -   Track recent login activity, including IP address and browser information.
-   **Security Hardening:**
    -   **Rate Limiting:** Protects against brute-force attacks by temporarily blocking IPs with too many failed login attempts.
    -   **CSRF Protection:** Robust `state` validation in the OAuth flow to prevent cross-site request forgery.

---

## 📂 Project Structure Explained

The project is organized into `backend` and `frontend` directories, ensuring a clean separation of concerns.

```
/custom-login-project/
|-- backend/
|   |-- app/
|   |   |-- routers/
|   |   |   |-- auth.py         # Handles all authentication endpoints (login, signup, social, reset).
|   |   |   |-- users.py        # Handles general user endpoints (e.g., getting a profile).
|   |   |   `-- admin.py        # Handles protected, admin-only endpoints.
|   |   |-- crud.py           # Contains all database interaction functions (Create, Read, Update).
|   |   |-- database.py       # Handles the MongoDB connection and Beanie initialization.
|   |   |-- email_utils.py    # Contains the utility function for sending SMTP emails.
|   |   |-- models.py         # Defines the database schemas (User, LoginHistory).
|   |   |-- schemas.py        # Defines the Pydantic models for API data validation.
|   |   `-- security.py       # Contains all security logic (hashing, JWTs, OAuth, RBAC).
|   |-- .env                  # (CRITICAL) Stores all secret credentials.
|   |-- main.py               # The FastAPI application entry point.
|   `-- requirements.txt      # Lists all Python dependencies.
|
|-- frontend/
|   |-- css/style.css         # The single stylesheet for the entire application.
|   |-- js/
|   |   |-- api.js            # A crucial API wrapper that handles auto token refreshing.
|   |   |-- auth.js           # Logic for the main login/signup page.
|   |   |-- dashboard.js      # Logic for the standard user dashboard.
|   |   `-- admin.js          # Logic for the admin dashboard.
|   |-- index.html            # The main login and signup page.
|   |-- dashboard.html        # The protected page for logged-in users.
|   |-- admin.html            # The protected page for administrators.
|   |-- verify.html           # Page for handling email verification.
|   `-- reset-password.html   # Page for handling password resets.
|
`-- README.md                 # You are here!
```

---

## 🚀 Setup and Installation Guide

Follow these steps carefully to get the project running locally.

### 1. Prerequisites

-   **Python 3.8+**
-   **Git**
-   A running **MongoDB** instance (e.g., from [MongoDB Atlas](https://www.mongodb.com/cloud/atlas/register)).
-   An **Email Account** that supports SMTP (e.g., Gmail with an "App Password").
-   A code editor like [VS Code](https://code.visualstudio.com/) with the [Live Server](https://marketplace.visualstudio.com/items?itemName=ritwickdey.LiveServer) extension.

### 2. Clone the Repository

```bash
git clone <your-repository-link>
cd custom-login-project
```

### 3. Backend Configuration

#### Step 3.1: Set Up Virtual Environment & Install Dependencies

Navigate to the **project root** directory.

```bash
# Create a virtual environment
python -m venv venv

# Activate it
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install all dependencies
pip install -r backend/requirements.txt
```

#### Step 3.2: Obtain Credentials

You need API keys and secrets for MongoDB, Google, GitHub, and your email provider.

-   **MongoDB:** Get your **Connection String (URI)** from your Atlas dashboard.
-   **Google OAuth:** Get your **Client ID** and **Client Secret** from the [Google Cloud Console](https://console.cloud.google.com/apis/credentials).
    -   *Authorized redirect URI:* `http://127.0.0.1:8000/auth/callback/google`
-   **GitHub OAuth:** Get your **Client ID** and **Client Secret** from your GitHub Developer Settings.
    -   *Authorization callback URL:* `http://127.0.0.1:8000/auth/callback/github`
-   **Email SMTP:** Get your SMTP server details. For Gmail, you must generate an **"App Password"** from your Google Account's security settings.

#### Step 3.3: Configure Environment Variables

Create a file named `.env` inside the `backend/` directory. Copy the content below and paste in your credentials.

```ini
# backend/.env

# A long, random, and secret string for signing JWTs (at least 32 characters)
JWT_SECRET_KEY=your_super_secret_random_string_here

# Your MongoDB Atlas connection string (including the database name)
MONGO_URI=mongodb+srv://<user>:<password>@<cluster-url>/<db-name>?retryWrites=true&w=majority

# Your Google credentials
GOOGLE_CLIENT_ID=your_google_client_id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your_google_client_secret

# Your GitHub credentials
GITHUB_CLIENT_ID=your_github_client_id
GITHUB_CLIENT_SECRET=your_github_client_secret

# Your Email SMTP credentials
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_gmail_app_password
```

### 4. Run the Application

#### Step 4.1: Start the Backend Server

Ensure you are in the **project root directory** with your virtual environment activated.

```bash
uvicorn backend.main:app --reload
```

The API server is now running at `http://127.0.0.1:8000`.

#### Step 4.2: Launch the Frontend

1.  Open the project folder in VS Code.
2.  Right-click the `frontend/index.html` file and select `Open with Live Server`.
3.  Your browser will open to the login page, typically at `http://127.0.0.1:5500`.

---

## 👑 How to Log In as an Admin

1.  **Sign Up:** Create a regular user account through the application.
2.  **Verify Email:** Click the verification link sent to your email.
3.  **Promote in Database:**
    -   Log in to your MongoDB Atlas dashboard and navigate to the `users` collection.
    -   Find the user you just created and **Edit** the document.
    -   Change the `role` field's value from `"user"` to `"admin"`.
    -   Click **Update** to save.
4.  **Log In Again:** Go back to the application and log in with your newly promoted admin account. You will now see the "Admin Tools" on your dashboard.

---

## 🔐 Authentication Flow Explained

This application uses a standard and secure token-based authentication mechanism.

1.  **Login:** A user provides credentials (email/password or via social login).
2.  **Token Issuance:** The server validates the credentials and issues two tokens:
    -   An **Access Token** (JWT, short-lived) containing user info.
    -   A **Refresh Token** (JWT, long-lived) stored in the database.
3.  **Storage:** Both tokens are sent to the client and stored in `localStorage`.
4.  **API Requests:** For every request to a protected API endpoint, the frontend sends the **Access Token** in the `Authorization` header.
5.  **Token Expiration & Refresh:**
    -   If the server receives an expired Access Token (HTTP 401), the frontend's API wrapper automatically uses the **Refresh Token** to request a new Access Token from the `/auth/refresh` endpoint.
    -   If the Refresh Token is also expired or invalid, the user is logged out.

---

## 📖 API Endpoint Documentation

| Endpoint                     | Method | Description                                                | Permissions |
| :--------------------------- | :----- | :--------------------------------------------------------- | :---------- |
| `/auth/signup`               | `POST` | Register a new user and sends a verification email.        | Public      |
| `/auth/token`                | `POST` | Log in with email/password to get access/refresh tokens.   | Public      |
| `/auth/login/{provider}`     | `GET`  | Initiates the social login flow for Google or GitHub.      | Public      |
| `/auth/callback/{provider}`  | `GET`  | Callback URL for the social login provider to redirect to. | Public      |
| `/auth/refresh`              | `POST` | Exchange a valid refresh token for a new access token.     | Public      |
| `/auth/verify-email`         | `POST` | Verifies a user's email using a token from the link.       | Public      |
| `/auth/forgot-password`      | `POST` | Sends a password reset link to the user's email.           | Public      |
| `/auth/reset-password`       | `POST` | Resets the user's password using a token from the link.    | Public      |
| `/users/me`                  | `GET`  | Get the profile details of the currently logged-in user.   | User        |
| `/admin/users`               | `GET`  | Get a list of all users in the database.                   | **Admin** |
| `/admin/login-history`       | `GET`  | Get the 20 most recent login events.                       | **Admin** |

---

## 🚨 Security Considerations

-   **Password Hashing:** Passwords are never stored in plaintext. `passlib` with `bcrypt` is used for strong, one-way hashing.
-   **Environment Variables:** All sensitive data (API keys, secrets) is loaded from a `.env` file, which is excluded from version control via `.gitignore`.
-   **Token Expiration:** Short-lived access tokens limit the damage if a token is compromised. The refresh token mechanism provides a balance between security and user experience.
-   **CORS Policy:** The backend is configured with a strict Cross-Origin Resource Sharing (CORS) policy to only allow requests from the specified frontend origin.
-   **Input Validation:** Pydantic models are used to rigorously validate all incoming request data to prevent injection and other data-related attacks.
-   **HTTPS in Production:** While the local setup uses HTTP, a production deployment must use HTTPS to encrypt all traffic between the client and server, protecting tokens from being intercepted.

---
## 📦 Deployment Considerations

To move this project from a local development setup to a live production environment, consider the following steps:

1.  **Backend Deployment:**
    -   **WSGI Server:** Use a production-grade server like **Gunicorn** or **Uvicorn with workers** to run the FastAPI application instead of the development server.
    -   **Containerization:** Package the backend application into a **Docker** container for portability and easy scaling.
    -   **Hosting:** Deploy the container to a cloud service like **AWS (ECS/Fargate), Google Cloud Run, or Heroku**.
2.  **Frontend Deployment:**
    -   **Static Hosting:** The frontend is a static site. It can be hosted cheaply and efficiently on services like **Vercel, Netlify, AWS S3, or GitHub Pages**.
3.  **Database:**
    -   Use a managed database service like **MongoDB Atlas** for production. It handles backups, scaling, and security for you.
4.  **Environment Variables:**
    -   In a production environment, do not use a `.env` file. Use the secret management system provided by your cloud host (e.g., AWS Secrets Manager, Google Secret Manager) to inject environment variables securely.

---

## 🔮 Future Improvements

This project provides a solid foundation. Here are some features that could be added to enhance it further:

-   **Two-Factor Authentication (2FA):** Add an extra layer of security using TOTP (e.g., Google Authenticator) or SMS verification.
-   **Comprehensive Logging:** Add structured logging to track important events, errors, and security-related activities for easier debugging and monitoring.
-   **More Social Providers:** Integrate other OAuth providers like Facebook, Twitter, or LinkedIn.
