// Инициализация графика
const ctx = document.getElementById('counterChart').getContext('2d');
const chart = new Chart(ctx, {
    type: 'line', // Тип графика — линейный
    data: {
        labels: [], // Временные метки (ось X)
        datasets: [{
            label: 'Значение счетчика', // Название графика
            data: [], // Значения счетчика (ось Y)
            borderColor: '#007bff', // Цвет линии
            fill: false, // Не заливать область под линией
        }]
    },
    options: {
        responsive: true, // График будет адаптивным
        scales: {
            x: {
                type: 'time', // Используем временную шкалу для оси X
                time: {
                    unit: 'second', // Единица измерения — секунды
                    displayFormats: {
                        second: 'HH:mm:ss' // Формат отображения времени
                    }
                },
                title: {
                    display: true,
                    text: 'Время' // Название оси X
                }
            },
            y: {
                title: {
                    display: true,
                    text: 'Значение счетчика' // Название оси Y
                }
            }
        }
    }
});

// Функция для обновления графика
function updateChart() {
    fetch('/counter')
    .then(response => response.json())
    .then(data => {
        const history = data.history;

        // Обновляем данные графика
        chart.data.labels = history.map(entry => entry.timestamp); // Временные метки
        chart.data.datasets[0].data = history.map(entry => entry.value); // Значения счетчика
        chart.update(); // Обновляем график
    })
    .catch(error => console.error('Ошибка:', error));
}

// Обновляем счетчик и график при нажатии на кнопку
document.getElementById('increment-btn').addEventListener('click', function() {
    fetch('/increment', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('counter').textContent = data.counter; // Обновляем счетчик
        updateChart(); // Обновляем график
    })
    .catch(error => console.error('Ошибка:', error));
});

// Первоначальное обновление графика при загрузке страницы
updateChart();