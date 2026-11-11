import csv
import json
from datetime import datetime


def generate_csv_report(
    ips,
    hashes,
    ip_results,
    hash_results,
    output_path,
):

    with open(output_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        writer.writerow(["Type", "Value", "Result", "Date"])

        for ip in ips:
            stats = ip_results.get(ip) or {}

            malicious = stats.get("malicious", 0)
            suspicious = stats.get("suspicious", 0)
            harmless = stats.get("harmless", 0)
            undetected = stats.get("undetected", 0)

            writer.writerow(["IP", ip, malicious, suspicious, harmless, undetected])

        for hash_value in hashes:

            stats = hash_results.get(hash_value or {})
            malicious = stats.get("malicious", 0)
            suspicious = stats.get("suspicious", 0)
            harmless = stats.get("harmless", 0)
            undetected = stats.get("undetected", 0)
            writer.writerow(
                ["HASH", hash_value, malicious, suspicious, harmless, undetected]
            )


def generate_json_report(ips, hashes, ip_result, hash_result, output_path):
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data = []

    for ip in ips:
        record = {"type": "IP", "value": ip, "result": ip_result.get(ip), "date": date}
        data.append(record)

    for hash_value in hashes:
        record = {
            "type": "HASH",
            "value": hash_value,
            "result": hash_result.get(hash_value),
            "date": date,
        }
        data.append(record)

    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)
