import bs4
import time
import requests
import json
import os
import datetime
import itertools

from bs4 import BeautifulSoup as soup
from twilio.rest import Client
from itertools import zip_longest

account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)

memory_urls = [
    "https://www.memoryexpress.com/Products/MX00114927",
    "https://www.memoryexpress.com/Products/MX00114926",
    "https://www.memoryexpress.com/Products/MX00114925",
    "https://www.memoryexpress.com/Products/MX00115014",
    "https://www.memoryexpress.com/Products/MX00114970",
    "https://www.memoryexpress.com/Products/MX00114818",
    "https://www.memoryexpress.com/Products/MX00115013",
    "https://www.memoryexpress.com/Products/MX00114924",
    "https://www.memoryexpress.com/Products/MX00114888",
#3070
    "https://www.memoryexpress.com/Products/MX00114408",
    "https://www.memoryexpress.com/Products/MX00114566",
    "https://www.memoryexpress.com/Products/MX00114605",
    "https://www.memoryexpress.com/Products/MX00114407",
    "https://www.memoryexpress.com/Products/MX00114785"
]

memory_headers = {
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
}

newegg_urls = [
    "https://www.newegg.ca/evga-geforce-rtx-3060-ti-08g-p5-3663-kr/p/N82E16814487535",
    "https://www.newegg.ca/evga-geforce-rtx-3060-ti-08g-p5-3667-kr/p/N82E16814487537",
    "https://www.newegg.ca/gigabyte-geforce-rtx-3060-ti-gv-n306teagle-oc-8gd/p/N82E16814932378",
    "https://www.newegg.ca/gigabyte-geforce-rtx-3060-ti-gv-n306teagle-8gd/p/N82E16814932379",
    "https://www.newegg.ca/gigabyte-geforce-rtx-3060-ti-gv-n306tgamingoc-pro-8gd/p/N82E16814932376",
    "https://www.newegg.ca/gigabyte-geforce-rtx-3060-ti-gv-n306tgaming-oc-8gd/p/N82E16814932377",
    "https://www.newegg.ca/msi-geforce-rtx-3060-ti-rtx-3060-ti-ventus-2x-oc/p/N82E16814137612",
    "https://www.newegg.ca/zotac-geforce-rtx-3060-ti-zt-a30610h-10m/p/N82E16814500507",
    "https://www.newegg.ca/zotac-geforce-rtx-3060-ti-zt-a30610e-10m/p/N82E16814500506",
    "https://www.newegg.ca/asus-geforce-rtx-3060-ti-ko-rtx3060ti-o8g-gaming/p/N82E16814126474",
#3070
    "https://www.newegg.ca/msi-geforce-rtx-3070-rtx-3070-ventus-2x/p/N82E16814137605",
    "https://www.newegg.ca/asus-geforce-rtx-3070-dual-rtx3070-8g/p/N82E16814126460",
    "https://www.newegg.ca/gigabyte-geforce-rtx-3070-gv-n3070eagle-8gd/p/N82E16814932344",
    "https://www.newegg.ca/zotac-geforce-rtx-3070-zt-a30700e-10p/p/N82E16814500501",
    "https://www.newegg.ca/evga-geforce-rtx-3070-08g-p5-3751-kr/p/N82E16814487528",
#bundles
    ""
]

newegg_headers = {
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'authority': 'www.newegg.ca',
    'method': 'GET',
    'path': '/api/HeaderPortals',
    'scheme': 'https',
    'accept': 'application/json, text/plain, */*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9'
}

