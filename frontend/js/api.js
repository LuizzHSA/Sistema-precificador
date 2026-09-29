class APIClient {
  constructor() {
    const isLocal = ['localhost', '127.0.0.1'].includes(window.location.hostname);
    const defaultURL = isLocal ? 'http://localhost:5000/api' : '/api';

    // Em produção, sempre usa a API no mesmo domínio da Vercel.
    // Evita URLs antigas de localhost salvas no navegador.
    if (!isLocal) {
      localStorage.removeItem('apiBaseURL');
    }

    this.baseURL = window.API_BASE_URL || (isLocal ? localStorage.getItem('apiBaseURL') : null) || defaultURL;
  }

  setBaseURL(url) {
    const isLocal = ['localhost', '127.0.0.1'].includes(window.location.hostname);
    this.baseURL = isLocal ? url.replace(/\/$/, '') : '/api';

    if (isLocal) {
      window.API_BASE_URL = this.baseURL;
      localStorage.setItem('apiBaseURL', this.baseURL);
    } else {
      localStorage.removeItem('apiBaseURL');
    }
  }

  async request(method, endpoint, data = null) {
    const headers = { Accept: 'application/json' };
    if (data !== null) headers['Content-Type'] = 'application/json';

    const response = await fetch(`${this.baseURL}${endpoint}`, {
      method,
      headers,
      body: data === null ? undefined : JSON.stringify(data),
    });

    const text = await response.text();
    let json = {};

    try {
      json = text ? JSON.parse(text) : {};
    } catch {
      json = { error: text || 'Resposta inválida da API' };
    }

    if (!response.ok) {
      throw {
        status: response.status,
        message: json.error || 'Erro na requisição',
        data: json,
      };
    }

    return json;
  }

  get(endpoint) { return this.request('GET', endpoint); }
  post(endpoint, data = {}) { return this.request('POST', endpoint, data); }
  put(endpoint, data = {}) { return this.request('PUT', endpoint, data); }
  delete(endpoint) { return this.request('DELETE', endpoint); }

  getDashboard() { return this.get('/dashboard'); }
  getStores(search = '') { return this.get(`/stores${search ? `?search=${encodeURIComponent(search)}` : ''}`); }
  createStore(data) { return this.post('/stores', data); }
  updateStore(id, data) { return this.put(`/stores/${id}`, data); }
  deleteStore(id) { return this.delete(`/stores/${id}`); }
  getProducts(filters = {}) {
    const query = new URLSearchParams(filters);
    return this.get(`/products${query.toString() ? `?${query}` : ''}`);
  }
  createProduct(data) { return this.post('/products', data); }
  updateProduct(id, data) { return this.put(`/products/${id}`, data); }
  deleteProduct(id) { return this.delete(`/products/${id}`); }
  getProductHistory(id, filters = {}) {
    const query = new URLSearchParams(filters);
    return this.get(`/products/${id}/history${query.toString() ? `?${query}` : ''}`);
  }
  getPriceChanges(filters = {}) {
    const query = new URLSearchParams(filters);
    return this.get(`/price-changes${query.toString() ? `?${query}` : ''}`);
  }
  getPriceChange(id) { return this.get(`/price-changes/${id}`); }
  createPriceChange(data) { return this.post('/price-changes', data); }
  updatePriceChange(id, data) { return this.put(`/price-changes/${id}`, data); }
  activatePriceChange(id) { return this.post(`/price-changes/${id}/activate`); }
  executePriceChange(id) { return this.post(`/price-changes/${id}/execute`); }
  deletePriceChange(id) { return this.delete(`/price-changes/${id}`); }
}

const api = new APIClient();
