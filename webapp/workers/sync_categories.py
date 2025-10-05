"""
Worker para sincronizar categorias
"""

import asyncio
import logging
import time
from datetime import datetime
from typing import Dict, Any
import requests

from database.db import db_manager

logger = logging.getLogger(__name__)


async def sync_categories() -> Dict[str, Any]:
    """
    Sincronizar categorias do endpoint /api/categories para o banco de dados
    """
    log_id = None
    start_time = time.time()
    
    try:
        # Criar log de sincronização
        log = await db_manager.create_sync_log({
            'type': 'categories',
            'status': 'running',
            'startedAt': datetime.now()
        })
        log_id = log.id if log else None
        
        logger.info("🔄 Iniciando sincronização de categorias...")
        
        # Buscar categorias da API
        response = requests.get('http://localhost:5000/api/categories', timeout=10)
        if response.status_code != 200:
            raise Exception(f"API returned status {response.status_code}")
        
        data = response.json()
        categories = data['categories']
        
        inserted_count = 0
        errors = []
        
        # Inserir/atualizar cada categoria
        for category_key, category_info in categories.items():
            try:
                category_data = {
                    'key': category_key,
                    'name': category_info['name'],
                    'description': category_info['description'],
                    'icon': category_info['icon'],
                    'exchanges': category_info['exchanges'],
                    'timeframes': category_info['timeframes']
                }
                
                await db_manager.upsert_category(category_data)
                inserted_count += 1
                logger.info(f"✅ Sincronizada categoria: {category_key}")
                
            except Exception as e:
                error_msg = f"Erro ao sincronizar {category_key}: {e}"
                logger.error(error_msg)
                errors.append(error_msg)
        
        duration = time.time() - start_time
        
        # Atualizar log
        if log_id:
            await db_manager.update_sync_log(log_id, {
                'status': 'success' if not errors else 'partial',
                'itemsCount': inserted_count,
                'errorMsg': ' | '.join(errors) if errors else None,
                'duration': duration,
                'finishedAt': datetime.now()
            })
        
        logger.info(f"✅ Sincronização de categorias concluída: {inserted_count} categorias em {duration:.2f}s")
        
        return {
            'success': True,
            'itemsCount': inserted_count,
            'duration': duration,
            'errors': errors
        }
        
    except Exception as e:
        duration = time.time() - start_time
        error_msg = f"Erro na sincronização de categorias: {e}"
        logger.error(f"❌ {error_msg}")
        
        # Atualizar log com erro
        if log_id:
            await db_manager.update_sync_log(log_id, {
                'status': 'error',
                'errorMsg': str(e),
                'duration': duration,
                'finishedAt': datetime.now()
            })
        
        return {
            'success': False,
            'error': str(e),
            'duration': duration
        }


async def sync_categories_worker():
    """Worker que sincroniza categorias periodicamente"""
    interval = 3600  # 1 hora
    
    logger.info(f"🚀 Worker de sincronização de categorias iniciado (intervalo: {interval}s)")
    
    while True:
        try:
            await sync_categories()
        except Exception as e:
            logger.error(f"Erro no worker de categorias: {e}")
        
        await asyncio.sleep(interval)


if __name__ == "__main__":
    async def main():
        await db_manager.connect()
        await sync_categories()
        await db_manager.disconnect()
    
    asyncio.run(main())
