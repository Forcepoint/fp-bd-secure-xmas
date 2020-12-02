import time
from modules import DBScanner


def run():
    scanner = DBScanner()
    scanner.scan_for_events()

if __name__ == "__main__":
    run()