# Custom Authentication Service with Social Login & RBAC

![Python](https://img.shields.io/badge/python-3.11-blue.svg) ![FastAPI](https://img.shields.io/badge/FastAPI-0.103-green.svg) ![MongoDB](https://img.shields.io/badge/MongoDB-7.0-brightgreen.svg) ![JWT](https://img.shields.io/badge/Auth-JWT-orange.svg)

This project is a complete, full-stack authentication system built to be secure, scalable, and easy to integrate. It provides a robust backend API using FastAPI and a clean, responsive frontend using vanilla HTML, CSS, and JavaScript. The service supports traditional email/password registration, social logins (Google & GitHub), and includes advanced features like refresh tokens and role-based access control.

---

## 🏗️ System Architecture

The application follows a classic client-server architecture with a decoupled frontend and backend. The authentication flow involves communication with third-party OAuth providers.

```
+-----------------+      (1) Login Request      +-----------------+      (4) DB Query      +-----------------+
|                 | --------------------------> |                 | ---------------------> |                 |
|    Frontend     |      (HTML, CSS, JS)      |     Backend     |     (FastAPI)      |     Database    |
| (User Browser)  | <-------------------------- |      (API)      | <--------------------- |    (MongoDB)    |
|                 |   (2) JWT Access/Refresh    |                 |    (5) User Data     |                 |
+-----------------+                             +--------+--------+                      +-----------------+
        ^                                                | (3) Redirect
        | (6) Protected                                  | & Callback
        |     Resource Request                           v
        v                                        +-----------------+
+-----------------+                              |                 |
| API Wrapper     |                              |  OAuth Provider |
| (api.js)        |                              | (Google/GitHub) |
| - Auto Token    |                              |                 |
|   Refresh       |                              +-----------------+
+-----------------+

```

**Flow Description:**
1.  **Login:** The user initiates a login/signup from the **Frontend**.
2.  **Token Issuance:** The **Backend** validates the request, queries the **Database**, and returns JWT Access and Refresh tokens.
3.  **Social Login:** For social logins, the user is redirected from the **Backend** to the **OAuth Provider**. After authorization, the provider calls back to the backend, which then issues tokens.
4.  **Database Interaction:** The backend communicates with the **MongoDB** database for all user data operations (create, read, update).
5.  **API Requests:** The frontend uses the Access Token to request protected data (like user profiles).
6.  **Auto-Refresh:** The `api.js` wrapper on the frontend intercepts API calls. If an Access Token is expired (401 Unauthorized), it silently uses the Refresh Token to get a new one before retrying the original request.

---

## ✨ Features

-   **Custom UI:** A simple and clean user interface for login and signup forms.
-   **Secure Email/Password Authentication:**
    -   Password hashing using industry-standard `bcrypt`.
    -   User registration, login, and logout functionality.
-   **Social Logins:**
    -   Seamless, one-click authentication with Google.
    -   Seamless, one-click authentication with GitHub.
-   **Advanced Token-Based Security:**
    -   **JWT Access Tokens:** Short-lived (30 min) JWTs for accessing protected resources.
    -   **Refresh Tokens:** Long-lived (7 days) refresh tokens for a smooth user experience without frequent logins.
    -   Automatic token refresh handling on the frontend.
-   **Role-Based Access Control (RBAC):**
    -   `user` and `admin` roles are supported.
    -   Protected API endpoints that can only be accessed by users with the 'admin' role.
    -   Conditional UI rendering on the frontend based on the user's role.
-   **NoSQL Database:**
    -   Flexible and scalable data storage using MongoDB.
    -   Asynchronous database operations with Beanie ODM for high performance.
-   **Comprehensive API:**
    -   Well-defined API endpoints for all authentication-related actions.
    -   Interactive API documentation available at `/docs` (via Swagger UI).

---

## 🛠️ Tech Stack & Architectural Choices

This project uses a modern technology stack chosen for performance, security, and developer experience.

| Category      | Technology                                                              | Rationale                                                                                                                              |
| :------------ | :---------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------- |
| **Backend** | [**FastAPI**](https://fastapi.tiangolo.com/)                            | A high-performance Python framework that leverages `async`/`await` for non-blocking I/O, perfect for building scalable APIs.          |
| **Database** | [**MongoDB**](https://www.mongodb.com/)                                 | A leading NoSQL database chosen for its flexible document model and horizontal scalability, ideal for user profile data.               |
| **ODM** | [**Beanie**](https://github.com/roman-right/beanie)                     | An asynchronous Object-Document Mapper that integrates seamlessly with FastAPI and Pydantic, simplifying database interactions.     |
| **Auth** | [**JWT**](https://jwt.io/) & [**OAuth 2.0**](https://oauth.net/2/)        | Standard protocols for token-based authentication and delegated authorization, ensuring secure and interoperable access control.     |
| **Frontend** | **Vanilla HTML, CSS, JS** | Chosen to keep the focus on the authentication logic without the overhead of a large framework, ensuring maximum compatibility.      |
| **Libraries** | `passlib`, `python-jose`, `authlib`                                     | Best-in-class libraries for handling password hashing, JWT encoding/decoding, and OAuth 2.0 client flows respectively.             |

---

## 🧠 Tech Stack to Learn

To fully understand and contribute to this project, you should be familiar with the following technologies and concepts.

| Area       | Technology / Concept                                                    | Key Topics to Focus On                                                                                                    |
| :--------- | :---------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------ |
| **Backend** | [**Python**](https://www.python.org/)                                   | Fundamentals of `async`/`await` for asynchronous programming, and managing packages with `pip` and `venv`.                |
|            | [**FastAPI**](https://fastapi.tiangolo.com/)                            | Creating routes (`@router.post`), using Dependency Injection (`Depends`), and working with Pydantic for data validation.    |
| **Frontend** | **HTML & CSS** | Structuring web pages with HTML5 and applying modern styling with CSS, including Flexbox for layout.                  |
|            | [**JavaScript (ES6+)**](https://developer.mozilla.org/en-US/docs/Web/JavaScript) | DOM manipulation, making API calls with `fetch`, handling Promises with `async`/`await`, and using `localStorage`. |
| **Database** | [**MongoDB**](https://www.mongodb.com/basics)                           | Understanding the basics of NoSQL, including documents, collections, and how to perform basic queries.                     |
|            | [**Beanie ODM**](https://beanie-odm.dev/)                               | Defining `Document` models that map to MongoDB collections and using its async methods for database operations.       |
| **Concepts** | **REST APIs** | Principles of REST, including HTTP methods (GET, POST), status codes (200, 401, 403), and using JSON for data transfer. |
|            | **JWT & OAuth 2.0** | The structure of a JWT (Header, Payload, Signature) and the high-level flow of OAuth 2.0 for social logins.           |

---

## 📂 Project Structure Explained

The project is organized into two main directories: `backend` and `frontend`, ensuring a clean separation of concerns.

```
custom-login-project/
├── backend/
│   ├── app/
│   │   ├── crud.py         # Defines functions that directly interact with the database (Create, Read, Update).
│   │   ├── database.py     # Handles the MongoDB connection and initializes the Beanie ODM.
│   │   ├── models.py       # Defines the database collection schemas (e.g., the User document and its fields/types).
│   │   ├── schemas.py      # Defines the Pydantic models for API data shapes (request bodies and response models).
│   │   ├── security.py     # Contains all authentication logic: password hashing, JWT creation, OAuth client setup, and RBAC dependencies.
│   │   └── routers/
│   │       ├── auth.py     # Contains API endpoints for authentication, like /signup, /token, /refresh, and social login callbacks.
│   │       └── users.py    # Contains API endpoints for user management, like fetching profiles or admin-only user lists.
│   ├── .env                # (CRITICAL) Stores all secrets: DB URIs, JWT secret key, and OAuth credentials. Ignored by Git.
│   ├── main.py             # The entry point for the FastAPI application. It sets up middleware (CORS) and includes the API routers.
│   └── requirements.txt    # Lists all Python dependencies for the backend.
│
├── frontend/
│   ├── js/
│   │   ├── api.js          # A crucial API wrapper for `fetch()` that automatically handles JWT access token refreshing.
│   │   ├── auth.js         # Contains the JavaScript logic for the login/signup page (index.html).
│   │   └── dashboard.js    # Contains the JavaScript logic for the user dashboard, including fetching user data and rendering admin views.
│   ├── css/style.css       # Custom styling for the frontend pages.
│   ├── index.html          # The main login and signup page.
│   └── dashboard.html      # The protected page shown to logged-in users.
│
└── README.md               # You are here!
```

---

## 🚀 Setup and Installation Guide

Follow these steps carefully to get the project running locally.

### 1. Prerequisites

-   **Python 3.8+**
-   **Git**
-   A running **MongoDB** instance.
    -   *Recommendation:* Get a free cluster from [MongoDB Atlas](https://www.mongodb.com/cloud/atlas/register).
-   A code editor like [VS Code](https://code.visualstudio.com/) with the [Live Server](https://marketplace.visualstudio.com/items?itemName=ritwickdey.LiveServer) extension for the frontend.

### 2. Clone the Repository

```bash
git clone <your-repository-link>
cd custom-login-project
```

### 3. Backend Configuration

#### Step 3.1: Set Up Virtual Environment & Install Dependencies

Navigate to the backend directory, create a virtual environment, and install the required packages.

```bash
cd backend

# Create a virtual environment
python -m venv venv

# Activate it
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

#### Step 3.2: Obtain Credentials

This is the most critical step. You need API keys and secrets for MongoDB, Google, and GitHub.

-   **MongoDB Connection String:**
    1.  Go to your MongoDB Atlas dashboard.
    2.  Click `Database` -> `Connect` -> `Drivers`.
    3.  Copy the **Connection String** (URI). It will look like `mongodb+srv://<user>:<password>@...`.

-   **Google OAuth Credentials:**
    1.  Go to the [Google Cloud Console Credentials Page](https://console.cloud.google.com/apis/credentials).
    2.  Create a new project if you don't have one.
    3.  Click `+ CREATE CREDENTIALS` -> `OAuth client ID`.
    4.  Select `Web application` for the Application type.
    5.  Under `Authorized redirect URIs`, add: `http://127.0.0.1:8000/auth/callback/google`
    6.  Click `Create`. Copy the **Client ID** and **Client Secret**.

-   **GitHub OAuth Credentials:**
    1.  Go to your GitHub `Settings` -> `Developer settings` -> `OAuth Apps` -> `New OAuth App`.
    2.  **Application name:** `My FastAPI Auth App` (or anything)
    3.  **Homepage URL:** `http://127.0.0.1:8000`
    4.  **Authorization callback URL:** `http://127.0.0.1:8000/auth/callback/github`
    5.  Click `Register application`.
    6.  Click `Generate a new client secret`. Copy the **Client ID** and the new **Client Secret**.

#### Step 3.3: Configure Environment Variables

Create a file named `.env` inside the `backend/` directory. Copy the content below and paste in your credentials.

```ini
# backend/.env

# A long, random, and secret string for signing JWTs
JWT_SECRET_KEY=generate_a_strong_random_secret_string_here

# Paste your MongoDB Atlas connection string
MONGO_URI=mongodb+srv://<user>:<password>@<cluster-url>/<db-name>?retryWrites=true&w=majority

# Paste your Google credentials
GOOGLE_CLIENT_ID=your_google_client_id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your_google_client_secret

# Paste your GitHub credentials
GITHUB_CLIENT_ID=your_github_client_id
GITHUB_CLIENT_SECRET=your_github_client_secret
```

### 4. Run the Application

#### Step 4.1: Start the Backend Server

Ensure you are in the `backend/` directory with your virtual environment activated.

```bash
uvicorn main:app --reload
```

The API server is now running at `http://127.0.0.1:8000`. You can access the interactive documentation at `http://127.0.0.1:8000/docs`.

#### Step 4.2: Launch the Frontend

1.  Open the project folder in VS Code.
2.  Navigate to `frontend/index.html`.
3.  Right-click the file and select `Open with Live Server`.
4.  Your browser will open to the login page, typically at `http://127.0.0.1:5500`.

You can now register, log in, and test the social login flows!

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
| `/auth/signup`               | `POST` | Register a new user with email and password.               | Public      |
| `/auth/token`                | `POST` | Log in with email/password to get access/refresh tokens.   | Public      |
| `/auth/login/{provider}`     | `GET`  | Initiates the social login flow for Google or GitHub.      | Public      |
| `/auth/callback/{provider}`  | `GET`  | Callback URL for the social login provider to redirect to. | Public      |
| `/auth/refresh`              | `POST` | Exchange a valid refresh token for a new access token.     | Public      |
| `/users/me`                  | `GET`  | Get the profile details of the currently logged-in user.   | User        |
| `/users/all`                 | `GET`  | Get a list of all users in the database.                   | **Admin** |

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
-   **Password Reset Flow:** Implement a "Forgot Password" feature that sends a secure, time-limited link to the user's email.
-   **Email Verification:** Require users to verify their email address after signing up by clicking a link sent to them.
-   **More Social Providers:** Integrate other OAuth providers like Facebook, Twitter, or LinkedIn.
-   **Comprehensive Logging:** Add structured logging to track important events, errors, and security-related activities for easier debugging and monitoring.
-   **Rate Limiting:** Protect against brute-force attacks by implementing rate limiting on login and password reset endpoints.

---
## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
