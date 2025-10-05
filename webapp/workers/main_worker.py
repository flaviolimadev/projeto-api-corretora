"""
Worker principal que executa todos os workers de sincronização
"""

import asyncio
import logging
import time
import threading
from datetime import datetime
import sys
import os

# Adicionar o diretório pai ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.postgres_manager import postgres_manager
from workers.sync_categories_postgres import sync_categories
from workers.sync_assets_postgres import sync_assets
from workers.sync_candles_postgres import sync_candles
from workers.sync_current_candles_postgres import sync_current_candles

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


class MainWorker:
    """Worker principal que gerencia todos os workers de sincronização"""
    
    def __init__(self):
        self.running = False
        self.threads = {}
        
        # Intervalos de sincronização (em segundos)
        self.intervals = {
            'categories': 3600,    # 1 hora
            'assets': 1800,        # 30 minutos
            'candles': 3600,       # 1 hora
            'current_candles': 60  # 1 minuto
        }
        
        # Funções dos workers
        self.workers = {
            'categories': sync_categories,
            'assets': sync_assets,
            'candles': sync_candles,
            'current_candles': sync_current_candles
        }
    
    def start_worker(self, worker_name, interval):
        """Iniciar um worker específico"""
        def worker_loop():
            logger.info(f"Iniciando worker: {worker_name} (intervalo: {interval}s)")
            
            while self.running:
                try:
                    logger.info(f"Executando {worker_name}...")
                    start_time = time.time()
                    
                    # Executar worker
                    success = self.workers[worker_name]()
                    
                    duration = time.time() - start_time
                    if success:
                        logger.info(f"{worker_name} concluído com sucesso em {duration:.2f}s")
                    else:
                        logger.error(f"{worker_name} falhou em {duration:.2f}s")
                    
                    # Aguardar próximo intervalo
                    time.sleep(interval)
                    
                except Exception as e:
                    logger.error(f"Erro no worker {worker_name}: {e}")
                    time.sleep(60)  # Aguardar 1 minuto em caso de erro
        
        thread = threading.Thread(target=worker_loop, daemon=True)
        thread.start()
        self.threads[worker_name] = thread
        logger.info(f"Worker {worker_name} iniciado")
    
    def start_all_workers(self):
        """Iniciar todos os workers"""
        logger.info("Iniciando Main Worker...")
        self.running = True
        
        # Iniciar cada worker
        for worker_name, interval in self.intervals.items():
            self.start_worker(worker_name, interval)
        
        logger.info("Todos os workers iniciados!")
        logger.info("Workers ativos:")
        for worker_name, interval in self.intervals.items():
            logger.info(f"  - {worker_name}: a cada {interval}s")
    
    def stop_all_workers(self):
        """Parar todos os workers"""
        logger.info("Parando todos os workers...")
        self.running = False
        
        # Aguardar threads terminarem
        for worker_name, thread in self.threads.items():
            thread.join(timeout=10)
            logger.info(f"Worker {worker_name} parado")
        
        logger.info("Todos os workers parados")
    
    def get_status(self):
        """Obter status dos workers"""
        if not postgres_manager.connect():
            return {"error": "Falha ao conectar ao banco"}
        
        try:
            # Obter logs recentes
            logs = postgres_manager.get_recent_sync_logs(limit=20)
            
            # Obter estatísticas
            categories = postgres_manager.get_all_categories()
            assets = postgres_manager.get_all_assets(limit=1000)
            current_candles = postgres_manager.get_all_current_candles()
            
            status = {
                'running': self.running,
                'workers': list(self.threads.keys()),
                'intervals': self.intervals,
                'statistics': {
                    'categories': len(categories),
                    'assets': len(assets),
                    'current_candles': len(current_candles)
                },
                'recent_logs': logs
            }
            
            return status
            
        except Exception as e:
            return {"error": str(e)}
        finally:
            postgres_manager.disconnect()


def run_main_worker():
    """Executar o worker principal"""
    print("=" * 70)
    print("MAIN WORKER - SINCRONIZADOR AUTOMATICO")
    print("=" * 70)
    print()
    print("Workers que serão iniciados:")
    print("  - categories: a cada 1 hora")
    print("  - assets: a cada 30 minutos")
    print("  - candles: a cada 1 hora")
    print("  - current_candles: a cada 1 minuto")
    print()
    print("Pressione Ctrl+C para parar")
    print("=" * 70)
    print()
    
    main_worker = MainWorker()
    
    try:
        # Iniciar todos os workers
        main_worker.start_all_workers()
        
        # Manter o programa rodando
        while True:
            time.sleep(60)  # Verificar a cada minuto
            
            # Mostrar status a cada 5 minutos
            if int(time.time()) % 300 == 0:
                status = main_worker.get_status()
                if 'error' not in status:
                    logger.info(f"Status: {status['statistics']['categories']} categorias, "
                              f"{status['statistics']['assets']} ativos, "
                              f"{status['statistics']['current_candles']} candles atuais")
    
    except KeyboardInterrupt:
        print("\nParando workers...")
        main_worker.stop_all_workers()
        print("Workers parados com sucesso!")
    
    except Exception as e:
        logger.error(f"Erro no Main Worker: {e}")
        main_worker.stop_all_workers()


if __name__ == "__main__":
    run_main_worker()
