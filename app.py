"""
Main Flask application for AML/BSA Compliance Agent
"""

from flask import Flask, render_template, jsonify, request
from regulatory_sources import REGULATORY_SOURCES, REGULATION_CATEGORIES
from scraper import RegulatoryScraper
from ai_analyzer import ComplianceAnalyzer
from email_service import EmailService
import schedule
import threading
import time
from datetime import datetime
import os

app = Flask(__name__)

latest_updates = []
last_refresh = None

def run_daily_scan():
    """Main function to scan regulators and analyze updates"""
    global latest_updates, last_refresh
    
    print(f"\nStarting scan: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    scraper = RegulatoryScraper()
    analyzer = ComplianceAnalyzer()
    email_service = EmailService()
    
    updates_by_regulator = {}
    
    for regulator_code, config in REGULATORY_SOURCES.items():
        print(f"Fetching from {config['name']}...")
        updates = scraper.fetch_regulator_updates(config)
        
        if updates:
            updates_by_regulator[config['name']] = {
                'updates': updates,
                'type': config['type']
            }
            print(f"  Found {len(updates)} updates")
        
        time.sleep(2)
    
    print("\nAnalyzing with AI...")
    analyzed = analyzer.batch_analyze(updates_by_regulator)
    
    latest_updates = analyzed
    last_refresh = datetime.now()
    
    print("\nSending email...")
    email_service.send_daily_summary(analyzed)
    print("\nScan completed\n")

def schedule_daily_scans():
    """Schedule daily scans at 8 AM EST (13:00 UTC)"""
    schedule.every().day.at("13:00").do(run_daily_scan)
    
    while True:
        schedule.run_pending()
        time.sleep(60)

@app.route('/')
def index():
    """Render main dashboard"""
    return render_template('index.html', 
                         regulators=REGULATORY_SOURCES,
                         categories=REGULATION_CATEGORIES)

@app.route('/api/updates')
def get_updates():
    """API endpoint to get latest updates"""
    filters = {
        'regulator': request.args.get('regulator'),
        'type': request.args.get('type'),
        'category': request.args.get('category')
    }
    
    filtered_updates = latest_updates
    
    # Filter by regulator
    if filters['regulator'] and filters['regulator'] != 'all':
        filtered_updates = [u for u in filtered_updates if u['regulator'] == filters['regulator']]
    
    # Filter by category
    if filters['category'] and filters['category'] != 'all':
        filtered_updates = [u for u in filtered_updates 
                          if filters['category'] in u.get('categories', [])]
    
    return jsonify({
        'updates': filtered_updates,
        'last_refresh': last_refresh.isoformat() if last_refresh else None,
        'count': len(filtered_updates)
    })

@app.route('/api/refresh')
def manual_refresh():
    """Manually trigger a scan"""
    threading.Thread(target=run_daily_scan, daemon=True).start()
    return jsonify({'status': 'Scan initiated'})

if __name__ == '__main__':
    # This only runs locally, not on Render with gunicorn
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
