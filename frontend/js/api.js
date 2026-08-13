// Cliente HTTP para comunicação com API
class APIClient {
  constructor(baseURL = '/api') {
    this.baseURL = baseURL;
    this.token = localStorage.getItem('token');
  }

  setToken(token) {
    this.token = token;
    localStorage.setItem('token', token);
  }

  getToken() {
    return this.token;
  }

  removeToken() {
    this.token = null;
    localStorage.removeItem('token');
  }

  async request(method, endpoint, data = null, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    const headers = {
      'Content-Type': 'application/json',
      ...options.headers,
    };

    if (this.token) {
      headers['Authorization'] = `Bearer ${this.token}`;
    }

    const config = {
      method,
      headers,
      ...options,
    };

    if (data) {
      config.body = JSON.stringify(data);
    }

    try {
      const response = await fetch(url, config);
      const json = await response.json();

      if (!response.ok) {
        throw {
          status: response.status,
          message: json.error || 'Erro na requisição',
          data: json,
        };
      }

      return json;
    } catch (error) {
      if (error.status === 401) {
        // Token expirado ou inválido
        this.removeToken();
        window.location.hash = '#/login';
      }
      throw error;
    }
  }

  // Métodos de conveniência
  get(endpoint, options) {
    return this.request('GET', endpoint, null, options);
  }

  post(endpoint, data, options) {
    return this.request('POST', endpoint, data, options);
  }

  put(endpoint, data, options) {
    return this.request('PUT', endpoint, data, options);
  }

  delete(endpoint, options) {
    return this.request('DELETE', endpoint, null, options);
  }

  // Métodos da API
  async login(email, password) {
    return this.post('/auth/login', { email, password });
  }

  async getMe() {
    return this.get('/auth/me');
  }

  async logout() {
    return this.post('/auth/logout', {});
  }

  async getPriceChanges(filters = {}) {
    const params = new URLSearchParams(filters);
    return this.get(`/price-changes?${params}`);
  }

  async getPriceChange(id) {
    return this.get(`/price-changes/${id}`);
  }

  async createPriceChange(data) {
    return this.post('/price-changes', data);
  }

  async updatePriceChange(id, data) {
    return this.put(`/price-changes/${id}`, data);
  }

  async executePriceChange(id) {
    return this.post(`/price-changes/${id}/execute`, {});
  }

  async deletePriceChange(id) {
    return this.delete(`/price-changes/${id}`);
  }
}

// Instância global
const api = new APIClient();
