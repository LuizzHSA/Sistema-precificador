#!/usr/bin/env python
"""
Popula o banco com dados de amostra para testes
"""
import os
import sys
import uuid
from datetime import datetime, timedelta
from dotenv import load_dotenv

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
load_dotenv()

from app.main import create_app
from app import db
from app.models import Store, Product, PriceChange

def seed_db():
    """Popula banco com dados de amostra"""
    app = create_app()
    
    with app.app_context():
        # Limpar dados existentes
        print("🧹 Limpando dados antigos...")
        PriceChange.query.delete()
        Product.query.delete()
        Store.query.delete()
        
        print("📝 Criando dados de amostra...")
        
        # Criar lojas
        store1 = Store(
            id=str(uuid.uuid4()),
            name="Loja A - Centro",
            email="loja-a@example.com",
            phone="(11) 3000-1000"
        )
        
        store2 = Store(
            id=str(uuid.uuid4()),
            name="Loja B - Shopping",
            email="loja-b@example.com",
            phone="(11) 3000-2000"
        )
        
        db.session.add(store1)
        db.session.add(store2)
        db.session.commit()
        
        # Criar produtos
        product1 = Product(
            id=str(uuid.uuid4()),
            store_id=store1.id,
            name="Notebook Dell",
            sku="DELL-001",
            current_price=3500.00
        )
        
        product2 = Product(
            id=str(uuid.uuid4()),
            store_id=store1.id,
            name="Mouse Logitech",
            sku="LOG-002",
            current_price=150.00
        )
        
        product3 = Product(
            id=str(uuid.uuid4()),
            store_id=store2.id,
            name="Teclado Mecânico",
            sku="KEY-003",
            current_price=450.00
        )
        
        db.session.add_all([product1, product2, product3])
        db.session.commit()
        
        # Criar alterações de preço
        now = datetime.utcnow()
        
        pc1 = PriceChange(
            id=str(uuid.uuid4()),
            store_id=store1.id,
            product_id=product1.id,
            current_price=3500.00,
            new_price=3200.00,
            effective_date=now + timedelta(days=1),
            status='pending',
            reason='Promoção de aniversário'
        )
        
        pc2 = PriceChange(
            id=str(uuid.uuid4()),
            store_id=store1.id,
            product_id=product2.id,
            current_price=150.00,
            new_price=120.00,
            effective_date=now,
            status='active',
            reason='Concorrência'
        )
        
        pc3 = PriceChange(
            id=str(uuid.uuid4()),
            store_id=store2.id,
            product_id=product3.id,
            current_price=450.00,
            new_price=399.90,
            effective_date=now - timedelta(days=1),
            status='executed',
            executed_at=now,
            reason='Redução de margem'
        )
        
        db.session.add_all([pc1, pc2, pc3])
        db.session.commit()
        
        print("✅ Dados de amostra criados com sucesso!")
        print(f"📊 Lojas criadas: {Store.query.count()}")
        print(f"📦 Produtos criados: {Product.query.count()}")
        print(f"💹 Alterações de preço criadas: {PriceChange.query.count()}")

if __name__ == '__main__':
    seed_db()
