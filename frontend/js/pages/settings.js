const SettingsPage = {
  async render() {
    const content = document.getElementById('content');
    const currentApi = localStorage.getItem('apiBaseURL') || window.API_BASE_URL || 'http://localhost:5000/api';
    content.innerHTML = `<div class="card"><div class="card-header"><h3>Configurações</h3></div><div class="card-body">
      <div class="form-group"><label for="apiBaseUrl">URL da API</label><input id="apiBaseUrl" class="form-input" value="${currentApi}" placeholder="http://localhost:5000/api"></div>
      <div class="form-group"><button id="saveSettings" class="btn btn--primary">Salvar configurações</button> <button id="resetSettings" class="btn">Restaurar padrão</button></div>
      <hr><h4>Status do sistema</h4><p id="apiStatus">Verificando API...</p>
      <h4>Ambiente</h4><p>Frontend: servidor HTTP local</p><p>API padrão: http://localhost:5000/api</p>
    </div></div>`;
    document.getElementById('saveSettings').onclick = async () => {
      const value = document.getElementById('apiBaseUrl').value.trim().replace(/\/$/, '');
      if (!value) return showToast('Informe a URL da API', 'error');
      api.setBaseURL(value);
      showToast('Configurações salvas', 'success');
      await this.checkApi(value);
    };
    document.getElementById('resetSettings').onclick = async () => {
      api.setBaseURL('http://localhost:5000/api');
      document.getElementById('apiBaseUrl').value = 'http://localhost:5000/api';
      showToast('Configurações restauradas', 'success');
      await this.checkApi('http://localhost:5000/api');
    };
    await this.checkApi(currentApi);
  },
  async checkApi(baseUrl) {
    const status = document.getElementById('apiStatus');
    if (!status) return;
    try {
      const response = await fetch(`${baseUrl.replace(/\/$/, '')}/../health`);
      if (!response.ok) throw new Error('HTTP ' + response.status);
      status.textContent = 'API online e respondendo normalmente.';
    } catch (error) { status.textContent = 'API indisponível. Verifique se o backend está executando.'; }
  },
};
