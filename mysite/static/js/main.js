// Оновлений main.js
document.addEventListener('DOMContentLoaded', function() {
    // Анімація кнопок при наведенні
    const buttons = document.querySelectorAll('.btn-discord, .btn-join');
    buttons.forEach(btn => {
        btn.addEventListener('mouseenter', function() {
            this.style.boxShadow = this.classList.contains('btn-discord')
                ? '0 4px 15px rgba(88, 101, 242, 0.6)'
                : '0 4px 15px rgba(30, 144, 255, 0.6)';
        });
        btn.addEventListener('mouseleave', function() {
            this.style.boxShadow = 'none';
        });
    });

    console.log('Сторінка завантажена!');
});