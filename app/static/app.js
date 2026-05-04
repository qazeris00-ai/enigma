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
            if (this.clicking) {
                this.stop();
                this.start();
            }
        });
    }

    toggle() {
        if (this.clicking) {
            this.stop();
        } else {
            this.start();
        }
    }

    start() {
        this.clicking = true;
        this.intervalEl.disabled = true;
        this.toggleBtn.textContent = 'Stop';
        this.toggleBtn.classList.remove('start');
        this.toggleBtn.classList.add('stop');
        this.resetBtn.disabled = true;
        this.updateResetButton();
        
        this.timerId = setInterval(() => {
            this.clickCount++;
            this.clickCountEl.textContent = this.clickCount;
        }, this.interval);
    }

    stop() {
        this.clicking = false;
        if (this.timerId) {
            clearInterval(this.timerId);
            this.timerId = null;
        }
        this.intervalEl.disabled = false;
        this.toggleBtn.textContent = 'Start';
        this.toggleBtn.classList.remove('stop');
        this.toggleBtn.classList.add('start');
        this.updateResetButton();
    }

    reset() {
        this.clickCount = 0;
        this.clickCountEl.textContent = '0';
        this.updateResetButton();
    }

    updateResetButton() {
        this.resetBtn.disabled = this.clicking || this.clickCount === 0;
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new AutoClicker();
});
