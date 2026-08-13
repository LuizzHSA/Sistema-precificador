// Aplicação principal
const app = {
  currentPage: 'dashboard',
  loginModal: null,

  async init() {
    console.log('🚀 Inicializando aplicação...');

    this.loginModal = new Modal('loginModal');

    // Setup event listeners
    this.setupRouting();
    this.setupAuth();
    this.setupNavigation();

    // Check if user is logged in
    const token = api.getToken();
    if (token) {
      await this.checkAuth();
    } else {
      this.showLogin();
    }
  },

  setupRouting() {
    window.addEventListener('hashchange', () => {
      const route = this.getCurrentRoute();
      this.navigate(route);
    });
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
        } finally {
          form.setLoading(false);
        }
      });
    }

    // Logout
    const logoutBtn = document.getElementById('logoutBtn');
    if (logoutBtn) {
      logoutBtn.addEventListener('click', (e) => {
        e.preventDefault();
        api.removeToken();
        store.logout();
        this.showLogin();
        showToast('Logout realizado', 'info');
      });
    }
  },

  setupNavigation() {
    document.querySelectorAll('.nav-link').forEach((link) => {
      link.addEventListener('click', (e) => {
        // Remover active de todos
        document.querySelectorAll('.nav-link').forEach((l) => {
          l.classList.remove('active');
        });
        // Adicionar active ao clicado
        e.target.closest('.nav-link').classList.add('active');
      });
    });

    // Menu toggle mobile
    const menuToggle = document.getElementById('menuToggle');
    if (menuToggle) {
      menuToggle.addEventListener('click', () => {
        document.querySelector('.sidebar').classList.toggle('active');
      });
    }
  },

  async checkAuth() {
    try {
      const user = await api.getMe();
      store.setUser(user);
      document.getElementById('userName').textContent = user.name || user.email;
      this.navigate(this.getCurrentRoute());
    } catch (error) {
      api.removeToken();
      this.showLogin();
    }
  },

  showLogin() {
    if (this.loginModal) {
      this.loginModal.show();
      const content = document.getElementById('content');
      if (content) {
        content.innerHTML = '';
      }
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
    };

    const PageComponent = pageMap[pageName];

    if (PageComponent) {
      this.currentPage = pageName;

      // Update page title
      const titles = {
        dashboard: 'Dashboard',
        'price-changes': 'Alterações de Preço',
        products: 'Produtos',
        stores: 'Lojas',
      };
      document.getElementById('pageTitle').textContent = titles[pageName] || 'Página';

      // Render page
      if (PageComponent.render) {
        await PageComponent.render();
      }
    }
  },
};

// Iniciar quando DOM estiver pronto
document.addEventListener('DOMContentLoaded', () => {
  app.init();
});
