import argparse
from modules.port_scanner import PortScanner
from modules.brute_forcer import BruteForcer
from modules.vulnerability_scanner import VulnerabilityScanner
from utils.reporter import generate_report

def main():
    parser = argparse.ArgumentParser(description="Penetration Testing Toolkit")
    subparsers = parser.add_subparsers(dest='command', required=True)
    
    # Port scanner subcommand
    scan_parser = subparsers.add_parser('scan', help='Port scanning')
    scan_parser.add_argument('target', help='Target IP or hostname')
    scan_parser.add_argument('-p', '--ports', help='Port range (e.g., 1-1000)')
    scan_parser.add_argument('-t', '--threads', type=int, default=100, help='Number of threads')
    
    # Brute force subcommand
    brute_parser = subparsers.add_parser('brute', help='Brute force attacks')
    brute_parser.add_argument('target', help='Target service (http://example.com or ssh://host:22)')
    brute_parser.add_argument('-u', '--username', help='Username to test')
    brute_parser.add_argument('-w', '--wordlist', help='Path to wordlist file')
    brute_parser.add_argument('-t', '--threads', type=int, default=10, help='Number of threads')
    
    # Vulnerability scanner subcommand
    vuln_parser = subparsers.add_parser('vulnscan', help='Vulnerability scanning')
    vuln_parser.add_argument('target', help='Target URL (e.g., http://example.com)')
    
    args = parser.parse_args()
    
    if args.command == 'scan':
        ports = range(*map(int, args.ports.split('-'))) if args.ports else None
        scanner = PortScanner(args.target, ports, args.threads)
        open_ports = scanner.scan()
        generate_report('port_scan', {'target': args.target, 'open_ports': open_ports})
        
    elif args.command == 'brute':
        forcer = BruteForcer(args.target, args.username, args.wordlist, args.threads)
        forcer.run()
        
    elif args.command == 'vulnscan':
        scanner = VulnerabilityScanner(args.target)
        vulnerabilities = scanner.scan()
        generate_report('vulnerability_scan', {
            'target': args.target,
            'vulnerabilities': vulnerabilities
        })

if __name__ == '__main__':
    main()
