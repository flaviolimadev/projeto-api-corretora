"""
Teste simples de conexão PostgreSQL
"""

import psycopg2

# Configuração do banco
DB_CONFIG = {
    'host': 'easypainel.ctrlser.com',
    'port': 5435,
    'database': 'corretora',
    'user': 'postgres',
    'password': '6b7215f9594dea0d0673',
    'sslmode': 'disable'
}

def test_connection():
    """Testar conexão com PostgreSQL"""
    print("Testando conexão com PostgreSQL...")
    print(f"Host: {DB_CONFIG['host']}:{DB_CONFIG['port']}")
    print(f"Database: {DB_CONFIG['database']}")
    print()
    
    try:
        # Conectar
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        print("OK - Conectado com sucesso!")
        
        # Testar query simples
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(f"PostgreSQL Version: {version[0]}")
        
        # Verificar se já existem tabelas
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_type = 'BASE TABLE'
            ORDER BY table_name;
        """)
        
        tables = cursor.fetchall()
        print(f"\nTabelas existentes: {len(tables)}")
        for table in tables:
            print(f"  - {table[0]}")
        
        cursor.close()
        conn.close()
        
        print("\nConexão testada com sucesso!")
        return True
        
    except Exception as e:
        print(f"\nERRO: {e}")
        return False

if __name__ == "__main__":
    test_connection()
