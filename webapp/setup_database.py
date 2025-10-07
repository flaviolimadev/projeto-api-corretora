"""
Script para criar tabelas no banco de dados
"""

import asyncio
import logging
from database.db import db_manager

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


async def setup_database():
    """Verificar e configurar banco de dados"""
    try:
        logger.info("Conectando ao banco de dados...")
        await db_manager.connect()
        logger.info("✅ Conectado com sucesso!")
        
        # Verificar se as tabelas existem
        logger.info("Verificando tabelas existentes...")
        
        try:
            categories = await db_manager.get_all_categories()
            logger.info(f"✅ Tabela 'categories' existe - {len(categories)} registros")
        except Exception as e:
            logger.warning(f"⚠️  Tabela 'categories' não existe ou está vazia: {e}")
        
        try:
            assets = await db_manager.get_all_assets()
            logger.info(f"✅ Tabela 'assets' existe - {len(assets)} registros")
        except Exception as e:
            logger.warning(f"⚠️  Tabela 'assets' não existe ou está vazia: {e}")
        
        try:
            current_candles = await db_manager.get_all_current_candles()
            logger.info(f"✅ Tabela 'current_candles' existe - {len(current_candles)} registros")
        except Exception as e:
            logger.warning(f"⚠️  Tabela 'current_candles' não existe ou está vazia: {e}")
        
        try:
            logs = await db_manager.get_recent_sync_logs(limit=10)
            logger.info(f"✅ Tabela 'sync_logs' existe - {len(logs)} registros recentes")
        except Exception as e:
            logger.warning(f"⚠️  Tabela 'sync_logs' não existe ou está vazia: {e}")
        
        logger.info("\n" + "="*60)
        logger.info("RESULTADO DA VERIFICAÇÃO:")
        logger.info("="*60)
        logger.info("Se você viu mensagens ✅ acima, as tabelas existem!")
        logger.info("Se você viu mensagens ⚠️, execute: prisma db push")
        logger.info("="*60)
        
        await db_manager.disconnect()
        logger.info("Desconectado do banco de dados")
        
    except Exception as e:
        logger.error(f"❌ Erro ao configurar banco de dados: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(setup_database())

