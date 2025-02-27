from flask import Flask, jsonify, request
import json
import os

app = Flask(__name__)

# Функции read_counter и write_counter остаются без изменений

@app.route("/increment", methods=["POST"])
def increment():
    counter = read_counter() + 1
    write_counter(counter)
    return jsonify({"counter": counter})

@app.route("/counter", methods=["GET"])
def get_counter():
    counter = read_counter()
    return jsonify({"counter": counter})

@app.route("/")
def index():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Quantum Counter</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
                font-family: 'Segoe UI', sans-serif;
            }

            body {
                background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
                height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                overflow: hidden;
            }

            .container {
                text-align: center;
                position: relative;
            }

            .counter-box {
                background: rgba(255, 255, 255, 0.1);
                backdrop-filter: blur(10px);
                border-radius: 20px;
                padding: 40px 60px;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
                border: 1px solid rgba(255, 255, 255, 0.1);
                transform-style: preserve-3d;
                perspective: 1000px;
            }

            .counter {
                font-size: 12rem;
                font-weight: 700;
                color: #fff;
                text-shadow: 0 0 20px rgba(79, 192, 255, 0.6);
                margin: 2rem 0;
                transition: all 0.3s ease;
            }

            .btn {
                background: linear-gradient(45deg, #4fc0ff, #7964ff);
                border: none;
                padding: 1.5rem 3rem;
                color: white;
                font-size: 1.5rem;
                border-radius: 50px;
                cursor: pointer;
                transition: all 0.3s ease;
                position: relative;
                overflow: hidden;
                transform: translateZ(20px);
            }

            .btn:hover {
                transform: translateY(-3px) scale(1.05);
                box-shadow: 0 10px 30px rgba(79, 192, 255, 0.4);
            }

            .btn:active {
                transform: translateY(0) scale(0.95);
            }

            .particles {
                position: absolute;
                width: 100%;
                height: 100%;
                pointer-events: none;
                top: 0;
                left: 0;
            }

            @keyframes float {
                0%, 100% { transform: translateY(0); }
                50% { transform: translateY(-20px); }
            }

            @media (max-width: 768px) {
                .counter {
                    font-size: 8rem;
                }
                .btn {
                    padding: 1rem 2rem;
                    font-size: 1.2rem;
                }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="counter-box">
                <h1 class="counter" id="counter">0</h1>
                <button class="btn" id="incrementBtn">INCREMENT++</button>
            </div>
            <div class="particles"></div>
        </div>

        <script>
            const counterElement = document.getElementById('counter');
            const btn = document.getElementById('incrementBtn');
            
            // Функция обновления счетчика с анимацией
            function updateCounter(newValue) {
                counterElement.style.transform = 'scale(1.2)';
                counterElement.style.color = '#4fc0ff';
                setTimeout(() => {
                    counterElement.style.transform = 'scale(1)';
                    counterElement.style.color = '#fff';
                }, 300);
                counterElement.textContent = newValue;
            }

            // Запрос текущего значения счетчика
            function fetchCounter() {
                fetch('/counter')
                    .then(response => response.json())
                    .then(data => updateCounter(data.counter))
                    .catch(err => console.error('Error:', err));
            }

            // Обновление счетчика каждую секунду
            setInterval(fetchCounter, 1000);

            // Обработчик клика на кнопке
            btn.addEventListener('click', () => {
                btn.disabled = true;
                fetch('/increment', { method: 'POST' })
                    .then(response => response.json())
                    .then(data => {
                        updateCounter(data.counter);
                        createParticles(event);
                        btn.disabled = false;
                    })
                    .catch(err => {
                        console.error('Error:', err);
                        btn.disabled = false;
                    });
            });

            // Создание частиц для анимации
            function createParticles(event) {
                const particles = document.createElement('div');
                particles.style.position = 'absolute';
                particles.style.left = event.clientX + 'px';
                particles.style.top = event.clientY + 'px';
                particles.style.width = '10px';
                particles.style.height = '10px';
                particles.style.borderRadius = '50%';
                particles.style.background = 'radial-gradient(circle, rgba(79,192,255,1) 0%, rgba(121,100,255,0.5) 100%)';
                particles.style.pointerEvents = 'none';
                document.body.appendChild(particles);

                particles.animate([
                    { transform: 'scale(1)', opacity: 1 },
                    { transform: 'scale(3)', opacity: 0 }
                ], {
                    duration: 1000,
                    easing: 'ease-out'
                });

                setTimeout(() => particles.remove(), 1000);
            }

            // Инициализация начального значения
            fetchCounter();
        </script>
    </body>
    </html>
    '''