document.addEventListener('DOMContentLoaded', () => {
    // Get references to all the necessary DOM elements
    const userInfoContainer = document.getElementById('user-info-container');
    const adminPanel = document.getElementById('admin-panel');
    const logoutBtn = document.getElementById('logout-btn');

    // Attach the logout function to the logout button's click event
    logoutBtn.addEventListener('click', logout);

    /**
     * Handles the access and refresh tokens passed as URL query parameters
     * after a successful social login redirect.
     */
    const handleSocialLoginTokens = () => {
        const params = new URLSearchParams(window.location.search);
        const token = params.get('token');
        const refreshToken = params.get('refresh_token');
        
        // If tokens are present, store them in localStorage
        if (token && refreshToken) {
            localStorage.setItem('accessToken', token);
            localStorage.setItem('refreshToken', refreshToken);
            // Use an absolute path to clean the URL correctly.
            window.history.replaceState({}, document.title, "/frontend/dashboard.html");
        }
    };

    /**
     * Renders the user's details into the user-info-container element.
     * @param {object} user - The user object received from the API.
     */
    const renderUserDetails = (user) => {
        userInfoContainer.innerHTML = `
            <div class="user-info">
                <p><strong>ID:</strong> ${user.id}</p>
                <p><strong>Name:</strong> ${user.full_name}</p>
                <p><strong>Email:</strong> ${user.email}</p>
                <p><strong>Role:</strong> ${user.role}</p>
            </div>
        `;
    };

    /**
     * Renders a link to the admin dashboard if the user is an admin.
     */
    const renderAdminPanel = () => {
        // This function now just adds a link to the new admin dashboard
        adminPanel.style.display = 'block';
        adminPanel.innerHTML = `
            <h3>Admin Tools</h3>
            <a href="/frontend/admin.html" class="btn" style="background-color: #ffc107; color: #212529; margin-top: 0;">Go to Admin Dashboard &rarr;</a>
        `;
    };

    /**
     * Initializes the dashboard by handling social login tokens and fetching user data.
     */
    const initializeDashboard = async () => {
        handleSocialLoginTokens();
        try {
            // Fetch the current user's details
            const response = await fetchWithAuth('/users/me');
            if (response.ok) {
                const user = await response.json();
                renderUserDetails(user);
                // If the user is an admin, render the admin panel link
                if (user.role === 'admin') {
                    renderAdminPanel();
                }
            } else {
                // If the request fails (e.g., token invalid), log the user out
                logout();
            }
        } catch (error) {
            console.error("Initialization failed:", error);
            logout();
        }
    };

    // Run the initialization function when the page loads
    initializeDashboard();
});
