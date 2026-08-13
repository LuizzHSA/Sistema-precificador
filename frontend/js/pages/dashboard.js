// Dashboard page
const DashboardPage = {
  async render() {
    const content = document.getElementById('content');
    content.innerHTML = `
            <div class="grid grid--3">
                <div class="card">
                    <div class="card-body">
                        <div style="text-align: center; padding: 20px;">
                            <h3 style="font-size: 2.5rem; margin: 10px 0; color: var(--primary);">0</h3>
                            <p style="color: var(--text-muted);">Alterações Hoje</p>
                        </div>
                    </div>
                </div>
                
                <div class="card">
                    <div class="card-body">
                        <div style="text-align: center; padding: 20px;">
                            <h3 style="font-size: 2.5rem; margin: 10px 0; color: var(--success);">0</h3>
                            <p style="color: var(--text-muted);">Executadas</p>
                        </div>
                    </div>
                </div>
                
                <div class="card">
                    <div class="card-body">
                        <div style="text-align: center; padding: 20px;">
                            <h3 style="font-size: 2.5rem; margin: 10px 0; color: var(--warning);">0</h3>
                            <p style="color: var(--text-muted);">Pendentes</p>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="card margin-top">
                <div class="card-header">
                    <h3>Alterações Recentes</h3>
                </div>
                <div class="card-body">
                    <p style="text-align: center; color: var(--text-muted);">
                        Nenhuma alteração para exibir
                    </p>
                </div>
            </div>
        `;
  },
};
