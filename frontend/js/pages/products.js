// Products page (placeholder)
const ProductsPage = {
  async render() {
    const content = document.getElementById('content');
    content.innerHTML = `
            <div class="card">
                <div class="card-header">
                    <h3>Produtos</h3>
                    <button class="btn btn--primary">➕ Novo</button>
                </div>
                <div class="card-body">
                    <p style="text-align: center; color: var(--text-muted);">
                        Página de produtos - Em desenvolvimento
                    </p>
                </div>
            </div>
        `;
  },
};
