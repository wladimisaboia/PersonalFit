window.saveExerciseStatus = function(exerciseId) {
    console.log('Iniciando saveExerciseStatus para exercício ID:', exerciseId);
    
    const select = document.querySelector(`select[data-exercise-id="${exerciseId}"]`);
    if (!select) {
        console.error('Select não encontrado para o exercício ID:', exerciseId);
        alert('Erro: Elemento de seleção não encontrado.');
        return;
    }

    const status = select.value;
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    const urlsElement = document.getElementById('urls');
    
    if (!urlsElement) {
        console.error('Elemento URLs não encontrado');
        alert('Erro: Configuração da página incompleta.');
        return;
    }

    const updateExerciseStatusUrl = urlsElement.dataset.updateStatusUrl;
    
    if (!updateExerciseStatusUrl) {
        console.error('URL de atualização não encontrada');
        alert('Erro: URL de atualização não configurada.');
        return;
    }

    console.log('Enviando requisição para:', updateExerciseStatusUrl);
    console.log('Dados:', { exercise_id: exerciseId, status: status });

    const saveButton = document.querySelector(`button[onclick="saveExerciseStatus(${exerciseId})"]`);
    if (saveButton) {
        saveButton.disabled = true;
        saveButton.textContent = 'Salvando...';
    }

    fetch(updateExerciseStatusUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': csrfToken
        },
        body: `exercise_id=${exerciseId}&status=${status}`
    })
    .then(response => {
        console.log('Resposta recebida:', response.status);
        if (!response.ok) {
            throw new Error(`Erro HTTP ${response.status}: ${response.statusText}`);
        }
        return response.json();
    })
    .then(data => {
        console.log('Dados recebidos:', data);
        
        if (data.status === 'success') {
            updateProgressChart();
            
            const exerciseElement = select.closest('.exercise-item');
            if (exerciseElement) {
                exerciseElement.classList.remove('pending', 'completed');
                exerciseElement.classList.add(status);
            }
            
            showNotification('Treino salvo com sucesso!', 'success');
        } else {
            throw new Error(data.message || 'Erro ao atualizar status.');
        }
    })
    .catch(error => {
        console.error('Erro na operação:', error);
        showNotification(error.message || 'Não foi possível completar a operação.', 'error');
    })
    .finally(() => {
        if (saveButton) {
            saveButton.disabled = false;
            saveButton.textContent = 'Salvar';
        }
    });
};

function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;
    
    Object.assign(notification.style, {
        position: 'fixed',
        top: '20px',
        right: '20px',
        padding: '15px 25px',
        borderRadius: '5px',
        zIndex: '1000',
        animation: 'fadeIn 0.3s ease-in'
    });

    switch (type) {
        case 'success':
            notification.style.backgroundColor = '#4CAF50';
            notification.style.color = 'white';
            break;
        case 'error':
            notification.style.backgroundColor = '#f44336';
            notification.style.color = 'white';
            break;
        default:
            notification.style.backgroundColor = '#2196F3';
            notification.style.color = 'white';
    }

    document.body.appendChild(notification);

    setTimeout(() => {
        notification.style.animation = 'fadeOut 0.3s ease-out';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

function updateProgressChart() {
    const chartInstance = Chart.getChart('trainingProgress');
    if (chartInstance) {
        chartInstance.destroy();
    }
    createProgressChart();
}

function createProgressChart() {
    const exercises = document.querySelectorAll('.status-select');
    let completed = 0;
    let pending = 0;

    exercises.forEach(select => {
        if (select.value === 'completed') {
            completed++;
        } else {
            pending++;
        }
    });

    const canvas = document.getElementById('trainingProgress');
    if (!canvas) {
        console.error('Canvas do gráfico não encontrado');
        return;
    }

    const ctx = canvas.getContext('2d');
    
    try {
        new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Concluídos', 'Pendentes'],
                datasets: [{
                    data: [completed, pending],
                    backgroundColor: ['#4CAF50', '#ddd'],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            padding: 20,
                            font: {
                                size: 14
                            }
                        }
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                const total = completed + pending;
                                const percentage = Math.round((context.raw / total) * 100);
                                return `${context.label}: ${context.raw} (${percentage}%)`;
                            }
                        }
                    }
                },
                animation: {
                    duration: 500,
                    easing: 'easeInOutQuart'
                }
            }
        });
    } catch (error) {
        console.error('Erro ao criar o gráfico:', error);
    }
}

