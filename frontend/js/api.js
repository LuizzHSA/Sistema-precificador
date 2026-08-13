class APIClient {
  constructor() {
    const developmentURL = window.location.hostname === 'localhost' && window.location.port === '8080' ? 'http://localhost:5000/api' : '/api';
    this.baseURL = window.API_BASE_URL || localStorage.getItem('apiBaseURL') || developmentURL;
    this.token = localStorage.getItem('token');
  }
  setToken(token) { this.token = token; localStorage.setItem('token', token); }
  getToken() { return this.token; }
  removeToken() { this.token = null; localStorage.removeItem('token'); }
  async request(method, endpoint, data = null) {
    const headers = { Accept: 'application/json' };
    if (data !== null) headers['Content-Type'] = 'application/json';
    if (this.token) headers.Authorization = `Bearer ${this.token}`;
    const response = await fetch(`${this.baseURL}${endpoint}`, { method, headers, body: data === null ? undefined : JSON.stringify(data) });
    const text = await response.text();
    const json = text ? JSON.parse(text) : {};
    if (!response.ok) {
      if (response.status === 401) { this.removeToken(); window.location.hash = '#/login'; }
      throw { status: response.status, message: json.error || 'Erro na requisição', data: json };
    }
    return json;
  }
  get(endpoint) { return this.request('GET', endpoint); }
  post(endpoint, data = {}) { return this.request('POST', endpoint, data); }
  put(endpoint, data = {}) { return this.request('PUT', endpoint, data); }
  delete(endpoint) { return this.request('DELETE', endpoint); }
  login(email, password) { return this.post('/auth/login', { email, password }); }
  getMe() { return this.get('/auth/me'); }
  logout() { return this.post('/auth/logout'); }
  getDashboard() { return this.get('/dashboard'); }
  getStores(search = '') { return this.get(`/stores${search ? `?search=${encodeURIComponent(search)}` : ''}`); }
  createStore(data) { return this.post('/stores', data); }
  updateStore(id, data) { return this.put(`/stores/${id}`, data); }
  deleteStore(id) { return this.delete(`/stores/${id}`); }
  getProducts(filters = {}) { const query = new URLSearchParams(filters); return this.get(`/products${query.toString() ? `?${query}` : ''}`); }
  createProduct(data) { return this.post('/products', data); }
  updateProduct(id, data) { return this.put(`/products/${id}`, data); }
  deleteProduct(id) { return this.delete(`/products/${id}`); }
  getPriceChanges(filters = {}) { const query = new URLSearchParams(filters); return this.get(`/price-changes${query.toString() ? `?${query}` : ''}`); }
  getPriceChange(id) { return this.get(`/price-changes/${id}`); }
  createPriceChange(data) { return this.post('/price-changes', data); }
  updatePriceChange(id, data) { return this.put(`/price-changes/${id}`, data); }
  activatePriceChange(id) { return this.post(`/price-changes/${id}/activate`); }
  executePriceChange(id) { return this.post(`/price-changes/${id}/execute`); }
  deletePriceChange(id) { return this.delete(`/price-changes/${id}`); }
}
const api = new APIClient();
