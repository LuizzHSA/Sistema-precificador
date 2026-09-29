// Aplicação principal - acesso direto temporário, sem autenticação
const app = {
  currentPage: 'dashboard',

  async init() {
    console.log('Inicializando aplicação...');
    this.setupRouting();
    this.setupNavigation();

    // Acesso direto temporário enquanto a autenticação está desativada.
    store.setUser({ name: 'Administrador', email: 'local' });
    const userName = document.getElementById('userName');
    if (userName) userName.textContent = 'Administrador';

    await this.navigate(this.getCurrentRoute());
  },

  setupRouting() {
    window.addEventListener('hashchange', () => this.navigate(this.getCurrentRoute()));
  },

  setupNavigation() {
    document.querySelectorAll('.nav-link').forEach((link) => link.addEventListener('click', (e) => {
      document.querySelectorAll('.nav-link').forEach((l) => l.classList.remove('active'));
      e.target.closest('.nav-link')?.classList.add('active');
    }));

    const menuToggle = document.getElementById('menuToggle');
    if (menuToggle) {
      menuToggle.addEventListener('click', () => document.querySelector('.sidebar').classList.toggle('active'));
    }

    const logoutBtn = document.getElementById('logoutBtn');
    if (logoutBtn) {
      logoutBtn.style.display = 'none';
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