const style = document.createElement('style');
style.textContent = `
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes fadeOut {
        from { opacity: 1; transform: translateY(0); }
        to { opacity: 0; transform: translateY(-20px); }
    }
    
    .exercise-item {
        transition: background-color 0.3s ease;
    }
    
    .exercise-item.completed {
        background-color: rgba(76, 175, 80, 0.1);
    }
    
    .exercise-item.pending {
        background-color: rgba(221, 221, 221, 0.1);
    }
`;
document.head.appendChild(style);

document.addEventListener('DOMContentLoaded', function() {
    console.log('Dashboard JS carregado');
    
    createProgressChart();
    
    document.querySelectorAll('.status-select').forEach(select => {
        select.addEventListener('change', function() {
            const exerciseItem = this.closest('.exercise-item');
            if (exerciseItem) {
                exerciseItem.classList.remove('pending', 'completed');
                exerciseItem.classList.add(this.value);
            }
        });
    });
});

document.addEventListener('DOMContentLoaded', function() {
    const scheduleForm = document.getElementById('schedule-form');
    const scheduleSubmit = document.getElementById('schedule-submit');

    if (scheduleForm && scheduleSubmit) {
        scheduleForm.addEventListener('submit', function(event) {
            event.preventDefault();

            const formData = new FormData(scheduleForm);
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

            scheduleSubmit.disabled = true;
            scheduleSubmit.textContent = 'Agendando...';

            fetch(scheduleForm.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': csrfToken,
                    'X-Requested-With': 'XMLHttpRequest',
                    'Accept': 'application/json'
                }
            })
            .then(response => {
                console.log('Response status:', response.status);
                console.log('Response headers:', response.headers);
                
                return response.text().then(text => {
                    console.log('Response text:', text);
                    
                    try {
                        return JSON.parse(text);
                    } catch (e) {
                        throw new Error('Resposta inválida: ' + text);
                    }
                });
            })
            .then(data => {
                if (data.status === 'success') {
                    showNotification(data.message, 'success');
                    
                    setTimeout(() => {
                        window.location.href = data.redirect_url || '{% url "student_dashboard" %}';
                    }, 2000);
                } else {
                    throw new Error(data.message || 'Erro ao agendar consulta');
                }
            })
            .catch(error => {
                console.error('Erro completo:', error);
                showNotification(error.message || 'Não foi possível agendar a consulta.', 'error');
            })
            .finally(() => {
                scheduleSubmit.disabled = false;
                scheduleSubmit.textContent = 'Agendar Consulta';
            });
        });
    }
});

