import logging
from colorama import init, Fore, Style

init(autoreset=True)

def setup_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    
    class ColoredFormatter(logging.Formatter):
        def format(self, record):
            if record.levelno == logging.DEBUG:
                prefix = Fore.CYAN + "[*] "
            elif record.levelno == logging.INFO:
                prefix = Fore.GREEN + "[+] "
            elif record.levelno == logging.WARNING:
                prefix = Fore.YELLOW + "[!] "
            elif record.levelno == logging.ERROR:
                prefix = Fore.RED + "[-] "
            elif record.levelno == logging.CRITICAL:
                prefix = Fore.RED + Style.BRIGHT + "[CRITICAL] "
            else:
                prefix = ""
            
            return prefix + record.getMessage()
    
    formatter = ColoredFormatter()
    ch.setFormatter(formatter)
    
    logger.addHandler(ch)
    return logger