cc_urls = [
    "https://www.canadacomputers.com/product_info.php?cPath=43_557_559&item_id=184759",
    "https://www.canadacomputers.com/product_info.php?cPath=43_557_559&item_id=185087",
    "https://www.canadacomputers.com/product_info.php?cPath=43_557_559&item_id=184760",
    "https://www.canadacomputers.com/product_info.php?cPath=43_557_559&item_id=185752",
    "https://www.canadacomputers.com/product_info.php?cPath=43_557_559&item_id=185751",
    "https://www.canadacomputers.com/product_info.php?cPath=43_557_559&item_id=185988",
    "https://www.canadacomputers.com/product_info.php?cPath=43_557_559&item_id=185987",
    "https://www.canadacomputers.com/product_info.php?cPath=43_557_559&item_id=185408",
    "https://www.canadacomputers.com/product_info.php?cPath=43_557_559&item_id=185407",
    "https://www.canadacomputers.com/product_info.php?cPath=43_557_559&item_id=185406",
    "https://www.canadacomputers.com/product_info.php?cPath=43_557_559&item_id=185405",
    "https://www.canadacomputers.com/product_info.php?cPath=43_557_559&item_id=185168",
#3070
    "https://www.canadacomputers.com/product_info.php?cPath=43_557_559&item_id=183101",
    "https://www.canadacomputers.com/product_info.php?cPath=43_557_559&item_id=183560",
    "https://www.canadacomputers.com/product_info.php?cPath=43_557_559&item_id=183500",
    "https://www.canadacomputers.com/product_info.php?cPath=43_557_559&item_id=183100"
]

cc_headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'keep-alive',
    'Host': 'www.canadacomputers.com',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'X-Requested-With': 'XMLHttpRequest'
}

bestbuy_urls = [
    "https://www.bestbuy.ca/en-ca/product/nvidia-geforce-rtx-3060-ti-8gb-gddr6-video-card/15166285",
    "https://www.bestbuy.ca/en-ca/product/zotac-geforce-rtx-3060-ti-twin-edge-8gb-gddr6-video-card/15178583",
#3070
    "https://www.bestbuy.ca/en-ca/product/nvidia-geforce-rtx-3070-8gb-gddr6-video-card-only-at-best-buy/15078017",
    "https://www.bestbuy.ca/en-ca/product/zotac-nvidia-geforce-rtx-3070-twin-edge-8gb-gddr6x-video-card/15000079",
    "https://www.bestbuy.ca/en-ca/product/evga-geforce-rtx-3070-xc3-black-8gb-gddr6-video-card/15081879"
]

bestbuy_headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
}

bh_urls = [
    "https://www.bhphotovideo.com/c/product/1606949-REG/gigabyte_gv_n306teagle_8gd_rtx_3060_ti_eagle.html",
    "https://www.bhphotovideo.com/c/product/1606948-REG/gigabyte_gv_n306teagle_oc_8gd_rtx_3060_ti_eagle.html",
    "https://www.bhphotovideo.com/c/product/1606947-REG/gigabyte_gv_n306tgaming_oc_8gd_rtx_3060_ti_gaming.html",
    "https://www.bhphotovideo.com/c/product/1606946-REG/gigabyte_gv_n306tgamingoc_pro_8gd_rtx_3060_ti_gaming.html",
    "https://www.bhphotovideo.com/c/product/1602755-REG/asus_dualrtx30708g_geforce_rtx_3070_8g.html",
#3070
    "https://www.bhphotovideo.com/c/product/1602755-REG/asus_dualrtx30708g_geforce_rtx_3070_8g.html",
    
]
bh_headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'
}

