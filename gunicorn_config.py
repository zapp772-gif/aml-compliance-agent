"""
Gunicorn configuration for background tasks
"""
import threading

def post_worker_init(worker):
    """
    Called just after a worker has been initialized.
    """
    from app import run_daily_scan, schedule_daily_scans
    
    print(f"Worker {worker.pid}: Starting background tasks immediately...")
    
    # Start scan immediately (no delay)
    threading.Thread(target=run_daily_scan, daemon=True).start()
    
    # Start scheduler
    threading.Thread(target=schedule_daily_scans, daemon=True).start()
    
    print(f"Worker {worker.pid}: Background tasks running")

# Gunicorn config
bind = "0.0.0.0:10000"
workers = 1
timeout = 300
worker_class = "sync"
