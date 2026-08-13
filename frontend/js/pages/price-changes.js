// Price Changes page
const PriceChangesPage = {
  async render() {
    const content = document.getElementById('content');
    content.innerHTML = `
            <div class="flex flex--between margin-bottom">
                <h2>Alterações de Preço</h2>
                <button class="btn btn--primary" id="newPriceChangeBtn">
                    ➕ Nova Alteração
                </button>
            </div>
            
            <div class="card">
                <div id="tableContainer" style="overflow-x: auto;">
                    <p style="text-align: center; padding: 30px; color: var(--text-muted);">
                        Carregando alterações...
                    </p>
                </div>
            </div>
        `;

    // Load data
    try {
      const data = await api.getPriceChanges({ per_page: 20 });
      this.renderTable(data.items || []);
    } catch (error) {
      showToast('Erro ao carregar alterações', 'error');
      console.error(error);
    }

    // Event listeners
    document.getElementById('newPriceChangeBtn').addEventListener('click', () => {
      this.showCreateModal();
    });
  },

  renderTable(items) {
    const container = document.getElementById('tableContainer');

    if (items.length === 0) {
      container.innerHTML = `
                <p style="text-align: center; padding: 30px; color: var(--text-muted);">
                    Nenhuma alteração de preço registrada
                </p>
            `;
      return;
    }

    let html = `
            <table class="table">
                <thead>
                    <tr>
                        <th>Produto</th>
                        <th>Preço Atual</th>
                        <th>Novo Preço</th>
                        <th>Variação</th>
                        <th>Data Efetiva</th>
                        <th>Status</th>
                        <th>Ações</th>
                    </tr>
                </thead>
                <tbody>
        `;

    items.forEach((item) => {
      const variation = item.percentage_change || 0;
      const variationClass = variation < 0 ? 'text-success' : 'text-danger';
      const statusBadge = this.getStatusBadge(item.status);

      html += `
                <tr>
                    <td>${item.product_name || 'N/A'}</td>
                    <td>R$ ${parseFloat(item.current_price).toFixed(2)}</td>
                    <td>R$ ${parseFloat(item.new_price).toFixed(2)}</td>
                    <td class="${variationClass}">
                        ${variation > 0 ? '+' : ''}${variation.toFixed(2)}%
                    </td>
                    <td>${new Date(item.effective_date).toLocaleDateString('pt-BR')}</td>
                    <td>${statusBadge}</td>
                    <td>
                        <button class="btn btn--small btn--secondary view-btn" data-id="${item.id}">
                            👁️ Ver
                        </button>
                    </td>
                </tr>
            `;
    });

    html += `
                </tbody>
            </table>
        `;

    container.innerHTML = html;

    // Add event listeners
    container.querySelectorAll('.view-btn').forEach((btn) => {
      btn.addEventListener('click', (e) => {
        this.showDetails(e.target.closest('button').dataset.id);
      });
    });
  },

  getStatusBadge(status) {
    const statusMap = {
      pending: '<span class="badge badge--pending">Pendente</span>',
      active: '<span class="badge badge--info">Ativa</span>',
      executed: '<span class="badge badge--success">Executada</span>',
      cancelled: '<span class="badge badge--danger">Cancelada</span>',
    };
    return statusMap[status] || `<span class="badge">${status}</span>`;
  },

  showCreateModal() {
    showToast('Modal de criação será implementado', 'info');
  },

  showDetails(id) {
    showToast(`Detalhes do item #${id}`, 'info');
  },
};
