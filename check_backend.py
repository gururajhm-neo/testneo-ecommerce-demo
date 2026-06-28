import sys
import urllib.request

url = 'http://127.0.0.1:9000/health'
try:
    with urllib.request.urlopen(url, timeout=5) as response:
        body = response.read().decode('utf-8', 'ignore')
        print('OK', response.status, body)
except Exception as exc:
    print('ERR', str(exc))
    sys.exit(1)