filename = "GPUlog.txt"
iteration = list(range(4, 8))
n = 8
zippered_urls = list(zip_longest(memory_urls, newegg_urls, cc_urls, bestbuy_urls, bh_urls))
# Use a generator with tuple constructor in a list comprehension statement to remove None
# tuple_urls = [tuple(xi for xi in x if xi is not None) for x in newlist]
# all_urls = [xi for x in tuple_urls for xi in x]
# or just extract items from tuples from list based on conditional statement
all_urls = [xi for x in zippered_urls for xi in x if xi is not None]
while True:
    for url in all_urls:
        try:
            if "memoryexpress" in url:
                headers = memory_headers
                headers['referer'] = url
                req = requests.get(url, headers)
                page_soup = soup(req.content, "html.parser")
                card_name = page_soup.find("div", {"class":"c-shth-page__main-content"}).h1.get_text()
                card_name = card_name.replace("\n", "")
                card_name = card_name.replace("\r", "")
                card_name = card_name.replace("  ", "")
                avail = page_soup.find('span', 'c-capr-inventory-store__availability').get_text()
                avail = avail.replace("\n", "")
                avail = avail.replace("\r", "")
                avail = avail.replace("  ", "")
                message = card_name + ": " + avail + " " + str(datetime.datetime.now())
                if avail != "Out of Stock":
                    instock = message + " " + url
                    client.messages.create(
                        to="+1123456789",
                        from_="+1123456789",
                        body=instock
                    )
                else:
                    print("memory " + message)
            elif "newegg" in url:
                headers = newegg_headers
                headers['referer'] = url
                req = requests.get(url, headers)
                page_soup = soup(req.content, "html.parser")
                card_name = page_soup.find("div", {"class":"product-wrap"}).h1.get_text()
                avail = page_soup.find("div", {"class":"product-inventory"}).strong.get_text()
                avail = avail.replace(" ", "")
                avail = avail.replace(".", "")
                message = card_name + ": " + avail + " " + str(datetime.datetime.now())
                price = price = page_soup.find("li", {"class":"price-current"}).strong.get_text()
                price = price.replace(",", "")
                price = int(price)
                if avail != "OUTOFSTOCK":
                    if price < 750:
                        instock = message + " " + url
                        client.messages.create(
                            to="+1123456789",
                            from_="+1123456789",
                            body=instock
                        )
                    else:
                        print("newegg " + message)
                else:
                    print("newegg " + message)
            elif "canadacomputers" in url:
                headers = cc_headers
                headers['referer'] = url
                req = requests.get(url, headers)
                page_soup = soup(req.content, "html.parser")
                card_name = page_soup.find("h1", {"class":"h3 mb-0"}).get_text()
                avail = page_soup.find("div",{"class":"col-12 py-2"}).span.get_text()
                avail = avail.replace("\n", "")
                avail = avail.replace("  ", "")
                message = card_name + ": " + avail + " " + str(datetime.datetime.now())
                if avail != "Not Available Online":
                    instock = message + " " + url
                    client.messages.create(
                        to="+1123456789",
                        from_="+1123456789",
                        body=instock
                    )
                else:
                    print("cc " + message)
            elif "bestbuy" in url:
                headers = bestbuy_headers
                req = requests.get(url, headers = headers)
                page_soup = soup(req.content, "html.parser")
                card_name = page_soup.find("h1", {"class":"productName_19xJx"}).get_text()
                avail = page_soup.find("span", {"class":"availabilityMessage_1MO75 container_3LC03"}).get_text()
                message = card_name + ": " + avail + " " + str(datetime.datetime.now())
                if avail != "Sold out online":
                    instock = message + " " + url
                    client.messages.create(
                        to="+1123456789",
                        from_="+1123456789",
                        body=instock
                    )
                else:
                    print("bestbuy " + message)
            elif "bhphotovideo" in url:
                headers = bh_headers
                req = requests.get(url, headers)
                page_soup = soup(req.content, "html.parser")
                card_name = page_soup.find("h1", {"class": "title1_17KKS47kFEQb7ynVBsRb_5 reset_gKJdXkYBaMDV-W3ignvsP primary_ELb2ysditdCtk24iMBTUs"}).get_text()
                avail = page_soup.find("span", {"data-selenium":"stockStatus"}).get_text()
                message = card_name + ": " + avail + " " + str(datetime.datetime.now())
                if avail != "New Item - Coming Soon":
                    instock = message + " " + url
                    client.messages.create(
                        to="+1123456789",
                        from_="+1123456789",
                        body=instock
                    )
                else:
                    print(message)
        except:
            print(url)
            f = open(filename, "a")
            f.write(url + " " + str(datetime.datetime.now()) + "\n")
            f.close
        time.sleep(1)
    n = n - 1
    for num in iteration:
        if n == num:
            time.sleep(num*6)
    if n == 3:
        n = 8
    
