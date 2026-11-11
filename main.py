from modules.log_parser import *
from modules.report_generator import *
from modules.virustotal import *

import argparse
import logging
from pathlib import Path
import os

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("-log-file", required=True)
    parser.add_argument("-api-key", default=os.getenv("VT_API_KEY"))
    parser.add_argument("-output", default="output/report.csv")
    parser.add_argument("-format", choices=["csv", "json"], default="csv")

    args = parser.parse_args()

    # Настройка логирования
    log_dir = Path(args.output).parent
    log_dir.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        filename=str(log_dir / "logscan.log"),
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        encoding="utf-8",
    )

    logging.info("LogScan started")
    logging.info("Анализ файла: %s", args.log_file)

    # Парсинг логов
    # ips, hashes = parse_logs(args.log_file)
    # Парсинг логов
    try:
        ips, hashes = parse_logs(args.log_file)

    except FileNotFoundError:
        logging.error("Файл не найден: %s", args.log_file)
        raise SystemExit(1)
    except PermissionError:
        logging.error("Нет доступа к файлу: %s", args.log_file)
        raise SystemExit(1)

    logging.info("Найдено IP-адресов: %s", len(ips))
    logging.info("Найдено SHA256: %s", len(hashes))

    ip_result = {}
    hash_result = {}

    # Проверка VirusTotal или Mock
    if args.api_key:
        logging.info("VirusTotal API mode")

        for ip in ips:
            ip_result[ip] = check_ip(ip, args.api_key)

        for hash_value in hashes:
            hash_result[hash_value] = check_hash(hash_value, args.api_key)

    else:
        logging.info("Mock mode")

        for ip in ips:
            ip_result[ip] = mock_check_ip(ip)

        for hash_value in hashes:
            hash_result[hash_value] = mock_check_hash(hash_value)

    # Генерация отчётов
    try:
        if args.format == "csv":
            generate_csv_report(ips, hashes, ip_result, hash_result, args.output)

        elif args.format == "json":
            generate_json_report(ips, hashes, ip_result, hash_result, args.output)
    except OSError as error:
        logging.error("Ошибка сохранения отчёта: %s", error)
        raise SystemExit(1)

    logging.info("Отчёт сохранён: %s", args.output)
    logging.info("LogScan finished")


if __name__ == "__main__":
    main()
