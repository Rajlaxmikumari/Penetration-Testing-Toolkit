from datetime import datetime
import json

def generate_report(scan_type, data):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"report_{scan_type}_{timestamp}.json"
    
    report = {
        'scan_type': scan_type,
        'timestamp': timestamp,
        'data': data
    }
    
    with open(filename, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"Report generated: {filename}")
