import tkinter as tk
import threading
from flask import Flask, render_template_string
import webbrowser

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Auto Clicker</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            min-height: 100vh;
            background-color: #171717;
            color: #ffffff;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        main { display: flex; flex-direction: column; align-items: center; gap: 2rem; }
        h1 { font-size: 2.25rem; font-weight: bold; }
        .counter { font-size: 4rem; font-family: 'Courier New', monospace; font-variant-numeric: tabular-nums; }
        .controls { display: flex; align-items: center; gap: 1rem; }
        .controls label { font-size: 0.875rem; color: #a3a3a3; }
        .controls input {
            width: 6rem;
            background-color: #262626;
            border: 1px solid #404040;
            border-radius: 0.25rem;
            padding: 0.5rem 0.75rem;
            text-align: center;
            color: #ffffff;
            font-size: 1rem;
        }
        .controls input:disabled { opacity: 0.5; }
        .btn {
            padding: 1rem 2rem;
            border: none;
            border-radius: 0.5rem;
            font-weight: 600;
            font-size: 1.125rem;
            cursor: pointer;
            transition: background-color 0.2s;
        }
        .btn.start { background-color: #16a34a; }
        .btn.start:hover { background-color: #15803d; }
        .btn.stop { background-color: #dc2626; }
        .btn.stop:hover { background-color: #b91c1c; }
        .btn.reset {
            background-color: #404040;
            padding: 0.5rem 1rem;
            font-size: 0.875rem;
        }
        .btn.reset:hover:not(:disabled) { background-color: #525252; }
        .btn:disabled { opacity: 0.5; cursor: not-allowed; }
        .hint { font-size: 0.875rem; color: #737373; }
    </style>
</head>
<body>
    <main>
        <h1>Auto Clicker</h1>
        <div id="clickCount" class="counter">0</div>
        <div class="controls">
            <label for="interval">Interval (ms):</label>
            <input type="number" id="interval" min="10" max="10000" value="100">
        </div>
        <button id="toggleBtn" class="btn start">Start</button>
        <button id="resetBtn" class="btn reset" disabled>Reset</button>
        <p class="hint">Press Space to toggle</p>
    </main>
    <script>
        class AutoClicker {
            constructor() {
                this.clicking = false;
                this.clickCount = 0;
                this.interval = 100;
                this.timerId = null;
                this.clickCountEl = document.getElementById('clickCount');
                this.intervalEl = document.getElementById('interval');
                this.toggleBtn = document.getElementById('toggleBtn');
                this.resetBtn = document.getElementById('resetBtn');
                this.toggleBtn.addEventListener('click', () => this.toggle());
                this.resetBtn.addEventListener('click', () => this.reset());
                document.addEventListener('keydown', (e) => {
                    if (e.code === 'Space' && e.target === document.body) {
                        e.preventDefault();
                        this.toggle();
                    }
                });
                this.intervalEl.addEventListener('change', () => {
                    this.interval = Math.max(10, parseInt(this.intervalEl.value) || 100);
                    if (this.clicking) { this.stop(); this.start(); }
                });
            }
            toggle() { if (this.clicking) this.stop(); else this.start(); }
            start() {
                this.clicking = true;
                this.intervalEl.disabled = true;
                this.toggleBtn.textContent = 'Stop';
                this.toggleBtn.classList.remove('start');
                this.toggleBtn.classList.add('stop');
                this.resetBtn.disabled = true;
                this.timerId = setInterval(() => {
                    this.clickCount++;
                    this.clickCountEl.textContent = this.clickCount;
                }, this.interval);
            }
            stop() {
                this.clicking = false;
                if (this.timerId) { clearInterval(this.timerId); this.timerId = null; }
                this.intervalEl.disabled = false;
                this.toggleBtn.textContent = 'Start';
                this.toggleBtn.classList.remove('stop');
                this.toggleBtn.classList.add('start');
                this.resetBtn.disabled = this.clicking || this.clickCount === 0;
            }
            reset() {
                this.clickCount = 0;
                this.clickCountEl.textContent = '0';
                this.resetBtn.disabled = true;
            }
        }
        document.addEventListener('DOMContentLoaded', () => new AutoClicker());
    </script>
</body>
</html>
"""

app = Flask(__name__)

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

def run_flask():
    app.run(port=5000, debug=False, use_reloader=False)

if __name__ == '__main__':
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    webbrowser.open('http://localhost:5000')
    
    root = tk.Tk()
    root.title("Auto Clicker")
    root.geometry("300x100")
    root.resizable(False, False)
    
    label = tk.Label(root, text="Auto Clicker running in browser", font=("Arial", 12))
    label.pack(expand=True)
    
    quit_btn = tk.Button(root, text="Quit", command=root.destroy)
    quit_btn.pack(pady=10)
    
    root.mainloop()