document.addEventListener('DOMContentLoaded', function() {
    // Login Form Handling
    const loginForm = document.getElementById('login-form');
    const loginSubmit = document.getElementById('login-submit');

    if (loginForm && loginSubmit) {
        loginForm.addEventListener('submit', function(event) {
            event.preventDefault();

            const formData = new FormData(loginForm);
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

            loginSubmit.disabled = true;
            loginSubmit.textContent = 'Entrando...';

            fetch(loginForm.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': csrfToken,
                    'X-Requested-With': 'XMLHttpRequest',
                    'Accept': 'application/json'
                }
            })
            .then(response => {
                return response.text().then(text => {
                    try {
                        return JSON.parse(text);
                    } catch (e) {
                        throw new Error('Resposta inválida: ' + text);
                    }
                });
            })
            .then(data => {
                if (data.status === 'success') {
                    showNotification(data.message, 'success');
                    
                    setTimeout(() => {
                        window.location.href = data.redirect_url;
                    }, 2000);
                } else {
                    throw new Error(data.message || 'Erro ao fazer login');
                }
            })
            .catch(error => {
                console.error('Erro completo:', error);
                showNotification(error.message || 'Não foi possível fazer login.', 'error');
            })
            .finally(() => {
                loginSubmit.disabled = false;
                loginSubmit.textContent = 'Entrar';
            });
        });
    }

    // Register Form Handling
    const registerForm = document.getElementById('register-form');
    const registerSubmit = document.getElementById('register-submit');

    if (registerForm && registerSubmit) {
        registerForm.addEventListener('submit', function(event) {
            event.preventDefault();

            const formData = new FormData(registerForm);
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

            registerSubmit.disabled = true;
            registerSubmit.textContent = 'Cadastrando...';

            fetch(registerForm.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': csrfToken,
                    'X-Requested-With': 'XMLHttpRequest',
                    'Accept': 'application/json'
                }
            })
            .then(response => {
                return response.text().then(text => {
                    try {
                        return JSON.parse(text);
                    } catch (e) {
                        throw new Error('Resposta inválida: ' + text);
                    }
                });
            })
            .then(data => {
                if (data.status === 'success') {
                    showNotification(data.message, 'success');
                    
                    setTimeout(() => {
                        window.location.href = data.redirect_url;
                    }, 2000);
                } else {
                    throw new Error(data.message || 'Erro ao se cadastrar');
                }
            })
            .catch(error => {
                console.error('Erro completo:', error);
                showNotification(error.message || 'Não foi possível fazer o cadastro.', 'error');
            })
            .finally(() => {
                registerSubmit.disabled = false;
                registerSubmit.textContent = 'Cadastrar';
            });
        });
    }
});

document.addEventListener('DOMContentLoaded', function() {
    const availabilityForm = document.getElementById('availability-form');
    const availabilitySubmit = document.getElementById('availability-submit');

    if (availabilityForm && availabilitySubmit) {
        availabilityForm.addEventListener('submit', function(event) {
            event.preventDefault();

            const formData = new FormData(availabilityForm);
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

            availabilitySubmit.disabled = true;
            availabilitySubmit.textContent = 'Adicionando...';

            fetch(availabilityForm.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': csrfToken,
                    'X-Requested-With': 'XMLHttpRequest',
                    'Accept': 'application/json'
                }
            })
            .then(response => {
                return response.text().then(text => {
                    try {
                        return JSON.parse(text);
                    } catch (e) {
                        throw new Error('Resposta inválida: ' + text);
                    }
                });
            })
            .then(data => {
                if (data.status === 'success') {
                    showNotification(data.message, 'success');
                    
                    setTimeout(() => {
                        window.location.href = data.redirect_url;
                    }, 2000);
                } else {
                    throw new Error(data.message || 'Erro ao adicionar disponibilidade');
                }
            })
            .catch(error => {
                console.error('Erro completo:', error);
                showNotification(error.message || 'Não foi possível adicionar disponibilidade.', 'error');
            })
            .finally(() => {
                availabilitySubmit.disabled = false;
                availabilitySubmit.textContent = 'Adicionar Disponibilidade';
            });
        });
    }
});

