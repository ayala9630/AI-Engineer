// Task API functions
async function addTask() {
    const title = document.getElementById('taskTitle').value.trim();
    const description = document.getElementById('taskDescription').value.trim();
    const priority = document.getElementById('taskPriority').value;

    if (!title) {
        alert('Please enter a task title');
        return;
    }

    try {
        const response = await fetch('/api/task/add', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                title: title,
                description: description,
                priority: priority
            })
        });

        const data = await response.json();

        if (data.success) {
            // Clear form
            document.getElementById('taskTitle').value = '';
            document.getElementById('taskDescription').value = '';
            document.getElementById('taskPriority').value = 'medium';
            
            // Reload page to show new task
            setTimeout(() => location.reload(), 300);
        } else {
            alert('Error: ' + data.error);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Failed to add task');
    }
}

async function toggleTask(taskId) {
    try {
        const response = await fetch(`/api/task/${taskId}/toggle`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        });

        const data = await response.json();

        if (data.success) {
            // Reload to reflect changes
            setTimeout(() => location.reload(), 300);
        } else {
            alert('Failed to update task: ' + (data.error || 'Unknown error'));
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Failed to update task');
    }
}

async function deleteTask(taskId) {
    if (confirm('Are you sure you want to delete this task?')) {
        try {
            const response = await fetch(`/api/task/${taskId}/delete`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            });

            const data = await response.json();

            if (data.success) {
                // Remove task from DOM
                const taskElement = document.querySelector(`[data-task-id="${taskId}"]`);
                if (taskElement) {
                    taskElement.style.animation = 'slideUp 0.3s ease';
                    setTimeout(() => {
                        taskElement.remove();
                        location.reload();
                    }, 300);
                }
            } else {
                alert('Failed to delete task: ' + (data.error || 'Unknown error'));
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Failed to delete task');
        }
    }
}

async function loadStats() {
    try {
        const response = await fetch('/api/stats');
        const data = await response.json();

        document.getElementById('totalTasks').textContent = data.total;
        document.getElementById('completedTasks').textContent = data.completed;
        document.getElementById('pendingTasks').textContent = data.pending;
        document.getElementById('completionRate').textContent = data.completion_rate + '%';
    } catch (error) {
        console.error('Error loading stats:', error);
    }
}

// Modal functions
function editTaskModal(taskId, title, description, priority) {
    document.getElementById('editTaskId').value = taskId;
    document.getElementById('editTaskTitle').value = title;
    document.getElementById('editTaskDescription').value = description;
    document.getElementById('editTaskPriority').value = priority;
    document.getElementById('editModal').style.display = 'block';
}

function closeEditModal() {
    document.getElementById('editModal').style.display = 'none';
}

async function saveTaskEdit() {
    const taskId = document.getElementById('editTaskId').value;
    const title = document.getElementById('editTaskTitle').value.trim();
    const description = document.getElementById('editTaskDescription').value.trim();
    const priority = document.getElementById('editTaskPriority').value;

    if (!title) {
        alert('Please enter a task title');
        return;
    }

    try {
        const response = await fetch(`/api/task/${taskId}/edit`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                title: title,
                description: description,
                priority: priority
            })
        });

        const data = await response.json();

        if (data.success) {
            closeEditModal();
            location.reload();
        } else {
            alert('Error: ' + data.error);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Failed to update task');
    }
}

// Close modal when clicking outside
window.onclick = function(event) {
    const modal = document.getElementById('editModal');
    if (event.target == modal) {
        modal.style.display = 'none';
    }
}
