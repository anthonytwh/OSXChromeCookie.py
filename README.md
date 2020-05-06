# OSXChromeCookie.py

Simple module to extract stored Chrome cookies used in the browser for sessions in Python scripts. This works with pre-authenticated browser sessions and can bypass some single sign-on(SSO) services/redirects. 

## To use

```
import requests
import OSXChromeCookie

URL = 'google.com'
s = requests.Session()
cookies = OSXChromeCookie.chrome_cookies(URL)
s.get(url, cookies = cookies)
```

Forked from https://gist.github.com/n8henrie/8715089.
