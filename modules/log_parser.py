import re
import ipaddress


def parse_logs(file_path):
    ips = set()
    hashes = set()
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            result_ips = re.findall(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", line)
            result_hashes = re.findall(r"\b[a-fA-F0-9]{64}\b", line)
            ips.update(result_ips)
            hashes.update(result_hashes)

    valid_ips = set()
    for ip in ips:
        try:
            ipaddress.IPv4Address(ip)
            valid_ips.add(ip)
        except ValueError:
            print(f"Invalid IP: {ip}")

    return list(valid_ips), list(hashes)
