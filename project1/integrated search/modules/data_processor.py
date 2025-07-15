# modules/data_processor.py

def map_to_owasp(description):
    desc_lower = description.lower()
    categories = []

    if "sql injection" in desc_lower or "command injection" in desc_lower or "injection" in desc_lower:
        categories.append("A03:2021-Injection\n")
    if "cryptographic" in desc_lower or "crypto" in desc_lower:
        categories.append("A02:2021-Cryptographic Failures\n")
    if "authentication" in desc_lower or "auth bypass" in desc_lower or "auth" in desc_lower:
        categories.append("A07:2021-Identification and Authentication Failures\n")
    if "xss" in desc_lower or "cross-site scripting" in desc_lower:
        categories.append("A03:2021-Injection\n")  # XSS는 Injection의 하위분류로 통합
    if "access control" in desc_lower or "authorization" in desc_lower or "idor" in desc_lower:
        categories.append("A01:2021-Broken Access Control\n")
    if "ssrf" in desc_lower or "server-side request forgery" in desc_lower:
        categories.append("A10:2021-Server-Side Request Forgery\n")
    if "deserialization" in desc_lower:
        categories.append("A08:2021-Software and Data Integrity Failures\n")
    if "security misconfiguration" in desc_lower or "config" in desc_lower:
        categories.append("A05:2021-Security Misconfiguration\n")
    if "vulnerable and outdated components" in desc_lower or "dependency" in desc_lower:
        categories.append("A06:2021-Vulnerable and Outdated Components\n")
    if "insecure design" in desc_lower:
        categories.append("A04:2021-Insecure Design\n")
     
    if not categories:
        categories.append("Other")

    return categories


def process_results(results):
    for item in results:
        if item.get('source') == 'NVD':
            description = item.get("description_en", "") or item.get("description_ko", "")
            item['owasp_category'] = map_to_owasp(description)
        else:
            item['owasp_category'] = ['N/A']  # 해커뉴스는 리스트 형태로 맞춤
    return results
