// Define the base URL for the backend API to avoid repeating it.
const API_URL = 'http://127.0.0.1:8000';

/**
 * A custom fetch wrapper that automatically handles JWT access token refreshing.
 * @param {string} url - The API endpoint to call (e.g., '/users/me').
 * @param {object} options - The options for the fetch request (e.g., method, body).
 * @returns {Promise<Response>} A promise that resolves to the fetch response.
 */
async function fetchWithAuth(url, options = {}) {
    let token = localStorage.getItem('accessToken');
    
    // If no token is found, redirect to the login page immediately.
    if (!token) {
        logout();
        return Promise.reject("No access token found.");
    }

    // Set the default headers for an authenticated request.
    options.headers = {
        ...options.headers,
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
    };

    // Make the initial API request.
    let response = await fetch(API_URL + url, options);

    // Check if the request failed due to an expired access token (401 Unauthorized).
    if (response.status === 401) {
        const refreshToken = localStorage.getItem('refreshToken');
        
        // If there's no refresh token, the session has fully expired. Log out.
        if (!refreshToken) {
            logout();
            return Promise.reject("Session expired.");
        }

        try {
            // Attempt to get a new access token using the refresh token.
            const refreshResponse = await fetch(`${API_URL}/auth/refresh`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ refresh_token: refreshToken })
            });

            if (refreshResponse.ok) {
                const data = await refreshResponse.json();
                // Store the new access token.
                localStorage.setItem('accessToken', data.access_token);
                
                // Update the authorization header and retry the original request.
                options.headers['Authorization'] = `Bearer ${data.access_token}`;
                response = await fetch(API_URL + url, options);
            } else {
                // If the refresh token is also invalid, log the user out.
                logout();
                return Promise.reject("Session expired.");
            }
        } catch (error) {
            // If the refresh attempt fails for any other reason, log out.
            logout();
            return Promise.reject("Session refresh failed.");
        }
    }
    return response;
}

/**
 * Logs the user out by clearing tokens and redirecting to the index page.
 */
function logout() {
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
    // --- CRITICAL CHANGE ---
    // Use an absolute path to ensure the redirect works from any page.
    window.location.href = '/frontend/index.html';
    // --- END OF CHANGE ---
}
