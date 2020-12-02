from modules import KafkaScanner


def run():
    scanner = KafkaScanner()
    scanner.scan_for_message()

if __name__ == "__main__":
    run()