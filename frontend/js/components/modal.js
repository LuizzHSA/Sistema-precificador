// Utilidades para modais
class Modal {
  constructor(elementId) {
    this.element = document.getElementById(elementId);
  }

  show() {
    this.element.classList.add('modal--active');
  }

  hide() {
    this.element.classList.remove('modal--active');
  }

  toggle() {
    this.element.classList.toggle('modal--active');
  }

  isVisible() {
    return this.element.classList.contains('modal--active');
  }

  onClose(callback) {
    const overlay = this.element.querySelector('.modal-overlay');
    if (overlay) {
      overlay.addEventListener('click', () => {
        callback();
        this.hide();
      });
    }
  }
}

// Toast notifications
function showToast(message, type = 'info', duration = 3000) {
  const container = document.getElementById('toastContainer');
  const toast = document.createElement('div');
  toast.className = `toast toast--${type}`;
  toast.textContent = message;

  container.appendChild(toast);

  if (duration > 0) {
    setTimeout(() => {
      toast.remove();
    }, duration);
  }

  return toast;
}
