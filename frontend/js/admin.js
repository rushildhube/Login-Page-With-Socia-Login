document.addEventListener('DOMContentLoaded', () => {
    // Get references to the container elements in admin.html
    const allUsersContainer = document.getElementById('all-users-container');
    const loginHistoryContainer = document.getElementById('login-history-container');

    /**
     * Fetches the list of all users from the /admin/users endpoint
     * and renders them into the all-users-container.
     */
    const renderUsers = async () => {
        try {
            // Use the authenticated fetch wrapper from api.js
            const response = await fetchWithAuth('/admin/users');
            if (response.ok) {
                const users = await response.json();
                // Create an HTML string for each user and join them together
                let usersHtml = users.map(u => `
                    <div class="user-info" style="border-left-color: var(--secondary-color);">
                        <p><strong>${u.full_name}</strong> (${u.email}) - Role: ${u.role}</p>
                    </div>
                `).join('');
                allUsersContainer.innerHTML = usersHtml;
            } else {
                allUsersContainer.innerHTML = "<p>Failed to load users.</p>";
            }
        } catch (error) {
            allUsersContainer.innerHTML = "<p>An error occurred while loading users.</p>";
        }
    };

    /**
     * Fetches the recent login history from the /admin/login-history endpoint
     * and renders it into the login-history-container.
     */
    const renderLoginHistory = async () => {
        try {
            const response = await fetchWithAuth('/admin/login-history');
            if (response.ok) {
                const history = await response.json();
                // Create an HTML string for each login event, formatting the timestamp
                let historyHtml = history.map(h => `
                    <div class="user-info" style="border-left-color: #ffc107;">
                        <p><strong>${h.user_email}</strong> logged in via <strong>${h.login_type}</strong> at ${new Date(h.timestamp).toLocaleString()}</p>
                    </div>
                `).join('');
                loginHistoryContainer.innerHTML = historyHtml;
            } else {
                loginHistoryContainer.innerHTML = "<p>Failed to load login history.</p>";
            }
        } catch (error) {
            loginHistoryContainer.innerHTML = "<p>An error occurred while loading login history.</p>";
        }
    };

    // Call both functions to populate the admin dashboard when the page loads
    renderUsers();
    renderLoginHistory();
});
