function toggleUserStatus(userId, action) {
    if (!confirm(`Are you sure you want to ${action} this user?`)) {
        return;
    }

    fetch(`/auth/users/${userId}/toggle_status`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('input[name="csrf_token"]').value
        }
    })
    .then(response => response.json())
    .then(data => {
        if (!data.success) {
            alert(data.error);
        } else {
            alert(data.message);
            location.reload(); // Refresh to show updated status
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while updating user status');
    });
}

async function editUser(userId) {
    try {
        const response = await fetch(`/auth/users/${userId}`);
        if (!response.ok) {
            throw new Error('Failed to fetch user data');
        }

        const user = await response.json();
        
        // Fill the edit form with user data
        document.getElementById('edit_user_id').value = user.id;
        document.getElementById('edit_username').value = user.username;
        document.getElementById('edit_email').value = user.email;
        document.getElementById('edit_role').value = user.role;
        document.getElementById('edit_password').value = ''; // Clear password field

        // Set the form action with the correct URL prefix
        const form = document.getElementById('editUserForm');
        form.action = `/auth/users/${userId}/edit`;

        // Show the modal
        const editModal = new bootstrap.Modal(document.getElementById('editUserModal'));
        editModal.show();
    } catch (error) {
        console.error('Error:', error);
        alert('Failed to load user data: ' + error.message);
    }
}
