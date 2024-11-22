document.addEventListener('DOMContentLoaded', function() {
    console.log('Dashboard JS loaded');

    // Exemplo de funcionalidade específica do dashboard
    const studentList = document.getElementById('student-list');
    if (studentList) {
        studentList.addEventListener('click', function(event) {
            if (event.target.tagName === 'A' && event.target.textContent === 'Assign Training Plan') {
                event.preventDefault();
                alert('Redirecting to assign training plan...');
                window.location.href = event.target.href;
            }
        });
    }
});

document.addEventListener('DOMContentLoaded', function() {
    console.log('Main JS loaded');

    // Exemplo de funcionalidade global
    const messages = document.querySelector('.messages');
    if (messages) {
        setTimeout(() => {
            messages.style.display = 'none';
        }, 5000);
    }
});

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

    const ctx = document.getElementById('trainingProgress').getContext('2d');
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Concluídos', 'Pendentes'],
            datasets: [{
                data: [completed, pending],
                backgroundColor: ['#4CAF50', '#ddd'],
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });
}

function saveExerciseStatus(exerciseId) {
    const select = document.querySelector(`select[data-exercise-id="${exerciseId}"]`);
    const status = select.value;
    
    fetch('/update_exercise_status/', {  // Ajuste a URL conforme necessário
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        body: `exercise_id=${exerciseId}&status=${status}`
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            const chartInstance = Chart.getChart('trainingProgress');
            if (chartInstance) {
                chartInstance.destroy();
            }
            createProgressChart();
            alert('Status atualizado com sucesso!');
        } else {
            alert('Erro ao atualizar status.');
        }
    });
}

document.addEventListener('DOMContentLoaded', createProgressChart);

