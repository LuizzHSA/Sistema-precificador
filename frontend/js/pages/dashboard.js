const DashboardPage = {
  async render() {
    const content = document.getElementById('content');
    content.innerHTML = '<div class="card"><div class="card-body">Carregando métricas...</div></div>';
    try {
      const data = await api.getDashboard();
      const cards = [['products', 'Produtos'], ['stores', 'Lojas'], ['pending', 'Pendentes'], ['active', 'Ativas'], ['executed', 'Executadas'], ['cancelled', 'Canceladas']];
      content.innerHTML = `<div class="grid grid--3">${cards.map(([key, label]) => `<div class="card"><div class="card-body"><div style="text-align:center;padding:20px"><h3 style="font-size:2.5rem;color:var(--primary)">${data[key] || 0}</h3><p>${label}</p></div></div></div>`).join('')}</div><div class="card margin-top"><div class="card-header"><h3>Alterações recentes</h3></div><div class="card-body">${data.recent.length ? `<div class="table-responsive"><table><thead><tr><th>Produto</th><th>Variação</th><th>Status</th></tr></thead><tbody>${data.recent.map(item => `<tr><td>${item.product || item.product_name || '-'}</td><td>${item.percentage_change > 0 ? '+' : ''}${item.percentage_change}%</td><td>${item.status}</td></tr>`).join('')}</tbody></table></div>` : '<p>Nenhuma alteração para exibir.</p>'}</div></div>`;
    } catch (error) { content.innerHTML = `<div class="card"><div class="card-body">${error.message}</div></div>`; }
  },
};
