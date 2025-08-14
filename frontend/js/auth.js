document.addEventListener('DOMContentLoaded', () => {
    const loginView = document.getElementById('login-view');
    const signupView = document.getElementById('signup-view');
    const showSignupBtn = document.getElementById('show-signup-btn');
    const showLoginBtn = document.getElementById('show-login-btn');
    const forgotPasswordBtn = document.getElementById('forgot-password-btn'); // New

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

    // --- NEW: Forgot Password Handler ---
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
    // --- END NEW ---

    const toggleButtonLoading = (button, isLoading) => {
        button.classList.toggle('loading', isLoading);
        button.disabled = isLoading;
    };

    loginForm.addEventListener('submit', async (e) => {
        // ... (this part remains the same)
        e.preventDefault();
        const button = loginForm.querySelector('.btn');
        const errorEl = document.getElementById('login-error');
        errorEl.textContent = '';
        toggleButtonLoading(button, true);

        const email = document.getElementById('login-email').value;
        const password = document.getElementById('login-password').value;

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
                errorEl.textContent = error.detail || 'Login failed. Please check your credentials.';
            }
        } catch (error) {
            errorEl.textContent = 'An error occurred. Please try again.';
        } finally {
            toggleButtonLoading(button, false);
        }
    });

    signupForm.addEventListener('submit', async (e) => {
        // ... (this part remains the same)
        e.preventDefault();
        const button = signupForm.querySelector('.btn');
        const errorEl = document.getElementById('signup-error');
        errorEl.textContent = '';
        toggleButtonLoading(button, true);

        const fullName = document.getElementById('signup-name').value;
        const email = document.getElementById('signup-email').value;
        const password = document.getElementById('signup-password').value;

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
                errorEl.textContent = error.detail || 'Signup failed. Please try again.';
            }
        } catch (error) {
            errorEl.textContent = 'An error occurred. Please try again.';
        } finally {
            toggleButtonLoading(button, false);
        }
    });
});