document.addEventListener('DOMContentLoaded', function() {
    const trainingForm = document.getElementById('training-form');
    const trainingSubmit = document.querySelector('button[type="submit"]');
    if (trainingForm && trainingSubmit) {
        trainingForm.addEventListener('submit', function(event) {
            event.preventDefault();
            const formData = new FormData(trainingForm);
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            
            trainingSubmit.disabled = true;
            trainingSubmit.textContent = 'Atribuindo...';
            fetch('', {  
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': csrfToken,
                    'X-Requested-With': 'XMLHttpRequest',
                    'Accept': 'application/json'
                }
            })
            .then(response => {
                return response.text().then(text => {
                    try {
                        return JSON.parse(text);
                    } catch (e) {
                        throw new Error('Resposta inválida: ' + text);
                    }
                });
            })
            .then(data => {
                if (data.status === 'success') {
                    showNotification(data.message, 'success');
                    
                    setTimeout(() => {
                        window.location.href = data.redirect_url;
                    }, 2000);
                } else {
                    throw new Error(data.message || 'Erro ao atribuir treino');
                }
            })
            .catch(error => {
                console.error('Erro completo:', error);
                showNotification(error.message || 'Não foi possível atribuir o treino.', 'error');
            })
            .finally(() => {
                trainingSubmit.disabled = false;
                trainingSubmit.textContent = 'Atribuir Plano';
            });
        });
    }
});

document.addEventListener('DOMContentLoaded', function() {
    const studentUpdateForm = document.getElementById('student-update-form');
    const studentUpdateSubmit = document.querySelector('button[type="submit"]');
    
    if (studentUpdateForm && studentUpdateSubmit) {
        studentUpdateForm.addEventListener('submit', function(event) {
            event.preventDefault();
            const formData = new FormData(studentUpdateForm);
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            
            studentUpdateSubmit.disabled = true;
            studentUpdateSubmit.textContent = 'Atualizando...';
            
            fetch('', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': csrfToken,
                    'X-Requested-With': 'XMLHttpRequest',
                    'Accept': 'application/json'
                }
            })
            .then(response => {
                return response.text().then(text => {
                    try {
                        return JSON.parse(text);
                    } catch (e) {
                        throw new Error('Resposta inválida: ' + text);
                    }
                });
            })
            .then(data => {
                if (data.status === 'success') {
                    showNotification(data.message, 'success');
                    
                    setTimeout(() => {
                        window.location.href = data.redirect_url;
                    }, 2000);
                } else {
                    throw new Error(data.message || 'Erro ao atualizar informações');
                }
            })
            .catch(error => {
                console.error('Erro completo:', error);
                showNotification(error.message || 'Não foi possível atualizar as informações.', 'error');
            })
            .finally(() => {
                studentUpdateSubmit.disabled = false;
                studentUpdateSubmit.textContent = 'Atualizar Informações';
            });
        });
    }
});

document.addEventListener('DOMContentLoaded', function() {
    const availabilityList = document.querySelector('.availability-list');
    
    if (availabilityList) {
        availabilityList.addEventListener('submit', function(event) {
            // Verifica se o botão de cancelamento foi clicado
            if (event.target.tagName === 'FORM' && event.target.querySelector('button[type="submit"]')) {
                event.preventDefault();
                const form = event.target;
                const url = form.action;
                const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
                const submitButton = form.querySelector('button[type="submit"]');
                
                submitButton.disabled = true;
                submitButton.textContent = 'Cancelando...';
                
                fetch(url, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': csrfToken,
                        'X-Requested-With': 'XMLHttpRequest',
                        'Accept': 'application/json'
                    }
                })
                .then(response => {
                    return response.text().then(text => {
                        try {
                            return JSON.parse(text);
                        } catch (e) {
                            throw new Error('Resposta inválida: ' + text);
                        }
                    });
                })
                .then(data => {
                    if (data.status === 'success') {
                        showNotification(data.message, 'success');
                        
                        setTimeout(() => {
                            window.location.href = data.redirect_url;
                        }, 2000);
                    } else {
                        showNotification(data.message, 'error');
                    }
                })
                .catch(error => {
                    console.error('Erro completo:', error);
                    showNotification('Erro ao processar solicitação', 'error');
                })
                .finally(() => {
                    submitButton.disabled = false;
                    submitButton.textContent = 'Cancelar';
                });
            }
        });
    }
});
