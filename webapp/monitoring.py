"""
Monitoring and metrics collection for TradingView API
"""

import time
import psutil
import logging
from datetime import datetime, timedelta
from flask import jsonify
from collections import defaultdict, deque
import threading

logger = logging.getLogger(__name__)

class MetricsCollector:
    """Collect and store application metrics"""
    
    def __init__(self, max_history=1000):
        self.max_history = max_history
        self.metrics = {
            'requests': deque(maxlen=max_history),
            'response_times': deque(maxlen=max_history),
            'errors': deque(maxlen=max_history),
            'websocket_connections': deque(maxlen=max_history),
            'database_queries': deque(maxlen=max_history),
            'cache_hits': deque(maxlen=max_history),
            'cache_misses': deque(maxlen=max_history)
        }
        self.counters = defaultdict(int)
        self.start_time = time.time()
        self.lock = threading.Lock()
    
    def record_request(self, endpoint, method, status_code, response_time):
        """Record API request metrics"""
        with self.lock:
            self.metrics['requests'].append({
                'timestamp': datetime.now().isoformat(),
                'endpoint': endpoint,
                'method': method,
                'status_code': status_code,
                'response_time': response_time
            })
            self.counters[f'requests_{status_code}'] += 1
            self.counters['total_requests'] += 1
    
    def record_error(self, error_type, error_message, endpoint=None):
        """Record error metrics"""
        with self.lock:
            self.metrics['errors'].append({
                'timestamp': datetime.now().isoformat(),
                'error_type': error_type,
                'error_message': error_message,
                'endpoint': endpoint
            })
            self.counters['total_errors'] += 1
    
    def record_websocket_connection(self, action, connection_id):
        """Record WebSocket connection metrics"""
        with self.lock:
            self.metrics['websocket_connections'].append({
                'timestamp': datetime.now().isoformat(),
                'action': action,  # 'connect' or 'disconnect'
                'connection_id': connection_id
            })
            if action == 'connect':
                self.counters['active_websocket_connections'] += 1
            else:
                self.counters['active_websocket_connections'] = max(0, 
                    self.counters['active_websocket_connections'] - 1)
    
    def record_database_query(self, query_type, execution_time, success=True):
        """Record database query metrics"""
        with self.lock:
            self.metrics['database_queries'].append({
                'timestamp': datetime.now().isoformat(),
                'query_type': query_type,
                'execution_time': execution_time,
                'success': success
            })
            self.counters['total_db_queries'] += 1
            if not success:
                self.counters['failed_db_queries'] += 1
    
    def record_cache_event(self, event_type, key=None):
        """Record cache hit/miss events"""
        with self.lock:
            if event_type == 'hit':
                self.metrics['cache_hits'].append({
                    'timestamp': datetime.now().isoformat(),
                    'key': key
                })
                self.counters['cache_hits'] += 1
            elif event_type == 'miss':
                self.metrics['cache_misses'].append({
                    'timestamp': datetime.now().isoformat(),
                    'key': key
                })
                self.counters['cache_misses'] += 1
    
    def get_system_metrics(self):
        """Get system resource metrics"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            return {
                'cpu_percent': cpu_percent,
                'memory': {
                    'total': memory.total,
                    'available': memory.available,
                    'percent': memory.percent,
                    'used': memory.used
                },
                'disk': {
                    'total': disk.total,
                    'used': disk.used,
                    'free': disk.free,
                    'percent': (disk.used / disk.total) * 100
                }
            }
        except Exception as e:
            logger.error(f"Error getting system metrics: {e}")
            return {}
    
    def get_metrics_summary(self, hours=1):
        """Get metrics summary for the last N hours"""
        with self.lock:
            cutoff_time = datetime.now() - timedelta(hours=hours)
            
            # Filter recent metrics
            recent_requests = [
                req for req in self.metrics['requests']
                if datetime.fromisoformat(req['timestamp']) > cutoff_time
            ]
            
            recent_errors = [
                err for err in self.metrics['errors']
                if datetime.fromisoformat(err['timestamp']) > cutoff_time
            ]
            
            # Calculate statistics
            response_times = [req['response_time'] for req in recent_requests]
            avg_response_time = sum(response_times) / len(response_times) if response_times else 0
            
            status_codes = defaultdict(int)
            for req in recent_requests:
                status_codes[req['status_code']] += 1
            
            # Error rate
            total_requests = len(recent_requests)
            error_requests = len([req for req in recent_requests if req['status_code'] >= 400])
            error_rate = (error_requests / total_requests * 100) if total_requests > 0 else 0
            
            return {
                'period_hours': hours,
                'total_requests': total_requests,
                'avg_response_time_ms': round(avg_response_time * 1000, 2),
                'error_rate_percent': round(error_rate, 2),
                'status_codes': dict(status_codes),
                'total_errors': len(recent_errors),
                'active_websocket_connections': self.counters['active_websocket_connections'],
                'cache_hit_rate': self._calculate_cache_hit_rate(),
                'uptime_seconds': time.time() - self.start_time
            }
    
    def _calculate_cache_hit_rate(self):
        """Calculate cache hit rate percentage"""
        total_cache_events = self.counters['cache_hits'] + self.counters['cache_misses']
        if total_cache_events == 0:
            return 0
        return round((self.counters['cache_hits'] / total_cache_events) * 100, 2)
    
    def get_detailed_metrics(self):
        """Get detailed metrics for monitoring dashboard"""
        system_metrics = self.get_system_metrics()
        summary = self.get_metrics_summary(hours=1)
        
        return {
            'timestamp': datetime.now().isoformat(),
            'system': system_metrics,
            'application': summary,
            'counters': dict(self.counters),
            'recent_errors': list(self.metrics['errors'])[-10:],  # Last 10 errors
            'recent_requests': list(self.metrics['requests'])[-20:]  # Last 20 requests
        }

# Global metrics collector instance
metrics_collector = MetricsCollector()

def get_metrics_endpoint():
    """Flask endpoint for metrics"""
    try:
        metrics = metrics_collector.get_detailed_metrics()
        return jsonify(metrics)
    except Exception as e:
        logger.error(f"Error getting metrics: {e}")
        return jsonify({'error': str(e)}), 500

def get_health_endpoint():
    """Enhanced health check with metrics"""
    try:
        system_metrics = metrics_collector.get_system_metrics()
        summary = metrics_collector.get_metrics_summary(hours=1)
        
        # Determine health status
        health_status = 'healthy'
        issues = []
        
        # Check system resources
        if system_metrics.get('cpu_percent', 0) > 90:
            health_status = 'warning'
            issues.append('High CPU usage')
        
        if system_metrics.get('memory', {}).get('percent', 0) > 90:
            health_status = 'warning'
            issues.append('High memory usage')
        
        if system_metrics.get('disk', {}).get('percent', 0) > 90:
            health_status = 'warning'
            issues.append('High disk usage')
        
        # Check application metrics
        if summary.get('error_rate_percent', 0) > 10:
            health_status = 'warning'
            issues.append('High error rate')
        
        if summary.get('avg_response_time_ms', 0) > 5000:
            health_status = 'warning'
            issues.append('Slow response times')
        
        return jsonify({
            'status': health_status,
            'timestamp': datetime.now().isoformat(),
            'uptime_seconds': summary.get('uptime_seconds', 0),
            'issues': issues,
            'metrics': {
                'requests_last_hour': summary.get('total_requests', 0),
                'avg_response_time_ms': summary.get('avg_response_time_ms', 0),
                'error_rate_percent': summary.get('error_rate_percent', 0),
                'active_connections': summary.get('active_websocket_connections', 0),
                'cache_hit_rate': summary.get('cache_hit_rate', 0)
            },
            'system': {
                'cpu_percent': system_metrics.get('cpu_percent', 0),
                'memory_percent': system_metrics.get('memory', {}).get('percent', 0),
                'disk_percent': system_metrics.get('disk', {}).get('percent', 0)
            }
        })
        
    except Exception as e:
        logger.error(f"Error in health check: {e}")
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500
