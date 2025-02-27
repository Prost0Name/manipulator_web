from flask import Flask, jsonify, request
import json
import os
from datetime import datetime, timedelta

app = Flask(__name__)

# Функция для чтения данных из JSON
def read_data():
    if os.path.exists("data.json"):
        with open("data.json", "r") as f:
            data = json.load(f)
            return data.get("counter", 0), data.get("timestamps", [])
    return 0, []

# Функция для записи данных в JSON
def write_data(counter, timestamps):
    with open("data.json", "w") as f:
        json.dump({"counter": counter, "timestamps": timestamps}, f)

# Сброс счётчика
@app.route("/reset", methods=["POST"])
def reset_counter():
    write_data(0, [])
    return jsonify({"counter": 0, "average_time": None})

@app.route("/increment", methods=["POST"])
def increment():
    counter, timestamps = read_data()
    counter += 1
    timestamps.append(datetime.now().isoformat())
    write_data(counter, timestamps)
    return jsonify({"counter": counter})

@app.route("/counter", methods=["GET"])
def get_counter():
    counter, timestamps = read_data()

    # Рассчитываем среднее время изготовления
    if len(timestamps) > 1:
        time_diffs = []
        for i in range(1, len(timestamps)):
            t1 = datetime.fromisoformat(timestamps[i-1])
            t2 = datetime.fromisoformat(timestamps[i])
            time_diffs.append((t2 - t1).total_seconds())

        average_time = sum(time_diffs) / len(time_diffs)
    else:
        average_time = None

    # Рассчитываем количество изделий за последние 30 секунд
    now = datetime.now()
    last_30_seconds = now - timedelta(seconds=30)
    recent_count = sum(1 for t in timestamps if datetime.fromisoformat(t) > last_30_seconds)

    return jsonify({"counter": counter, "average_time": average_time, "recent_count": recent_count})

@app.route("/")
def index():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Мониторинг производства</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Inter', sans-serif; }
            body { background: #f8f9fa; color: #333; min-height: 100vh; display: flex; flex-direction: column; align-items: center; padding: 2rem; }
            .dashboard { max-width: 1200px; width: 100%; background: white; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); padding: 2rem; }
            .header { text-align: center; margin-bottom: 2rem; }
            .header h1 { font-size: 2rem; font-weight: 600; color: #2c3e50; }
            .counter-section { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; }
            .counter { font-size: 3rem; font-weight: 600; color: #2c3e50; }
            .average-time { font-size: 1.2rem; color: #7f8c8d; }
            .btn { background: #e74c3c; border: none; padding: 0.75rem 1.5rem; color: white; font-size: 1rem; border-radius: 8px; cursor: pointer; transition: background 0.3s ease; }
            .btn:hover { background: #c0392b; }
            .chart-container { background: white; border-radius: 12px; padding: 1.5rem; margin-top: 2rem; }
            canvas { width: 100% !important; height: 400px !important; }
        </style>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    </head>
    <body>
        <div class="dashboard">
            <div class="header">
                <h1>Мониторинг производства</h1>
                <p>Термопластавтомат №5 | Линия 3</p>
            </div>

            <div class="counter-section">
                <div>
                    <div class="counter" id="counter">0</div>
                    <small>Изготовлено изделий</small>
                </div>
                <button class="btn" id="resetBtn">Сброс</button>
            </div>
            <div class="average-time" id="averageTime">Среднее время: —</div>

            <div class="chart-container">
                <canvas id="productionChart"></canvas>
            </div>
        </div>

        <script>
            const counterElement = document.getElementById('counter');
            const averageTimeElement = document.getElementById('averageTime');
            const ctx = document.getElementById('productionChart').getContext('2d');
            let productionChart;

            const productionData = {
                labels: [],
                datasets: [{
                    label: 'Изготовлено за 30 сек',
                    data: [],
                    borderColor: '#2ecc71',
                    backgroundColor: 'rgba(46, 204, 113, 0.1)',
                    borderWidth: 2,
                    fill: true
                }]
            };

            function initChart() {
                productionChart = new Chart(ctx, {
                    type: 'line',
                    data: productionData,
                    options: { 
                        responsive: true, 
                        maintainAspectRatio: false
                    }
                });
            }

            async function fetchCounter() {
                try {
                    const response = await fetch('/counter');
                    const data = await response.json();
                    counterElement.textContent = data.counter;
                    averageTimeElement.textContent = data.average_time ? 
                        `Среднее время: ${data.average_time.toFixed(1)} сек.` : 'Среднее время: —';

                    const now = new Date();
                    const time = `${now.getHours()}:${String(now.getMinutes()).padStart(2, '0')}:${String(now.getSeconds()).padStart(2, '0')}`;
                    productionData.labels.push(time);
                    productionData.datasets[0].data.push(data.recent_count);

                    // Удерживаем только последние 12 точек
                    if (productionData.labels.length > 12) {
                        productionData.labels.shift();
                        productionData.datasets[0].data.shift();
                    }

                    // Сжимаем график
                    if (productionData.labels.length > 20) {
                        productionData.labels.shift();
                        productionData.datasets[0].data.shift();
                    }

                    productionChart.update();
                } catch (err) {
                    console.error('Ошибка:', err);
                }
            }

            document.getElementById('resetBtn').addEventListener('click', async () => {
                await fetch('/reset', { method: 'POST' });
                counterElement.textContent = '0';
                productionData.labels = [];
                productionData.datasets[0].data = [];
                productionChart.update();
            });

            initChart();
            fetchCounter();
            setInterval(fetchCounter, 5000);
        </script>
    </body>
    </html>
    '''

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
