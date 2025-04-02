window.onload = function() {
    const content = document.getElementById('con');
    
    // Даем время на загрузку страницы, затем добавляем класс show
    setTimeout(() => {
        content.classList.add('show');
    }, 100); // Задержка перед началом анимации (можно настроить)
};

document.addEventListener('DOMContentLoaded', function() {
// Находим только параграфы, содержащие слово "лет"
const paragraphsWithAge = Array.from(document.querySelectorAll('p')).filter(p => 
    p.textContent.match(/\d+\s*лет/i)
);

// Функция для определения правильной формы
function getAgeWord(age) {
    age = parseInt(age);
    const lastDigit = age % 10;
    const lastTwoDigits = age % 100;
    
    if (lastDigit === 1 && lastTwoDigits !== 11) {
        return 'год';
    } else if ([2, 3, 4].includes(lastDigit) && ![12, 13, 14].includes(lastTwoDigits)) {
        return 'года';
    } else {
        return 'лет'; // Оставим "лет", если форма правильная
    }
}

// Обрабатываем только найденные параграфы
paragraphsWithAge.forEach(paragraph => {
    const text = paragraph.textContent;
    // Ищем конкретно формат "число лет"
    const match = text.match(/(\d+)\s*лет/i);
    
    if (match) {
        const age = match[1];
        const correctWord = getAgeWord(age);
        // Заменяем только если форма изменилась
        if (correctWord !== 'лет') {
            paragraph.textContent = text.replace(/(\d+)\s*лет/i, `${age} ${correctWord}`);
        }
    }
});
});

document.getElementById('myForm').addEventListener('submit', function(e) {
e.preventDefault(); // Предотвращаем стандартную отправку формы
processInput(); // Вызываем функцию обработки
});

function processInput() {
const input = document.getElementById('input').value;
console.log('Введено:', input);
// Здесь ваша логика обработки ввода
}

document.getElementById('input').addEventListener('keypress', function(e) {
if (e.key === 'Enter') {
  e.preventDefault();
  processInput();
}
});


