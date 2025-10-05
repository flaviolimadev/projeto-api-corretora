"""
Verificar categorias no banco
"""

from database.postgres_manager import postgres_manager

def check_categories():
    """Verificar categorias no banco"""
    print("Verificando categorias no PostgreSQL...")
    
    try:
        # Conectar
        if not postgres_manager.connect():
            print("ERRO: Falha ao conectar")
            return
        
        # Obter categorias
        categories = postgres_manager.get_all_categories()
        print(f"\nTotal de categorias: {len(categories)}")
        print()
        
        for cat in categories:
            print(f"  - {cat['key']}: {cat['name']}")
            print(f"    Exchanges: {len(cat['exchanges'])}")
            print(f"    Timeframes: {len(cat['timeframes'])}")
            print()
        
        postgres_manager.disconnect()
        print("Verificação concluída!")
        
    except Exception as e:
        print(f"ERRO: {e}")

if __name__ == "__main__":
    check_categories()
