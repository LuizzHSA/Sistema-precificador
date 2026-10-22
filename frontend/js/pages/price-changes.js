const PriceChangesPage = {
  async render() {
    const content = document.getElementById('content');
    try {
      const [productsResponse, stores] = await Promise.all([api.getProducts(), api.getStores()]);
      const products = productsResponse.data || productsResponse;
      content.innerHTML = `<div class="card"><div class="card-header"><h3>Alterações de preço</h3><button id="newChange" class="btn btn--primary">Nova alteração</button></div><div class="card-body"><div class="flex"><select id="statusFilter"><option value="">Todos os status</option><option value="pending">Pendente</option><option value="active">Ativa</option><option value="executed">Executada</option><option value="cancelled">Cancelada</option></select><select id="storeFilter"><option value="">Todas as lojas</option>${stores.map(s => `<option value="${escapeHtml(s.id)}">${escapeHtml(s.name)}</option>`).join('')}</select><select id="productFilter"><option value="">Todos os produtos</option>${products.map(p => `<option value="${escapeHtml(p.id)}">${escapeHtml(p.name)}</option>`).join('')}</select><input id="changeSearch" placeholder="Buscar produto, SKU ou motivo"><button id="clearFilters" class="btn">Limpar filtros</button></div><div id="changeForm"></div><div id="changeTable">Carregando...</div></div></div>`;
      const load = async () => {
        try {
          const response = await api.getPriceChanges({
            status: document.getElementById('statusFilter').value,
            store_id: document.getElementById('storeFilter').value,
            product_id: document.getElementById('productFilter').value,
            search: document.getElementById('changeSearch').value,
            per_page: 100,
          });
          this.draw(response.data || response.items || []);
        } catch (error) {
          document.getElementById('changeTable').textContent = error.message || 'Não foi possível carregar as alterações.';
        }
      };
      document.getElementById('statusFilter').onchange = load;
      document.getElementById('storeFilter').onchange = load;
      document.getElementById('productFilter').onchange = load;
      document.getElementById('changeSearch').oninput = load;
      document.getElementById('clearFilters').onclick = () => {
        document.getElementById('statusFilter').value = '';
        document.getElementById('storeFilter').value = '';
        document.getElementById('productFilter').value = '';
        document.getElementById('changeSearch').value = '';
        load();
      };
      document.getElementById('newChange').onclick = () => this.form();
      this.load = load;
      await load();
    } catch (error) {
      content.innerHTML = `<div class="card"><div class="card-body">${escapeHtml(error.message || 'Não foi possível carregar as alterações de preço.')}</div></div>`;
    }
  },

  draw(items) {
    const table = document.getElementById('changeTable');
    if (!table) return;
    table.innerHTML = items.length ? `<table><thead><tr><th>Produto</th><th>Atual</th><th>Novo</th><th>Variação</th><th>Data</th><th>Status</th><th>Ações</th></tr></thead><tbody>${items.map(i => `<tr><td>${escapeHtml(i.product || i.product_name || '-')}</td><td>R$ ${Number(i.current_price).toFixed(2)}</td><td>R$ ${Number(i.new_price).toFixed(2)}</td><td>${i.percentage_change > 0 ? '+' : ''}${i.percentage_change}%</td><td>${new Date(i.effective_date).toLocaleDateString('pt-BR')}</td><td>${escapeHtml(i.status)}</td><td><button class="btn btn--small details" data-id="${escapeHtml(i.id)}">Detalhes</button>${i.status === 'pending' ? `<button class="btn btn--small activate" data-id="${escapeHtml(i.id)}">Ativar</button>` : ''}${i.status === 'active' ? `<button class="btn btn--small execute" data-id="${escapeHtml(i.id)}">Executar</button>` : ''}${['pending','active'].includes(i.status) ? `<button class="btn btn--small cancel" data-id="${escapeHtml(i.id)}">Cancelar</button>` : ''}</td></tr>`).join('')}</tbody></table>` : '<p>Nenhuma alteração encontrada.</p>';

    table.querySelectorAll('.details').forEach(button => button.onclick = async () => {
      try {
        const item = await api.getPriceChange(button.dataset.id);
        showToast(`${item.product || '-'}: ${item.reason || 'Sem motivo'} | diferença R$ ${item.price_difference}`, 'info', 6000);
      } catch (error) { showToast(error.message || 'Não foi possível carregar os detalhes', 'error'); }
    });
    table.querySelectorAll('.activate').forEach(button => button.onclick = async () => {
      try { await api.activatePriceChange(button.dataset.id); showToast('Alteração ativada', 'success'); await this.load(); }
      catch (error) { showToast(error.message || 'Não foi possível ativar a alteração', 'error'); }
    });
    table.querySelectorAll('.execute').forEach(button => button.onclick = async () => {
      if (!confirm('Executar alteração?')) return;
      try { await api.executePriceChange(button.dataset.id); showToast('Alteração executada', 'success'); await this.load(); }
      catch (error) { showToast(error.message || 'Não foi possível executar a alteração', 'error'); }
    });
    table.querySelectorAll('.cancel').forEach(button => button.onclick = async () => {
      if (!confirm('Cancelar alteração?')) return;
      try { await api.deletePriceChange(button.dataset.id); showToast('Alteração cancelada', 'success'); await this.load(); }
      catch (error) { showToast(error.message || 'Não foi possível cancelar a alteração', 'error'); }
    });
  },

  async form() {
    try {
      const [productsResponse, stores] = await Promise.all([api.getProducts(), api.getStores()]);
      const products = productsResponse.data || productsResponse;
      if (!stores.length || !products.length) {
        showToast('Cadastre uma loja e pelo menos um produto antes de criar uma alteração.', 'error');
        return;
      }
      const box = document.getElementById('changeForm');
      const firstStoreId = stores[0].id;
      const optionsForStore = storeId => products.filter(product => product.store_id === storeId);
      const initialProducts = optionsForStore(firstStoreId);
      box.innerHTML = `<form id="changeEditor" class="card margin-top"><h4>Nova alteração</h4><label for="changeStore">Loja</label><select id="changeStore" name="store_id" required>${stores.map(s => `<option value="${escapeHtml(s.id)}">${escapeHtml(s.name)}</option>`).join('')}</select><label for="changeProduct">Produto</label><select id="changeProduct" name="product_id" required>${initialProducts.map(p => `<option value="${escapeHtml(p.id)}">${escapeHtml(p.name)} — R$ ${Number(p.current_price).toFixed(2)}</option>`).join('')}</select><output id="currentPrice">Preço atual: R$ ${Number(initialProducts[0]?.current_price || 0).toFixed(2)}</output><label for="newPrice">Novo preço</label><input id="newPrice" name="new_price" type="number" min="0.01" step="0.01" placeholder="Novo preço" required><label for="effectiveDate">Data efetiva</label><input id="effectiveDate" name="effective_date" type="datetime-local" required><label for="changeReason">Motivo</label><input id="changeReason" name="reason" maxlength="500" placeholder="Motivo"><button class="btn btn--primary" type="submit" ${initialProducts.length ? '' : 'disabled'}>Salvar</button><button class="btn" id="cancelChange" type="button">Cancelar</button></form>`;

      const updateCurrentPrice = () => {
        const product = products.find(item => item.id === document.getElementById('changeProduct').value);
        document.getElementById('currentPrice').textContent = `Preço atual: R$ ${Number(product?.current_price || 0).toFixed(2)}`;
      };
      document.getElementById('changeStore').onchange = event => {
        const matching = optionsForStore(event.target.value);
        const select = document.getElementById('changeProduct');
        select.innerHTML = matching.map(p => `<option value="${escapeHtml(p.id)}">${escapeHtml(p.name)} — R$ ${Number(p.current_price).toFixed(2)}</option>`).join('');
        select.disabled = matching.length === 0;
        document.querySelector('#changeEditor button[type="submit"]').disabled = matching.length === 0;
        updateCurrentPrice();
      };
      document.getElementById('changeProduct').onchange = updateCurrentPrice;
      document.getElementById('cancelChange').onclick = () => { box.innerHTML = ''; };
      document.getElementById('changeEditor').onsubmit = async event => {
        event.preventDefault();
        const data = Object.fromEntries(new FormData(event.currentTarget));
        data.new_price = Number(data.new_price);
        const submit = event.currentTarget.querySelector('button[type="submit"]');
        submit.disabled = true;
        try {
          await api.createPriceChange(data);
          showToast('Alteração criada', 'success');
          box.innerHTML = '';
          await this.load();
        } catch (error) {
          showToast(error.message || 'Não foi possível criar a alteração', 'error');
          submit.disabled = false;
        }
      };
    } catch (error) {
      showToast(error.message || 'Não foi possível abrir o formulário', 'error');
    }
  },
};
