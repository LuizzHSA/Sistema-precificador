const ProductsPage = {
  async render() {
    const content = document.getElementById('content');
    try {
      const [response, stores] = await Promise.all([api.getProducts(), api.getStores()]);
      const items = response.data || response;
      content.innerHTML = `<div class="card"><div class="card-header"><h3>Produtos</h3><button id="newProduct" class="btn btn--primary">Novo produto</button></div><div class="card-body"><input id="productSearch" class="form-control" placeholder="Buscar por nome ou SKU"><div id="productForm"></div><div class="table-responsive"><table><thead><tr><th>Nome</th><th>SKU</th><th>Loja</th><th>Preço</th><th>Ações</th></tr></thead><tbody id="productsTable"></tbody></table></div></div></div>`;
      const draw = list => { document.getElementById('productsTable').innerHTML = list.length ? list.map(p => `<tr><td>${p.name}</td><td>${p.sku}</td><td>${p.store || '-'}</td><td>R$ ${Number(p.current_price).toFixed(2)}</td><td><button class="btn btn--small details-product" data-id="${p.id}">Detalhes</button> <button class="btn btn--small edit-product" data-id="${p.id}">Editar</button> <button class="btn btn--small delete-product" data-id="${p.id}">Excluir</button></td></tr>`).join('') : '<tr><td colspan="5">Nenhum produto encontrado.</td></tr>'; };
      draw(items);
      document.getElementById('productSearch').addEventListener('input', async e => draw((await api.getProducts({search: e.target.value})).data || []));
      document.getElementById('newProduct').addEventListener('click', () => this.form(null, stores, draw));
      content.querySelectorAll('.details-product').forEach(btn => btn.addEventListener('click', () => this.details(btn.dataset.id)));
      content.querySelectorAll('.edit-product').forEach(btn => btn.addEventListener('click', () => this.form(items.find(p => p.id === btn.dataset.id), stores, draw)));
      content.querySelectorAll('.delete-product').forEach(btn => btn.addEventListener('click', async () => { if (confirm('Excluir este produto?')) { await api.deleteProduct(btn.dataset.id); showToast('Produto excluído', 'success'); this.render(); } }));
    } catch (error) { content.innerHTML = `<div class="card"><div class="card-body">${error.message}</div></div>`; }
  },
  async details(productId) {
    try {
      const result = await api.getProductHistory(productId);
      const changes = result.data || [];
      const product = result.product;
      const box = document.getElementById('productForm');
      box.innerHTML = `<div class="card margin-top"><div class="card-header"><h4>${product.name}</h4><button id="closeProductDetails" class="btn">Fechar</button></div><div class="card-body"><p><strong>SKU:</strong> ${product.sku} | <strong>Loja:</strong> ${product.store || '-'} | <strong>Preço atual:</strong> R$ ${Number(product.current_price).toFixed(2)}</p><h5>Histórico de preços</h5>${changes.length ? `<table><thead><tr><th>Data</th><th>Anterior</th><th>Novo</th><th>Status</th><th>Variação</th></tr></thead><tbody>${changes.map(item => `<tr><td>${new Date(item.created_at).toLocaleString('pt-BR')}</td><td>R$ ${Number(item.current_price).toFixed(2)}</td><td>R$ ${Number(item.new_price).toFixed(2)}</td><td>${item.status}</td><td>${item.percentage_change}%</td></tr>`).join('')}</tbody></table>` : '<p>Nenhuma alteração registrada.</p>'}</div></div>`;
      document.getElementById('closeProductDetails').onclick = () => { box.innerHTML = ''; };
    } catch (error) { showToast(error.message, 'error'); }
  },
  form(product, stores) {
    const box = document.getElementById('productForm');
    box.innerHTML = `<form id="productEditor" class="card margin-top"><h4>${product ? 'Editar' : 'Novo'} produto</h4><input name="name" placeholder="Nome" required value="${product?.name || ''}"><input name="sku" placeholder="SKU" required value="${product?.sku || ''}"><select name="store_id" required>${stores.map(s => `<option value="${s.id}" ${product?.store_id === s.id ? 'selected' : ''}>${s.name}</option>`).join('')}</select><input name="current_price" type="number" min="0.01" step="0.01" placeholder="Preço" required value="${product?.current_price || ''}"><button class="btn btn--primary">Salvar</button> <button type="button" id="cancelProduct" class="btn">Cancelar</button></form>`;
    document.getElementById('cancelProduct').onclick = () => box.innerHTML = '';
    document.getElementById('productEditor').onsubmit = async e => { e.preventDefault(); const data = Object.fromEntries(new FormData(e.target)); data.current_price = Number(data.current_price); try { if (product) await api.updateProduct(product.id, data); else await api.createProduct(data); showToast('Produto salvo', 'success'); this.render(); } catch (error) { showToast(error.message, 'error'); } };
  },
};
