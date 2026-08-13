// Utilidades para formulários
class Form {
  constructor(formElement) {
    this.form = formElement;
    this.fields = {};
  }

  static getFormData(formElement) {
    const formData = new FormData(formElement);
    const data = {};
    formData.forEach((value, key) => {
      data[key] = value;
    });
    return data;
  }

  validate() {
    return this.form.checkValidity();
  }

  getData() {
    return Form.getFormData(this.form);
  }

  setData(data) {
    Object.keys(data).forEach((key) => {
      const input = this.form.querySelector(`[name="${key}"]`);
      if (input) {
        input.value = data[key];
      }
    });
  }

  reset() {
    this.form.reset();
  }

  setLoading(loading) {
    const submitButton = this.form.querySelector('button[type="submit"]');
    if (submitButton) {
      submitButton.disabled = loading;
      if (loading) {
        submitButton.innerHTML = '<span class="spinner"></span> Carregando...';
      } else {
        submitButton.innerHTML = 'Enviar';
      }
    }
  }

  onSubmit(callback) {
    this.form.addEventListener('submit', (e) => {
      e.preventDefault();
      if (this.validate()) {
        callback(this.getData());
      }
    });
  }

  showError(fieldName, message) {
    const field = this.form.querySelector(`[name="${fieldName}"]`);
    if (field) {
      field.classList.add('error');
      const errorEl = document.createElement('span');
      errorEl.className = 'form-error';
      errorEl.textContent = message;
      field.parentElement.appendChild(errorEl);
    }
  }

  clearErrors() {
    this.form.querySelectorAll('.form-error').forEach((el) => el.remove());
    this.form.querySelectorAll('.error').forEach((el) => el.classList.remove('error'));
  }
}
