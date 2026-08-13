const DashboardPage = {
  async render() {
    const content = document.getElementById('content');
    content.innerHTML = '<div class="card"><div class="card-body">Carregando métricas...</div></div>';
    try {
      const data = await api.getDashboard();
      const cards = [['products', 'Produtos'], ['stores', 'Lojas'], ['pending', 'Pendentes'], ['active', 'Ativas'], ['executed', 'Executadas'], ['cancelled', 'Canceladas']];
      const rows = items => items.length ? items.map(item => `<tr><td>${item.product || item.product_name || '-'}</td><td>${item.percentage_change > 0 ? '+' : ''}${item.percentage_change}%</td><td>R$ ${Number(item.price_difference).toFixed(2)}</td><td>${item.status}</td></tr>`).join('') : '<tr><td colspan="4">Nenhuma alteração.</td></tr>';
      const table = (title, items) => `<div class="card margin-top"><div class="card-header"><h3>${title}</h3></div><div class="card-body"><div class="table-responsive"><table><thead><tr><th>Produto</th><th>Variação</th><th>Diferença</th><th>Status</th></tr></thead><tbody>${rows(items || [])}</tbody></table></div></div></div>`;
      content.innerHTML = `<div class="grid grid--3">${cards.map(([key, label]) => `<div class="card"><div class="card-body"><div style="text-align:center;padding:20px"><h3 style="font-size:2.5rem;color:var(--primary)">${data[key] || 0}</h3><p>${label}</p></div></div></div>`).join('')}</div><div class="card margin-top"><div class="card-body"><strong>${data.today_changes || 0}</strong> alterações registradas hoje.</div></div>${table('Alterações recentes', data.recent)}${table('Maiores aumentos', data.largest_increases)}${table('Maiores reduções', data.largest_reductions)}`;
    } catch (error) { content.innerHTML = `<div class="card"><div class="card-body">${error.message}</div></div>`; }
  },
};
