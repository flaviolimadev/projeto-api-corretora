import sys
import os
import logging
import time
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importar workers específicos
from workers.sync_categories_postgres import sync_categories
from workers.sync_assets_postgres import sync_assets
from workers.sync_candles_postgres import sync_candles
from workers.sync_current_candles_windows import sync_current_candles_windows

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def run_categories():
    """Executar sincronização de categorias"""
    try:
        logger.info("Executando categories...")
        start_time = datetime.now()
        success = sync_categories()
        duration = (datetime.now() - start_time).total_seconds()
        
        if success:
            logger.info(f"categories concluído com sucesso em {duration:.2f}s")
        else:
            logger.error(f"categories falhou em {duration:.2f}s")
    except Exception as e:
        logger.error(f"Erro em categories: {e}")

def run_assets():
    """Executar sincronização de ativos"""
    try:
        logger.info("Executando assets...")
        start_time = datetime.now()
        success = sync_assets()
        duration = (datetime.now() - start_time).total_seconds()
        
        if success:
            logger.info(f"assets concluído com sucesso em {duration:.2f}s")
        else:
            logger.error(f"assets falhou em {duration:.2f}s")
    except Exception as e:
        logger.error(f"Erro em assets: {e}")

def run_candles():
    """Executar sincronização de candles históricos"""
    try:
        logger.info("Executando candles...")
        start_time = datetime.now()
        success = sync_candles()
        duration = (datetime.now() - start_time).total_seconds()
        
        if success:
            logger.info(f"candles concluído com sucesso em {duration:.2f}s")
        else:
            logger.error(f"candles falhou em {duration:.2f}s")
    except Exception as e:
        logger.error(f"Erro em candles: {e}")

def run_current_candles():
    """Executar sincronização de candles atuais (Windows otimizado)"""
    try:
        logger.info("Executando current_candles...")
        start_time = datetime.now()
        success = sync_current_candles_windows()
        duration = (datetime.now() - start_time).total_seconds()
        
        if success:
            logger.info(f"current_candles concluído com sucesso em {duration:.2f}s")
        else:
            logger.error(f"current_candles falhou em {duration:.2f}s")
    except Exception as e:
        logger.error(f"Erro em current_candles: {e}")

def main():
    """Função principal do Main Worker Windows"""
    print("=" * 70)
    print("MAIN WORKER WINDOWS - SINCRONIZADOR AUTOMATICO")
    print("=" * 70)
    print()
    print("Workers que serão iniciados:")
    print("  - categories: a cada 1 hora")
    print("  - assets: a cada 30 minutos")
    print("  - candles: a cada 1 hora")
    print("  - current_candles: a cada 1 minuto (Windows otimizado)")
    print()
    print("Pressione Ctrl+C para parar")
    print("=" * 70)
    
    logger.info("Iniciando Main Worker Windows...")
    
    # Criar scheduler
    scheduler = BlockingScheduler()
    
    # Adicionar jobs
    scheduler.add_job(
        run_categories,
        trigger=IntervalTrigger(seconds=3600),  # 1 hora
        id='categories',
        name='Sincronização de Categorias',
        max_instances=1,
        replace_existing=True
    )
    
    scheduler.add_job(
        run_assets,
        trigger=IntervalTrigger(seconds=1800),  # 30 minutos
        id='assets',
        name='Sincronização de Ativos',
        max_instances=1,
        replace_existing=True
    )
    
    scheduler.add_job(
        run_candles,
        trigger=IntervalTrigger(seconds=3600),  # 1 hora
        id='candles',
        name='Sincronização de Candles Históricos',
        max_instances=1,
        replace_existing=True
    )
    
    scheduler.add_job(
        run_current_candles,
        trigger=IntervalTrigger(seconds=60),  # 1 minuto
        id='current_candles',
        name='Sincronização de Candles Atuais (Windows)',
        max_instances=1,
        replace_existing=True
    )
    
    # Executar jobs imediatamente na primeira vez
    logger.info("Executando jobs iniciais...")
    run_categories()
    run_assets()
    run_candles()
    run_current_candles()
    
    logger.info("Workers ativos:")
    logger.info("  - categories: a cada 3600s")
    logger.info("  - assets: a cada 1800s")
    logger.info("  - candles: a cada 3600s")
    logger.info("  - current_candles: a cada 60s")
    
    try:
        scheduler.start()
    except KeyboardInterrupt:
        logger.info("Parando Main Worker Windows...")
        scheduler.shutdown()
        print("\n" + "=" * 70)
        print("MAIN WORKER WINDOWS PARADO!")
        print("=" * 70)

if __name__ == '__main__':
    main()

