"""
Worker principal otimizado para produção
Inclui monitoramento, retry logic e configuração via variáveis de ambiente
"""

import asyncio
import logging
import time
import threading
import signal
import sys
import os
from datetime import datetime
from typing import Dict, Any
import json

# Adicionar o diretório pai ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.postgres_manager import postgres_manager
from workers.sync_categories_postgres import sync_categories
from workers.sync_assets_postgres import sync_assets
from workers.sync_candles_postgres import sync_candles
from workers.sync_current_candles_postgres import sync_current_candles

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/app/logs/worker.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


class ProductionWorker:
    """Worker principal otimizado para produção"""
    
    def __init__(self):
        self.running = False
        self.threads = {}
        self.worker_stats = {}
        self.shutdown_event = threading.Event()
        
        # Configurações via variáveis de ambiente
        self.intervals = {
            'categories': int(os.getenv('SYNC_INTERVAL_CATEGORIES', 3600)),
            'assets': int(os.getenv('SYNC_INTERVAL_ASSETS', 1800)),
            'candles': int(os.getenv('SYNC_INTERVAL_CANDLES', 3600)),
            'current_candles': int(os.getenv('SYNC_INTERVAL_CURRENT', 60))
        }
        
        # Configurações de retry
        self.max_retries = int(os.getenv('MAX_RETRIES', 3))
        self.retry_delay = int(os.getenv('RETRY_DELAY', 60))
        
        # Funções dos workers
        self.workers = {
            'categories': sync_categories,
            'assets': sync_assets,
            'candles': sync_candles,
            'current_candles': sync_current_candles
        }
        
        # Estatísticas dos workers
        for worker_name in self.workers.keys():
            self.worker_stats[worker_name] = {
                'last_run': None,
                'last_success': None,
                'last_error': None,
                'total_runs': 0,
                'successful_runs': 0,
                'failed_runs': 0,
                'consecutive_failures': 0
            }
        
        # Configurar handlers de sinal para shutdown graceful
        signal.signal(signal.SIGTERM, self._signal_handler)
        signal.signal(signal.SIGINT, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        """Handler para sinais de shutdown"""
        logger.info(f"Recebido sinal {signum}, iniciando shutdown graceful...")
        self.shutdown_event.set()
        self.stop_all_workers()
    
    def _execute_worker_with_retry(self, worker_name: str) -> bool:
        """Executar worker com lógica de retry"""
        worker_func = self.workers[worker_name]
        stats = self.worker_stats[worker_name]
        
        for attempt in range(self.max_retries + 1):
            try:
                logger.info(f"Executando {worker_name} (tentativa {attempt + 1}/{self.max_retries + 1})")
                start_time = time.time()
                
                # Executar worker
                success = worker_func()
                
                duration = time.time() - start_time
                stats['last_run'] = datetime.now().isoformat()
                stats['total_runs'] += 1
                
                if success:
                    stats['last_success'] = datetime.now().isoformat()
                    stats['successful_runs'] += 1
                    stats['consecutive_failures'] = 0
                    stats['last_error'] = None
                    
                    logger.info(f"{worker_name} concluído com sucesso em {duration:.2f}s")
                    return True
                else:
                    stats['failed_runs'] += 1
                    stats['consecutive_failures'] += 1
                    error_msg = f"{worker_name} retornou False"
                    stats['last_error'] = error_msg
                    
                    logger.warning(f"{worker_name} falhou: {error_msg}")
                    
                    if attempt < self.max_retries:
                        logger.info(f"Aguardando {self.retry_delay}s antes da próxima tentativa...")
                        time.sleep(self.retry_delay)
                    
            except Exception as e:
                stats['failed_runs'] += 1
                stats['consecutive_failures'] += 1
                error_msg = str(e)
                stats['last_error'] = error_msg
                
                logger.error(f"Erro no worker {worker_name} (tentativa {attempt + 1}): {e}")
                
                if attempt < self.max_retries:
                    logger.info(f"Aguardando {self.retry_delay}s antes da próxima tentativa...")
                    time.sleep(self.retry_delay)
        
        logger.error(f"{worker_name} falhou após {self.max_retries + 1} tentativas")
        return False
    
    def start_worker(self, worker_name: str, interval: int):
        """Iniciar um worker específico"""
        def worker_loop():
            logger.info(f"Iniciando worker: {worker_name} (intervalo: {interval}s)")
            
            while not self.shutdown_event.is_set():
                try:
                    # Executar worker com retry
                    self._execute_worker_with_retry(worker_name)
                    
                    # Aguardar próximo intervalo ou shutdown
                    if self.shutdown_event.wait(interval):
                        break
                        
                except Exception as e:
                    logger.error(f"Erro crítico no worker {worker_name}: {e}")
                    # Aguardar antes de tentar novamente
                    if self.shutdown_event.wait(60):
                        break
        
        thread = threading.Thread(target=worker_loop, daemon=True, name=f"worker-{worker_name}")
        thread.start()
        self.threads[worker_name] = thread
        logger.info(f"Worker {worker_name} iniciado")
    
    def start_all_workers(self):
        """Iniciar todos os workers"""
        logger.info("Iniciando Production Worker...")
        logger.info(f"Configurações: {json.dumps(self.intervals, indent=2)}")
        
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
        self.shutdown_event.set()
        
        # Aguardar threads terminarem
        for worker_name, thread in self.threads.items():
            if thread.is_alive():
                thread.join(timeout=10)
                if thread.is_alive():
                    logger.warning(f"Worker {worker_name} não parou em 10s")
                else:
                    logger.info(f"Worker {worker_name} parado")
        
        logger.info("Todos os workers parados")
    
    def get_status(self) -> Dict[str, Any]:
        """Obter status detalhado dos workers"""
        try:
            # Conectar ao banco para obter estatísticas
            db_connected = postgres_manager.connect()
            
            if db_connected:
                try:
                    categories = postgres_manager.get_all_categories()
                    assets = postgres_manager.get_all_assets(limit=1000)
                    current_candles = postgres_manager.get_all_current_candles()
                    recent_logs = postgres_manager.get_recent_sync_logs(limit=10)
                finally:
                    postgres_manager.disconnect()
            else:
                categories = []
                assets = []
                current_candles = []
                recent_logs = []
            
            # Calcular estatísticas de uptime
            uptime = time.time() - self.start_time if hasattr(self, 'start_time') else 0
            
            status = {
                'running': self.running,
                'uptime_seconds': uptime,
                'workers': {
                    'active': list(self.threads.keys()),
                    'intervals': self.intervals,
                    'statistics': self.worker_stats
                },
                'database': {
                    'connected': db_connected,
                    'categories_count': len(categories),
                    'assets_count': len(assets),
                    'current_candles_count': len(current_candles)
                },
                'recent_logs': recent_logs,
                'timestamp': datetime.now().isoformat()
            }
            
            return status
            
        except Exception as e:
            logger.error(f"Erro ao obter status: {e}")
            return {
                'error': str(e),
                'running': self.running,
                'timestamp': datetime.now().isoformat()
            }
    
    def save_status_to_file(self):
        """Salvar status em arquivo para monitoramento externo"""
        try:
            status = self.get_status()
            status_file = '/app/logs/worker_status.json'
            
            with open(status_file, 'w') as f:
                json.dump(status, f, indent=2, default=str)
                
        except Exception as e:
            logger.error(f"Erro ao salvar status: {e}")


def run_production_worker():
    """Executar o worker de produção"""
    print("=" * 80)
    print("PRODUCTION WORKER - SINCRONIZADOR AUTOMATICO")
    print("=" * 80)
    print()
    
    # Mostrar configurações
    print("Configurações:")
    print(f"  - SYNC_INTERVAL_CATEGORIES: {os.getenv('SYNC_INTERVAL_CATEGORIES', 3600)}s")
    print(f"  - SYNC_INTERVAL_ASSETS: {os.getenv('SYNC_INTERVAL_ASSETS', 1800)}s")
    print(f"  - SYNC_INTERVAL_CANDLES: {os.getenv('SYNC_INTERVAL_CANDLES', 3600)}s")
    print(f"  - SYNC_INTERVAL_CURRENT: {os.getenv('SYNC_INTERVAL_CURRENT', 60)}s")
    print(f"  - MAX_RETRIES: {os.getenv('MAX_RETRIES', 3)}")
    print(f"  - RETRY_DELAY: {os.getenv('RETRY_DELAY', 60)}s")
    print()
    print("Pressione Ctrl+C para parar")
    print("=" * 80)
    print()
    
    worker = ProductionWorker()
    worker.start_time = time.time()
    
    try:
        # Iniciar todos os workers
        worker.start_all_workers()
        
        # Loop principal
        last_status_save = time.time()
        while not worker.shutdown_event.is_set():
            # Salvar status a cada 5 minutos
            if time.time() - last_status_save > 300:
                worker.save_status_to_file()
                last_status_save = time.time()
            
            # Aguardar 1 minuto ou até shutdown
            if worker.shutdown_event.wait(60):
                break
            
            # Mostrar status a cada 10 minutos
            if int(time.time()) % 600 == 0:
                status = worker.get_status()
                if 'error' not in status:
                    db_stats = status.get('database', {})
                    logger.info(f"Status: {db_stats.get('categories_count', 0)} categorias, "
                              f"{db_stats.get('assets_count', 0)} ativos, "
                              f"{db_stats.get('current_candles_count', 0)} candles atuais")
    
    except KeyboardInterrupt:
        print("\nRecebido Ctrl+C, parando workers...")
    except Exception as e:
        logger.error(f"Erro no Production Worker: {e}")
    finally:
        worker.stop_all_workers()
        worker.save_status_to_file()
        print("Workers parados com sucesso!")


if __name__ == "__main__":
    run_production_worker()
