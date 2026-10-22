// Aplicação principal com sessão autenticada.
const app = {
  currentPage: 'dashboard',
  authenticating: false,

  async init() {
    this.setupRouting();
    this.setupNavigation();
    const token = api.getToken();
    if (!token) {
      this.showLogin();
      return;
    }
    try {
      const user = await api.currentUser();
      this.showApplication(user);
      await this.navigate(this.getCurrentRoute());
    } catch {
      api.setToken(null);
      this.showLogin();
    }
  },

  setupRouting() {
    window.addEventListener('hashchange', () => {
      if (store.getState().user) this.navigate(this.getCurrentRoute());
    });
  },

  setupNavigation() {
    document.querySelectorAll('.nav-link').forEach((link) => link.addEventListener('click', (e) => {
      document.querySelectorAll('.nav-link').forEach((l) => l.classList.remove('active'));
      e.target.closest('.nav-link')?.classList.add('active');
    }));
    const menuToggle = document.getElementById('menuToggle');
    if (menuToggle) menuToggle.addEventListener('click', () => document.querySelector('.sidebar').classList.toggle('active'));
    const logoutBtn = document.getElementById('logoutBtn');
    if (logoutBtn) logoutBtn.addEventListener('click', async (event) => {
      event.preventDefault();
      await this.logout();
    });
  },

  showLogin(message = '') {
    const screen = document.getElementById('authScreen');
    const application = document.getElementById('app');
    if (application) application.style.display = 'none';
    if (!screen) return;
    screen.style.display = 'flex';
    screen.innerHTML = `
      <section class="card" style="width:min(420px,calc(100% - 32px));margin:auto">
        <div class="card-header"><h2>Entrar no Sistema Precificador</h2></div>
        <div class="card-body">
          <p>Informe suas credenciais para continuar.</p>
          <p id="authError" role="alert" style="color:#b42318">${message}</p>
          <form id="loginForm">
            <div class="form-group"><label for="loginEmail">E-mail</label><input class="form-input" id="loginEmail" name="email" type="email" autocomplete="username" required></div>
            <div class="form-group"><label for="loginPassword">Senha</label><input class="form-input" id="loginPassword" name="password" type="password" autocomplete="current-password" required></div>
            <button class="btn btn--primary" id="loginSubmit" type="submit" style="width:100%">Entrar</button>
          </form>
        </div>
      </section>`;
    document.getElementById('loginForm').addEventListener('submit', async (event) => {
      event.preventDefault();
      if (this.authenticating) return;
      this.authenticating = true;
      const button = document.getElementById('loginSubmit');
      const error = document.getElementById('authError');
      button.disabled = true;
      button.textContent = 'Entrando...';
      error.textContent = '';
      try {
        const form = new FormData(event.currentTarget);
        const user = await api.login(String(form.get('email') || '').trim(), String(form.get('password') || ''));
        this.showApplication(user);
        await this.navigate(this.getCurrentRoute());
      } catch (err) {
        error.textContent = err.message || 'Não foi possível entrar. Verifique suas credenciais.';
      } finally {
        this.authenticating = false;
        if (button.isConnected) {
          button.disabled = false;
          button.textContent = 'Entrar';
        }
      }
    });
  },

  showApplication(user) {
    const screen = document.getElementById('authScreen');
    const application = document.getElementById('app');
    if (screen) screen.style.display = 'none';
    if (application) application.style.display = '';
    store.setUser(user);
    const userName = document.getElementById('userName');
    if (userName) userName.textContent = user.name || user.email || 'Usuário';
    const logoutBtn = document.getElementById('logoutBtn');
    if (logoutBtn) logoutBtn.style.display = '';
  },

  async logout() {
    await api.logout();
    store.logout();
    window.location.hash = '#/dashboard';
    this.showLogin('Você saiu da sua conta.');
  },

  handleUnauthorized() {
    if (!store.getState().user) return;
    store.logout();
    this.showLogin('Sua sessão expirou. Entre novamente.');
  },

  getCurrentRoute() {
    const hash = window.location.hash.slice(2) || 'dashboard';
    return hash.split('/')[0];
  },

  async navigate(page) {
    if (!store.getState().user) return;
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
    const titles = {
      dashboard: 'Dashboard',
      'price-changes': 'Alterações de Preço',
      products: 'Produtos',
      stores: 'Lojas',
      settings: 'Configurações',
    };
    const pageTitle = document.getElementById('pageTitle');
    if (pageTitle) pageTitle.textContent = titles[pageName] || 'Página';
    if (PageComponent.render) await PageComponent.render();
  },
};

document.addEventListener('DOMContentLoaded', () => app.init());
