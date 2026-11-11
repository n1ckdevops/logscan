import requests


def check_ip(ip, api_key):
    url = f"https://www.virustotal.com/api/v3/ip_addresses/{ip}"
    headers = {"x-apikey": api_key}
    try:
        response = requests.get(url, headers=headers, timeout=10)
    except requests.exceptions.Timeout:
        return None
    except requests.exceptions.ConnectionError:
        return None
    if response.status_code == 200:
        return extract_stats(response.json())
    else:
        return None


def check_hash(hash_value, api_key):
    url = f"https://www.virustotal.com/api/v3/files/{hash_value}"
    headers = {"x-apikey": api_key}
    try:
        response = requests.get(url, headers=headers, timeout=10)
    except requests.exceptions.Timeout:
        return None
    except requests.exceptions.ConnectionError:
        return None
    if response.status_code == 200:
        return extract_stats(response.json())
    else:
        return None


def mock_check_ip(ip):
    check_result = {"malicious": 2, "suspicious": 1, "harmless": 65, "undetected": 10}
    return check_result


def mock_check_hash(hash_value):
    check_result = {"malicious": 2, "suspicious": 1, "harmless": 65, "undetected": 10}
    return check_result


def extract_stats(data):
    if data is None:
        return None

    data_block = data.get("data") or {}

    attributes = data_block.get("attributes") or {}

    stats = attributes.get("last_analysis_stats") or None

    return stats
