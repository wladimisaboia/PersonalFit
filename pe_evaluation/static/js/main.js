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