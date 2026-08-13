#!/usr/bin/env python
"""
Script para setup rápido do projeto
"""
import os
import sys
import subprocess
import platform

def run_command(cmd, description, cwd=None):
    """Executa um comando e mostra o resultado"""
    print(f"\n{'='*60}")
    print(f"▶ {description}")
    print(f"{'='*60}")
    result = subprocess.run(cmd, shell=True, cwd=cwd)
    if result.returncode != 0:
        print(f"❌ Erro ao executar: {description}")
        return False
    return True

def main():
    """Setup principal"""
    print("\n" + "🎬 SETUP DO SISTEMA DE PRECIFICAÇÃO".center(60))
    print("="*60)
    
    # Verificar Python
    if sys.version_info < (3, 9):
        print("❌ Python 3.9+ é necessário")
        sys.exit(1)
    
    print(f"✅ Python {sys.version.split()[0]} encontrado")
    
    # Backend setup
    print("\n📦 Configurando Backend...")
    backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
    
    # 1. Crear venv
    venv_path = os.path.join(backend_dir, 'venv')
    if not os.path.exists(venv_path):
        print("▶ Criando virtual environment...")
        cmd = f'{sys.executable} -m venv venv'
        run_command(cmd, "Virtual environment", cwd=backend_dir)
    
    # 2. Instalar dependências
    if platform.system() == 'Windows':
        pip_cmd = os.path.join(venv_path, 'Scripts', 'pip')
        python_cmd = os.path.join(venv_path, 'Scripts', 'python')
    else:
        pip_cmd = os.path.join(venv_path, 'bin', 'pip')
        python_cmd = os.path.join(venv_path, 'bin', 'python')
    
    print(f"\n▶ Instalando dependências do backend...")
    run_command(f'{pip_cmd} install -r requirements.txt', "Instalação de dependências", cwd=backend_dir)
    
    # 3. Inicializar banco de dados
    print(f"\n▶ Inicializando banco de dados...")
    run_command(f'{python_cmd} init_db.py', "Inicialização do banco de dados", cwd=backend_dir)
    
    # 4. Popular com dados de amostra
    print(f"\n▶ Populando banco com dados de amostra...")
    run_command(f'{python_cmd} seed.py', "Seed de dados", cwd=backend_dir)
    
    print("\n" + "="*60)
    print("✅ SETUP COMPLETO!")
    print("="*60)
    print("\n📋 Próximos passos:")
    print("\n1️⃣  Terminal 1 - Iniciar Backend (API):")
    if platform.system() == 'Windows':
        print(f"   cd backend")
        print(f"   venv\\Scripts\\activate")
        print(f"   python main.py")
    else:
        print(f"   cd backend")
        print(f"   source venv/bin/activate")
        print(f"   python main.py")
    
    print("\n2️⃣  Terminal 2 - Iniciar Frontend (UI):")
    print("   cd frontend")
    print("   python -m http.server 8080")
    
    print("\n3️⃣  Acessar no navegador:")
    print("   http://localhost:8080")
    
    print("\n🔑 Credenciais de teste:")
    print("   Email: admin@pricetracker.com")
    print("   Senha: admin123")
    
    print("\n📚 API disponível em:")
    print("   http://localhost:5000")
    print("   Health check: http://localhost:5000/health")
    
    print("\n" + "="*60 + "\n")

if __name__ == '__main__':
    main()
