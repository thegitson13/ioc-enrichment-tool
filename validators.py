import ipaddress
import requests
import logging

class Validators:
    def __init__(self, data):
        self.data = data

    def validate_ip(self):
        ip_data = []
        
        for item in self.data:
            ip = item["value"]
            ip_version = item["type"]
            if ip_version in ["ipv4", "ipv6"]:
                ip_obj = ipaddress.ip_address(ip)
                if ip_obj.is_private:
                    ip_data.append({"type": ip_version, "value": ip, "valid": False, "reason": "Private IP address"})
                elif ip_obj.is_loopback:
                    ip_data.append({"type": ip_version, "value": ip, "valid": False, "reason": "Loopback IP address"})
                elif ip_obj.is_multicast:
                    ip_data.append({"type": ip_version, "value": ip, "valid": False, "reason": "Multicast IP address"})
                else:
                    ip_data.append({"type": ip_version, "value": ip, "valid": True})

        return ip_data

    
    def api_validator(self, ip_data, api_key, url_ip):
        full_ip_data = {}

        for item in ip_data:
            ip = item["value"]
            if item["valid"]:
                querystring = {
                    'ipAddress': ip,
                    'maxAgeInDays': '90'
                }

                headers = {
                    'Accept': 'application/json',
                    'Key': api_key
                }

                try:
                    response = requests.get(url_ip, headers=headers, params=querystring)
                    if response.status_code == 200:
                        data = response.json()["data"]
                        full_ip_data[ip] = {
                            "ipAddress": data.get("ipAddress"),
                            "isPublic": data.get("isPublic"),
                            "abuseScore": data.get("abuseConfidenceScore"),
                            "countryCode": data.get("countryCode"),
                            "isp": data.get("isp"),
                            "domain": data.get("domain"),
                            "totalReports": data.get("totalReports"),
                            "isTor": data.get("isTor")
                        }
                    else:
                        logging.error(f"Error checking IP {ip}: {response.status_code}")

                except requests.RequestException as error:
                    logging.error(f"API request failed for {ip}: {error}")
                    continue

            else:
                continue

        for values in ip_data:
            if values["value"] not in full_ip_data:
                full_ip_data[values["value"]] = {
                    "ipAddress": values["value"],
                    "IPVersion": values["type"],
                    "valid": values["valid"],
                    "addressType": values["reason"]
                }
        
        return full_ip_data

    def data_combiner(self, api_data, primary_data, unknown_data):
        combined_data = {}
        combined_data["ips"] = api_data
        all_domain = []
        all_hashes = []
        
        for item in primary_data:
            if item["type"] == "domain":
                domain = {
                    "type": item["type"],
                    "value": item["value"]
                }
                all_domain.append(domain)

            if item["type"] in ["md5", "sha1", "sha256"]:
                hash_data = {
                    "type": item["type"],
                    "value": item["value"]
                }
                all_hashes.append(hash_data)

        combined_data["domain"] = all_domain
        combined_data["hash"] = all_hashes
        combined_data["unknown/invalid"] = unknown_data
        return combined_data