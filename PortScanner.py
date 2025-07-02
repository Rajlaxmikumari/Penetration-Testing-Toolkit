import socket
from concurrent.futures import ThreadPoolExecutor
from utils.logger import setup_logger

logger = setup_logger('port_scanner')

class PortScanner:
    def __init__(self, target, ports=None, threads=100, timeout=1):
        self.target = target
        self.ports = ports or range(1, 1025)  # Default to common ports
        self.threads = threads
        self.timeout = timeout
        self.open_ports = []
        
    def scan_port(self, port):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(self.timeout)
                result = s.connect_ex((self.target, port))
                if result == 0:
                    self.open_ports.append(port)
                    try:
                        service = socket.getservbyport(port)
                    except:
                        service = "unknown"
                    logger.info(f"Port {port} ({service}) is open")
        except Exception as e:
            logger.error(f"Error scanning port {port}: {e}")
    
    def scan(self):
        logger.info(f"Starting scan on {self.target}")
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            executor.map(self.scan_port, self.ports)
        
        logger.info(f"Scan completed. Open ports: {sorted(self.open_ports)}")
        return self.open_ports
