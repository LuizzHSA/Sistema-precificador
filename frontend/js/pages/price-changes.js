const PriceChangesPage = {
  async render() {
    const content = document.getElementById('content');
    content.innerHTML = `<div class="card"><div class="card-header"><h3>Alterações de preço</h3><button id="newChange" class="btn btn--primary">Nova alteração</button></div><div class="card-body"><div class="flex"><select id="statusFilter"><option value="">Todos os status</option><option value="pending">Pendente</option><option value="active">Ativa</option><option value="executed">Executada</option><option value="cancelled">Cancelada</option></select><input id="changeSearch" placeholder="Buscar produto, SKU ou motivo"></div><div id="changeForm"></div><div id="changeTable">Carregando...</div></div></div>`;
    const load = async () => { try { const response = await api.getPriceChanges({ status: document.getElementById('statusFilter').value, search: document.getElementById('changeSearch').value, per_page: 100 }); this.draw(response.data || response.items || []); } catch (error) { document.getElementById('changeTable').textContent = error.message; } };
    document.getElementById('statusFilter').onchange = load;
    document.getElementById('changeSearch').oninput = load;
    document.getElementById('newChange').onclick = () => this.form();
    this.load = load;
    await load();
  },
  draw(items) {
    document.getElementById('changeTable').innerHTML = items.length ? `<table><thead><tr><th>Produto</th><th>Atual</th><th>Novo</th><th>Variação</th><th>Data</th><th>Status</th><th>Ações</th></tr></thead><tbody>${items.map(i => `<tr><td>${i.product || i.product_name || '-'}</td><td>R$ ${Number(i.current_price).toFixed(2)}</td><td>R$ ${Number(i.new_price).toFixed(2)}</td><td>${i.percentage_change > 0 ? '+' : ''}${i.percentage_change}%</td><td>${new Date(i.effective_date).toLocaleDateString('pt-BR')}</td><td>${i.status}</td><td>${i.status === 'pending' ? `<button class="btn btn--small activate" data-id="${i.id}">Ativar</button>` : ''}${i.status === 'active' ? `<button class="btn btn--small execute" data-id="${i.id}">Executar</button>` : ''}${['pending','active'].includes(i.status) ? `<button class="btn btn--small cancel" data-id="${i.id}">Cancelar</button>` : ''}</td></tr>`).join('')}</tbody></table>` : '<p>Nenhuma alteração encontrada.</p>';
    document.querySelectorAll('.activate').forEach(b => b.onclick = async () => { await api.activatePriceChange(b.dataset.id); showToast('Alteração ativada', 'success'); this.load(); });
    document.querySelectorAll('.execute').forEach(b => b.onclick = async () => { if (confirm('Executar alteração?')) { await api.executePriceChange(b.dataset.id); showToast('Alteração executada', 'success'); this.load(); } });
    document.querySelectorAll('.cancel').forEach(b => b.onclick = async () => { if (confirm('Cancelar alteração?')) { await api.deletePriceChange(b.dataset.id); showToast('Alteração cancelada', 'success'); this.load(); } });
  },
  async form() {
    const [productsResponse, stores] = await Promise.all([api.getProducts(), api.getStores()]);
    const products = productsResponse.data || productsResponse;
    document.getElementById('changeForm').innerHTML = `<form id="changeEditor" class="card margin-top"><h4>Nova alteração</h4><select name="store_id" required>${stores.map(s => `<option value="${s.id}">${s.name}</option>`).join('')}</select><select name="product_id" required>${products.map(p => `<option value="${p.id}">${p.name} — R$ ${p.current_price}</option>`).join('')}</select><input name="new_price" type="number" min="0.01" step="0.01" placeholder="Novo preço" required><input name="effective_date" type="datetime-local" required><input name="reason" placeholder="Motivo"><button class="btn btn--primary">Salvar</button></form>`;
    document.getElementById('changeEditor').onsubmit = async e => { e.preventDefault(); const data = Object.fromEntries(new FormData(e.target)); data.new_price = Number(data.new_price); try { await api.createPriceChange(data); showToast('Alteração criada', 'success'); this.render(); } catch (error) { showToast(error.message, 'error'); } };
  },
};
