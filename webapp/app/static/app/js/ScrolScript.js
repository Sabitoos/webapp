window.onload = function() {
        const content = document.getElementById('con');
        
        // Даем время на загрузку страницы, затем добавляем класс show
        setTimeout(() => {
            content.classList.add('show');
        }, 100); // Задержка перед началом анимации (можно настроить)
};

