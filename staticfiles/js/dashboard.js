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