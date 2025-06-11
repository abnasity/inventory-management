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

// Handle bulk selections
document.addEventListener('DOMContentLoaded', function() {
    const selectAllCheckbox = document.getElementById('selectAllUsers');
    const userCheckboxes = document.querySelectorAll('.user-select');
    const bulkActionsBtn = document.getElementById('bulkActionsBtn');
    const bulkActionsDropdown = document.getElementById('bulkActionsDropdown');
    const selectedCountBadge = document.querySelector('.selected-count');

    selectAllCheckbox?.addEventListener('change', function() {
        userCheckboxes.forEach(checkbox => {
            if (!checkbox.disabled) {
                checkbox.checked = this.checked;
            }
        });
        updateBulkActionsVisibility();
    });

    userCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', updateBulkActionsVisibility);
    });

    function updateBulkActionsVisibility() {
        const selectedCount = document.querySelectorAll('.user-select:checked').length;
        selectedCountBadge.textContent = selectedCount;
        bulkActionsBtn.disabled = selectedCount === 0;
        bulkActionsDropdown.style.display = selectedCount > 0 ? 'block' : 'none';
    }
});

// Bulk actions
async function bulkActivate() {
    await bulkUpdateStatus(true);
}

async function bulkDeactivate() {
    await bulkUpdateStatus(false);
}

async function bulkUpdateStatus(activate) {
    const selectedUsers = Array.from(document.querySelectorAll('.user-select:checked'))
        .map(checkbox => checkbox.value);
    
    if (!selectedUsers.length) return;
    
    const action = activate ? 'activate' : 'deactivate';
    if (!confirm(`Are you sure you want to ${action} ${selectedUsers.length} users?`)) {
        return;
    }

    try {
        const response = await fetch('/auth/users/bulk_status', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('input[name="csrf_token"]').value
            },
            body: JSON.stringify({
                user_ids: selectedUsers,
                activate: activate
            })
        });

        const data = await response.json();
        if (data.success) {
            location.reload();
        } else {
            alert(data.error || 'Failed to update users');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred during bulk update');
    }
}

// Password strength meter
function checkPasswordStrength(password) {
    let strength = 0;
    const feedback = [];

    // Length check
    if (password.length < 8) {
        feedback.push('Password should be at least 8 characters long');
    } else {
        strength += 1;
    }

    // Contains number
    if (/\d/.test(password)) {
        strength += 1;
    } else {
        feedback.push('Add numbers');
    }

    // Contains lowercase
    if (/[a-z]/.test(password)) {
        strength += 1;
    } else {
        feedback.push('Add lowercase letters');
    }

    // Contains uppercase
    if (/[A-Z]/.test(password)) {
        strength += 1;
    } else {
        feedback.push('Add uppercase letters');
    }

    // Contains special char
    if (/[^A-Za-z0-9]/.test(password)) {
        strength += 1;
    } else {
        feedback.push('Add special characters');
    }

    return {
        score: strength,
        feedback: feedback.join(', ')
    };
}

// Add password strength meter to password fields
document.addEventListener('DOMContentLoaded', function() {
    const passwordInputs = document.querySelectorAll('input[type="password"]');
    passwordInputs.forEach(input => {
        const meterContainer = document.createElement('div');
        meterContainer.className = 'password-strength-meter mt-2';
        meterContainer.innerHTML = `
            <div class="progress" style="height: 5px;">
                <div class="progress-bar" role="progressbar" style="width: 0%"></div>
            </div>
            <small class="form-text text-muted feedback-text"></small>
        `;
        input.parentNode.insertBefore(meterContainer, input.nextSibling);

        input.addEventListener('input', function() {
            const strength = checkPasswordStrength(this.value);
            const progressBar = meterContainer.querySelector('.progress-bar');
            const feedbackText = meterContainer.querySelector('.feedback-text');

            // Update progress bar
            progressBar.style.width = `${(strength.score / 5) * 100}%`;
            progressBar.className = 'progress-bar';
            if (strength.score <= 2) {
                progressBar.classList.add('bg-danger');
            } else if (strength.score <= 3) {
                progressBar.classList.add('bg-warning');
            } else {
                progressBar.classList.add('bg-success');
            }

            // Update feedback text
            feedbackText.textContent = strength.feedback || 'Strong password';
        });
    });
});
