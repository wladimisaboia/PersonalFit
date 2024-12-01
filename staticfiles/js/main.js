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
