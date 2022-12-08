import requests
import random

with open("valid_proxies2.txt", "r") as f:
    proxies = f.read().split("\n")  


sites = [
    "http://books.toscrape.com/",
    "http://books.toscrape.com/catalogue/page-2.html"
]

counter = 0

for site in sites:
    try:
        proxy = random.choice(proxies)
        print(f'Using the proxy: {proxy}')
        res = requests.get(site, proxies={
            "http": proxy,
            "https": proxy
        })

        print(res.status_code)
        print(res.text)

    except:
        print("Failed")

    finally:
        counter += 1