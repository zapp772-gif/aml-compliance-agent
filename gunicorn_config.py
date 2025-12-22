"""
Gunicorn configuration for background tasks
"""
import threading
import time

def post_worker_init(worker):
    """
    Called just after a worker has been initialized.
    This is the proper place to start background tasks.
    """
    from app import run_daily_scan, schedule_daily_scans
    
    print(f"Worker {worker.pid}: Initializing background tasks...")
    
    # Delay initial scan to let worker fully initialize
    def delayed_scan():
        time.sleep(15)
        print(f"Worker {worker.pid}: Starting initial scan...")
        run_daily_scan()
    
    # Start delayed scan
    threading.Thread(target=delayed_scan, daemon=True).start()
    
    # Start scheduler
    threading.Thread(target=schedule_daily_scans, daemon=True).start()
    
    print(f"Worker {worker.pid}: Background tasks scheduled")

# Gunicorn config
bind = "0.0.0.0:10000"
workers = 1
timeout = 120
worker_class = "sync"
