document.addEventListener('DOMContentLoaded', () => {
    const loginView = document.getElementById('login-view');
    const signupView = document.getElementById('signup-view');
    const showSignupBtn = document.getElementById('show-signup-btn');
    const showLoginBtn = document.getElementById('show-login-btn');
    const forgotPasswordBtn = document.getElementById('forgot-password-btn');

    const loginForm = document.getElementById('login-form');
    const signupForm = document.getElementById('signup-form');

    const API_BASE_URL = 'http://127.0.0.1:8000';

    showSignupBtn.addEventListener('click', () => {
        loginView.style.display = 'none';
        signupView.style.display = 'block';
    });

    showLoginBtn.addEventListener('click', () => {
        signupView.style.display = 'none';
        loginView.style.display = 'block';
    });

    forgotPasswordBtn.addEventListener('click', async () => {
        const email = document.getElementById('login-email').value;
        if (!email) {
            alert("Please enter your email address in the email field first.");
            return;
        }
        try {
            await fetch(`${API_BASE_URL}/auth/forgot-password?email=${encodeURIComponent(email)}`, {
                method: 'POST'
            });
            alert("If an account with that email exists, a password reset link has been sent (check your backend terminal).");
        } catch (error) {
            alert("An error occurred. Please try again.");
        }
    });

    const toggleButtonLoading = (button, isLoading) => {
        button.classList.toggle('loading', isLoading);
        button.disabled = isLoading;
    };

    // --- NEW: Email validation helper ---
    const isValidEmail = (email) => {
        const re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        return re.test(String(email).toLowerCase());
    };

    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const button = loginForm.querySelector('.btn');
        const errorEl = document.getElementById('login-error');
        errorEl.style.display = 'none';
        toggleButtonLoading(button, true);

        const email = document.getElementById('login-email').value;
        const password = document.getElementById('login-password').value;

        // --- NEW: Client-side validation ---
        if (!isValidEmail(email)) {
            errorEl.textContent = "Please enter a valid email address.";
            errorEl.style.display = 'block';
            toggleButtonLoading(button, false);
            return;
        }

        const formData = new FormData();
        formData.append('username', email);
        formData.append('password', password);

        try {
            const response = await fetch(`${API_BASE_URL}/auth/token`, {
                method: 'POST',
                body: formData
            });

            if (response.ok) {
                const data = await response.json();
                localStorage.setItem('accessToken', data.access_token);
                localStorage.setItem('refreshToken', data.refresh_token);
                window.location.href = '/frontend/dashboard.html';
            } else {
                const error = await response.json();
                // --- NEW: More specific error messages ---
                if (error.detail.includes("Incorrect email or password")) {
                    errorEl.textContent = "Incorrect email or password. Please try again.";
                } else if (error.detail.includes("Email not verified")) {
                    errorEl.textContent = "Your email is not verified. Please check your inbox for a verification link.";
                } else {
                    errorEl.textContent = "An unknown error occurred.";
                }
                errorEl.style.display = 'block';
            }
        } catch (error) {
            errorEl.textContent = 'Could not connect to the server. Please try again later.';
            errorEl.style.display = 'block';
        } finally {
            toggleButtonLoading(button, false);
        }
    });

    signupForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const button = signupForm.querySelector('.btn');
        const errorEl = document.getElementById('signup-error');
        errorEl.style.display = 'none';
        toggleButtonLoading(button, true);

        const fullName = document.getElementById('signup-name').value;
        const email = document.getElementById('signup-email').value;
        const password = document.getElementById('signup-password').value;
        
        // --- NEW: Client-side validation ---
        if (!isValidEmail(email)) {
            errorEl.textContent = "Please enter a valid email address.";
            errorEl.style.display = 'block';
            toggleButtonLoading(button, false);
            return;
        }

        try {
            const response = await fetch(`${API_BASE_URL}/auth/signup`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ full_name: fullName, email, password }),
            });

            if (response.ok) {
                alert('Signup successful! A verification link has been sent (check your backend terminal).');
                showLoginBtn.click();
            } else {
                const error = await response.json();
                // --- NEW: More specific error messages ---
                if (error.detail.includes("Email already registered")) {
                    errorEl.textContent = "An account with this email already exists. Please sign in.";
                } else {
                    errorEl.textContent = "An unknown error occurred during signup.";
                }
                errorEl.style.display = 'block';
            }
        } catch (error) {
            errorEl.textContent = 'Could not connect to the server. Please try again later.';
            errorEl.style.display = 'block';
        } finally {
            toggleButtonLoading(button, false);
        }
    });
});
