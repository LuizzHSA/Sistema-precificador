const StoresPage = {
  async render() {
    const content = document.getElementById('content');
    try {
      content.innerHTML = '<div class="card"><div class="card-body">Carregando lojas...</div></div>';
      const items = await api.getStores();
      content.innerHTML = `<div class="card"><div class="card-header"><h3>Lojas</h3><button id="newStore" class="btn btn--primary">Nova loja</button></div><div class="card-body"><input id="storeSearch" class="form-control" placeholder="Buscar loja"><div id="storeForm"></div><div class="table-responsive"><table><thead><tr><th>Nome</th><th>Email</th><th>Telefone</th><th>Ações</th></tr></thead><tbody id="storesTable"></tbody></table></div></div></div>`;

      const draw = list => {
        document.getElementById('storesTable').innerHTML = list.length
          ? list.map(s => `<tr><td>${escapeHtml(s.name)}</td><td>${escapeHtml(s.email)}</td><td>${escapeHtml(s.phone || '-')}</td><td><button class="btn btn--small edit-store" data-id="${escapeHtml(s.id)}">Editar</button> <button class="btn btn--small delete-store" data-id="${escapeHtml(s.id)}">Excluir</button></td></tr>`).join('')
          : '<tr><td colspan="4">Nenhuma loja encontrada.</td></tr>';

        content.querySelectorAll('.edit-store').forEach(btn => {
          btn.onclick = () => this.form(list.find(s => s.id === btn.dataset.id));
        });
        content.querySelectorAll('.delete-store').forEach(btn => {
          btn.onclick = async () => {
            if (!confirm('Excluir esta loja?')) return;
            try {
              await api.deleteStore(btn.dataset.id);
              showToast('Loja excluída', 'success');
              await this.render();
            } catch (error) {
              showToast(error.message || 'Não foi possível excluir a loja', 'error');
            }
          };
        });
      };

      draw(items);
      document.getElementById('storeSearch').addEventListener('input', async e => {
        try {
          draw(await api.getStores(e.target.value));
        } catch (error) {
          const table = document.getElementById('storesTable');
          if (table) table.textContent = error.message || 'Não foi possível carregar as lojas.';
        }
      });
      document.getElementById('newStore').onclick = () => this.form();
    } catch (error) {
      content.innerHTML = `<div class="card"><div class="card-body">${escapeHtml(error.message || 'Não foi possível carregar as lojas.')}</div></div>`;
    }
  },

  form(store) {
    const box = document.getElementById('storeForm');
    box.innerHTML = `<form id="storeEditor" class="card margin-top"><h4>${store ? 'Editar' : 'Nova'} loja</h4><input name="name" placeholder="Nome" required maxlength="120" value="${escapeHtml(store?.name || '')}"><input name="email" type="email" placeholder="Email" required maxlength="255" value="${escapeHtml(store?.email || '')}"><input name="phone" placeholder="Telefone" maxlength="40" value="${escapeHtml(store?.phone || '')}"><button class="btn btn--primary">Salvar</button> <button type="button" id="cancelStore" class="btn">Cancelar</button></form>`;
    document.getElementById('cancelStore').onclick = () => { box.innerHTML = ''; };
    document.getElementById('storeEditor').onsubmit = async e => {
      e.preventDefault();
      const data = Object.fromEntries(new FormData(e.target));
      const submit = e.target.querySelector('button[type="submit"], button:not([type])');
      if (submit) { submit.disabled = true; submit.textContent = 'Salvando...'; }
      try {
        if (store) await api.updateStore(store.id, data);
        else await api.createStore(data);
        showToast('Loja salva', 'success');
        await this.render();
      } catch (error) {
        showToast(error.message || 'Não foi possível salvar a loja', 'error');
        if (submit) { submit.disabled = false; submit.textContent = 'Salvar'; }
      }
    };
  },
};
