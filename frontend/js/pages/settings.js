const SettingsPage = {
  async render() {
    const content = document.getElementById('content');
    const isLocal = ['localhost', '127.0.0.1'].includes(window.location.hostname);
    const currentApi = isLocal
      ? (localStorage.getItem('apiBaseURL') || 'http://localhost:5000/api')
      : '/api';

    content.innerHTML = `
      <div class="card">
        <div class="card-header"><h3>Configurações</h3></div>
        <div class="card-body">
          <div class="form-group">
            <label for="apiBaseUrl">URL da API</label>
            <input
              id="apiBaseUrl"
              class="form-input"
              value="${currentApi}"
              ${isLocal ? '' : 'disabled'}
            >
          </div>

          ${isLocal ? `
            <div class="form-group">
              <button id="saveSettings" class="btn btn--primary">Salvar configurações</button>
              <button id="resetSettings" class="btn">Restaurar padrão</button>
            </div>
          ` : '<p>A API de produção usa automaticamente <strong>/api</strong> no mesmo domínio.</p>'}

          <hr>
          <h4>Status do sistema</h4>
          <p id="apiStatus">Verificando API...</p>

          <h4>Ambiente</h4>
          <p>Frontend: ${isLocal ? 'local' : 'Vercel / produção'}</p>
          <p>API: ${currentApi}</p>
        </div>
      </div>
    `;

    if (isLocal) {
      document.getElementById('saveSettings').onclick = async () => {
        const value = document.getElementById('apiBaseUrl').value.trim().replace(/\/$/, '');
        if (!value) return showToast('Informe a URL da API', 'error');

        api.setBaseURL(value);
        showToast('Configurações salvas', 'success');
        await this.checkApi(value);
      };

      document.getElementById('resetSettings').onclick = async () => {
        const value = 'http://localhost:5000/api';
        api.setBaseURL(value);
        document.getElementById('apiBaseUrl').value = value;
        showToast('Configurações restauradas', 'success');
        await this.checkApi(value);
      };
    }

    await this.checkApi(currentApi);
  },

  async checkApi(baseUrl) {
    const status = document.getElementById('apiStatus');
    if (!status) return;

    try {
      const healthUrl = baseUrl === '/api' ? '/health' : `${baseUrl.replace(/\/$/, '')}/../health`;
      const response = await fetch(healthUrl);

      if (!response.ok) throw new Error('HTTP ' + response.status);

      status.textContent = 'API online e respondendo normalmente.';
    } catch (error) {
      status.textContent = 'API indisponível. Verifique a conexão com o backend.';
    }
  },
};
