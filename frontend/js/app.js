// Aplicação principal
const app = {
  currentPage: 'dashboard',
  loginModal: null,

  async init() {
    console.log('Inicializando aplicação...');
    this.loginModal = new Modal('loginModal');
    this.setupRouting();
    this.setupAuth();
    this.setupNavigation();
    const token = api.getToken();
    if (token) await this.checkAuth();
    else this.showLogin();
  },

  setupRouting() {
    window.addEventListener('hashchange', () => this.navigate(this.getCurrentRoute()));
  },

  setupAuth() {
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
      const form = new Form(loginForm);
      form.onSubmit(async (data) => {
        try {
          form.setLoading(true);
          const response = await api.login(data.email, data.password);
          api.setToken(response.token);
          store.setUser(response.user);
          this.loginModal.hide();
          this.navigate('dashboard');
          showToast('Login realizado com sucesso!', 'success');
        } catch (error) {
          showToast(error.message || 'Erro ao fazer login', 'error');
        } finally { form.setLoading(false); }
      });
    }
    const logoutBtn = document.getElementById('logoutBtn');
    if (logoutBtn) logoutBtn.addEventListener('click', (e) => {
      e.preventDefault(); api.removeToken(); store.logout(); this.showLogin(); showToast('Logout realizado', 'info');
    });
  },

  setupNavigation() {
    document.querySelectorAll('.nav-link').forEach((link) => link.addEventListener('click', (e) => {
      document.querySelectorAll('.nav-link').forEach((l) => l.classList.remove('active'));
      e.target.closest('.nav-link')?.classList.add('active');
    }));
    const menuToggle = document.getElementById('menuToggle');
    if (menuToggle) menuToggle.addEventListener('click', () => document.querySelector('.sidebar').classList.toggle('active'));
  },

  async checkAuth() {
    try {
      const user = await api.getMe();
      store.setUser(user);
      document.getElementById('userName').textContent = user.name || user.email;
      await this.navigate(this.getCurrentRoute());
    } catch (error) { api.removeToken(); this.showLogin(); }
  },

  showLogin() {
    if (this.loginModal) {
      this.loginModal.show();
      const content = document.getElementById('content');
      if (content) content.innerHTML = '';
    }
  },

  getCurrentRoute() {
    const hash = window.location.hash.slice(2) || 'dashboard';
    return hash.split('/')[0];
  },

  async navigate(page) {
    const pageName = page.toLowerCase();
    const pageMap = {
      dashboard: DashboardPage,
      'price-changes': PriceChangesPage,
      products: ProductsPage,
      stores: StoresPage,
      settings: SettingsPage,
    };
    const PageComponent = pageMap[pageName];
    if (!PageComponent) return;
    this.currentPage = pageName;
    const titles = { dashboard: 'Dashboard', 'price-changes': 'Alterações de Preço', products: 'Produtos', stores: 'Lojas', settings: 'Configurações' };
    document.getElementById('pageTitle').textContent = titles[pageName] || 'Página';
    if (PageComponent.render) await PageComponent.render();
  },
};

document.addEventListener('DOMContentLoaded', () => app.init());
