import ipaddress
import re

class Detector:
    def __init__(self, data):
        self.data = data

    def data_detector(self):
        data_type = []
        unknown = []
        domain_endings = (".com", ".org", ".net", ".edu", ".gov", ".io", ".co", ".us", ".uk", ".ca", ".de", ".jp", ".fr", ".au", ".ru", ".ch", ".it", ".nl", ".se", ".no", ".es")
        for item in self.data:
            if item.endswith(domain_endings):
                data_type.append({"type": "domain","value": item})
            elif re.fullmatch(r"[a-fA-F0-9]{64}", item):
                data_type.append({"type": "sha256","value": item})
            elif re.fullmatch(r"[a-fA-F0-9]{40}", item):
                data_type.append({"type": "sha1","value": item})
            elif re.fullmatch(r"[a-fA-F0-9]{32}", item):
                data_type.append({"type": "md5","value": item})
            else:
                try:
                    ip = ipaddress.ip_address(item)
                    if ip.version == 4:
                        data_type.append({"type": "ipv4","value": item})
                    elif ip.version == 6:
                        data_type.append({"type": "ipv6","value": item})
                except ValueError:
                    unknown.append({"unknownData": item})

        return data_type, unknown     