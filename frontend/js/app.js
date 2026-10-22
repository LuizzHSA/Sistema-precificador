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

  showLogin(message = '', mode = 'login') {
    const screen = document.getElementById('authScreen');
    const application = document.getElementById('app');
    if (application) application.style.display = 'none';
    if (!screen) return;
    const registering = mode === 'register';
    screen.style.display = 'flex';
    screen.innerHTML = `
      <section class="card" style="width:min(420px,calc(100% - 32px));margin:auto">
        <div class="card-header"><h2>${registering ? 'Criar sua conta' : 'Entrar no Sistema Precificador'}</h2></div>
        <div class="card-body">
          <p>${registering ? 'Crie sua conta para começar a organizar seus preços.' : 'Informe suas credenciais para continuar.'}</p>
          <p id="authError" role="alert" style="color:#b42318"></p>
          <form id="loginForm">
            ${registering ? '<div class="form-group"><label for="loginName">Nome</label><input class="form-input" id="loginName" name="name" type="text" maxlength="120" autocomplete="name" required></div>' : ''}
            <div class="form-group"><label for="loginEmail">E-mail</label><input class="form-input" id="loginEmail" name="email" type="email" maxlength="255" autocomplete="username" required></div>
            <div class="form-group"><label for="loginPassword">Senha</label><input class="form-input" id="loginPassword" name="password" type="password" minlength="${registering ? '10' : '1'}" autocomplete="${registering ? 'new-password' : 'current-password'}" required></div>
            <button class="btn btn--primary" id="loginSubmit" type="submit" style="width:100%">${registering ? 'Criar conta' : 'Entrar'}</button>
          </form>
          <p style="margin-top:16px;text-align:center">
            <button id="authSwitch" type="button" class="btn">${registering ? 'Já tenho uma conta' : 'Criar uma conta'}</button>
          </p>
        </div>
      </section>`;
    document.getElementById('authError').textContent = message;
    document.getElementById('authSwitch').addEventListener('click', () => this.showLogin('', registering ? 'login' : 'register'));
    document.getElementById('loginForm').addEventListener('submit', async (event) => {
      event.preventDefault();
      if (this.authenticating) return;
      this.authenticating = true;
      const button = document.getElementById('loginSubmit');
      const error = document.getElementById('authError');
      button.disabled = true;
      button.textContent = registering ? 'Criando conta...' : 'Entrando...';
      error.textContent = '';
      try {
        const form = new FormData(event.currentTarget);
        const email = String(form.get('email') || '').trim();
        const password = String(form.get('password') || '');
        const user = registering
          ? await api.register(String(form.get('name') || '').trim(), email, password)
          : await api.login(email, password);
        this.showApplication(user);
        await this.navigate(this.getCurrentRoute());
      } catch (err) {
        error.textContent = err.message || (registering ? 'Não foi possível criar sua conta.' : 'Não foi possível entrar. Verifique suas credenciais.');
      } finally {
        this.authenticating = false;
        if (button.isConnected) {
          button.disabled = false;
          button.textContent = registering ? 'Criar conta' : 'Entrar';
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
