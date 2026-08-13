#!/usr/bin/env python3
import argparse
import logging
import os
import sys
import time

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from app.main import create_app
from app.services.automation import process_due_price_changes

logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"), format="%(asctime)s %(levelname)s %(name)s %(message)s")


def main():
    parser = argparse.ArgumentParser(description="Processa alterações de preço vencidas")
    parser.add_argument("--max-retries", type=int, default=int(os.getenv("MAX_RETRIES", "3")))
    parser.add_argument("--loop", action="store_true", help="Executa continuamente")
    parser.add_argument("--interval", type=int, default=int(os.getenv("WORKER_INTERVAL_SECONDS", "60")))
    args = parser.parse_args()
    app = create_app()
    while True:
        with app.app_context():
            result = process_due_price_changes(max_retries=args.max_retries)
            logging.getLogger(__name__).info("price_change_worker_finished", extra=result)
        if not args.loop:
            return 1 if result["failed"] else 0
        time.sleep(max(args.interval, 5))


if __name__ == "__main__":
    raise SystemExit(main())
