#pip install shodan
import shodan
import json
# Shodan API 키를 설정합니다.
SHODAN_API_KEY = 'Z2soDBnFLLNRKZsamG9hUQLtBBh9GTwH'
api = shodan.Shodan(SHODAN_API_KEY)

# 웹캠을 검색합니다.
query = 'a'

results = api.search(query)

print(f"총 결과 : {results['total']}")

try:
    for match in results['matches'][:2]:
        #print(json.dumps(result, indent=4))
        print(f"IP정보: {match['ip_str']}")
        print(f"포트정보: {match['port']}")
        print(f"Org: {match.get('org', 'N/A')}")
        print(f"Location: {match['location']['country_name']}")
        print(f"Hostnames: {', '.join(match['hostnames']) if match['hostnames'] else 'N/A'}")
except shodan.APIError as e:
    print(f"오류: {e}")