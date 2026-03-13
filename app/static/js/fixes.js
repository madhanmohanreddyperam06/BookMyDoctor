// JavaScript fixes for template syntax issues

// Function to handle status updates
function updateStatus(appointmentId, status) {
    if (confirm('Are you sure you want to update this appointment status?')) {
        fetch(`/doctor/appointment/${appointmentId}/update_status`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-Requested-With': 'XMLHttpRequest'
            },
            body: `status=${status}`
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showAlert('Appointment status updated successfully', 'success');
                setTimeout(() => location.reload(), 1500);
            } else {
                showAlert('Failed to update status', 'danger');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showAlert('An error occurred', 'danger');
        });
    }
}

// Function to handle speciality activation/deactivation
function activateSpeciality(specialityId) {
    fetch(`/admin/specialities/${specialityId}/activate`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showAlert('Speciality activated successfully!', 'success');
            setTimeout(() => location.reload(), 1500);
        } else {
            showAlert('Failed to activate speciality', 'danger');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showAlert('An error occurred', 'danger');
    });
}

function deactivateSpeciality(specialityId) {
    if (confirm('Are you sure you want to deactivate this speciality?')) {
        fetch(`/admin/specialities/${specialityId}/deactivate`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showAlert('Speciality deactivated successfully!', 'warning');
                setTimeout(() => location.reload(), 1500);
            } else {
                showAlert('Failed to deactivate speciality', 'danger');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showAlert('An error occurred', 'danger');
        });
    }
}

// Function to handle doctor activation/deactivation
function activateDoctor(doctorId) {
    fetch(`/admin/doctors/${doctorId}/activate`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showAlert('Doctor activated successfully!', 'success');
            setTimeout(() => location.reload(), 1500);
        } else {
            showAlert('Failed to activate doctor', 'danger');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showAlert('An error occurred', 'danger');
    });
}

function deactivateDoctor(doctorId) {
    if (confirm('Are you sure you want to deactivate this doctor?')) {
        fetch(`/admin/doctors/${doctorId}/deactivate`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showAlert('Doctor deactivated successfully!', 'warning');
                setTimeout(() => location.reload(), 1500);
            } else {
                showAlert('Failed to deactivate doctor', 'danger');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showAlert('An error occurred', 'danger');
        });
    }
}

// Function to handle shift cancellation
function cancelShift(shiftId) {
    if (confirm('Are you sure you want to cancel this shift?')) {
        fetch(`/admin/shifts/${shiftId}/cancel`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showAlert('Shift cancelled successfully!', 'warning');
                setTimeout(() => location.reload(), 1500);
            } else {
                showAlert('Failed to cancel shift', 'danger');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showAlert('An error occurred', 'danger');
        });
    }
}

// Initialize event listeners when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Add event listeners for all buttons with data-action attributes
    document.querySelectorAll('[data-action]').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const action = this.dataset.action;
            const id = this.dataset.id;
            const status = this.dataset.status;
            
            switch(action) {
                case 'updateStatus':
                    updateStatus(id, status);
                    break;
                case 'activateSpeciality':
                    activateSpeciality(id);
                    break;
                case 'deactivateSpeciality':
                    deactivateSpeciality(id);
                    break;
                case 'activateDoctor':
                    activateDoctor(id);
                    break;
                case 'deactivateDoctor':
                    deactivateDoctor(id);
                    break;
                case 'cancelShift':
                    cancelShift(id);
                    break;
            }
        });
    });
    
    // Handle progress bar data-width attributes
    document.querySelectorAll('.progress-bar[data-width]').forEach(progressBar => {
        const widthData = progressBar.dataset.width;
        if (widthData) {
            const [booked, max] = widthData.split('-').map(Number);
            const percentage = max > 0 ? (booked / max) * 100 : 0;
            progressBar.style.width = percentage + '%';
        }
    });
});
