// Stores page (placeholder)
const StoresPage = {
  async render() {
    const content = document.getElementById('content');
    content.innerHTML = `
            <div class="card">
                <div class="card-header">
                    <h3>Lojas</h3>
                    <button class="btn btn--primary">➕ Nova</button>
                </div>
                <div class="card-body">
                    <p style="text-align: center; color: var(--text-muted);">
                        Página de lojas - Em desenvolvimento
                    </p>
                </div>
            </div>
        `;
  },
};
