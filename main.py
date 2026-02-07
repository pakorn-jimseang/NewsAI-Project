# main.py
import requests
from bs4 import BeautifulSoup
import time
import random
import re

def fetch_soup(url, headers):
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup
    else:
        print("-- Connected Fail --")
        print(f"Status Code: {response.status_code}")
        return None
    
def extract_headlines(soup):
    
    result_list = []
    
    s = soup.find_all('a', 
                      class_=['text-module__text__0GDob text-module__dark-grey__UFC18 text-module__inherit-font__1P1hv text-module__inherit-size__EyiQW link-module__link__INqxZ link-module__underline_on_hover__YTwYC link-module__inherit-line-height__1vd2c media-story-card-module__heading__xgKcP',
                              'text-module__text__0GDob text-module__dark-grey__UFC18 text-module__medium__2Rl30 text-module__heading_6__u1KdJ heading-module__base__p-zaD heading-module__heading_6__-zrtS media-story-card-module__headline__ZWaRz'],
                      attrs={'data-testid': ['Link', 'Heading']}
                      )
    
    print(f"{len(s)} data founded")
    print("-" * 30)
    
    for item in s:
        title = item.text.strip()
        link = item.get('href')
        new_item = {'title': title, 'link': link}
        
        result_list.append(new_item)
    
    return result_list

def extract_content(result_list, soup):
    
    websiteName = 'https://www.reuters.com'
    contentList = []
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36',
    'Referer': 'https://www.reuters.com/',
    'Accept-Language': 'en-US, en;q=0.9, th;q=0.8',
    'Cookie': '_ga_WBSR7WLTGD=GS2.1.s1769908360$o2$g1$t1769912009$j60$l0$h0; usprivacy=1---; _fbp=fb.1.1769695620210.991327313477132089; _gcl_au=1.1.45759110.1769695621; permutive-id=ff740d36-a56c-4af1-8117-a1c2b56bc3cb; _cc_id=d7e2d3c21f74db1d00cb30390eec6d74; panoramaId_expiry=1770300414582; panoramaId=cba845036a807b8a8ca89bfb5144185ca02c2d230c22e2ccf14b07af87bc434a; panoramaIdType=panoDevice; BOOMR_CONSENT="opted-in"; _cb=C__gHqD73LqiCJC3f; _ml_id=f8d25841-a405-4889-ac0c-afab69991a1e.1832767621.1.1832767621.1832767621; _matheriSegs=MATHER_QS_AB_TEST1-C; ajs_anonymous_id=6497ccc2-7c5e-4437-9a81-398f39d78e43; _ga=GA1.2.592050921.1769695622; _pbjs_userid_consent_data=3524755945110770; _v__chartbeat3=BU2doRuMMl1BgvxVX; idw-fe-id=6db694c5-9a49-4175-99f9-73785472e9c9; OneTrustWPCCPAGoogleOptOut=false; _li_dcdm_c=.reuters.com; _gid=GA1.2.1909588994.1769908360; _iiq_fdata=%7B%22pcid%22%3A%22645af2b5-c525-3882-4804-bfb07cad83d1%22%2C%22pcidDate%22%3A1769908364043%7D; __idcontext=eyJjb29raWVJRCI6IjMyM1lhdFMzRHhyaXUxZnZSd01wUVd2QnhjOCIsImRldmljZUlEIjoiMzIzWWF5RFZvczJMU0cycHdWVWxBbWRERzIyIiwiaXYiOiIiLCJ2IjoiIn0%3D; sailthru_content=834e5a05b5c7c582db1dcbc7018cd575; cnx_userId=2-332e608db48048e98c44af67e9a72dd2; cto_bidid=9z67aF96cVhRJTJCSWNBVEdQWTJNVnNFeWw3Y01uYXB6a0FIRUVuTnlMQWFEY1ZnSENNNXNHeFFLV2gzVW9LRXpadmFNb252Q1k1dUE1SSUyQnFWcFN4cWhSTlBiR2IwejhTdmlTdU1rcGxTOTVwOFo5WDglM0Q; _cb_svref=https%3A%2F%2Fwww.google.com%2F; __gads=ID=c4940f1414c4e225:T=1769695615:RT=1769911841:S=ALNI_MbPw5vA7WhehRM1uDISbABE9MVB1Q; __eoi=ID=dde404477c126c60:T=1769695615:RT=1769911841:S=AA-AfjbjVW6qj0x3RlEzuCfbRUy3; dicbo_id=%7B%22dicbo_fetch%22%3A1769911854600%7D; _ga_WBSR7WLTGD=GS2.1.s1769908360$o2$g1$t1769911948$j59$l0$h0; OptanonConsent=isGpcEnabled=0&datestamp=Sun+Feb+01+2026+09%3A12%3A28+GMT%2B0700+(%E0%B9%80%E0%B8%A7%E0%B8%A5%E0%B8%B2%E0%B8%AD%E0%B8%B4%E0%B8%99%E0%B9%82%E0%B8%94%E0%B8%88%E0%B8%B5%E0%B8%99)&version=202509.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=f7d3518d-26dc-4124-8844-af1d6c24366d&interactionCount=1&isAnonUser=1&landingPath=NotLandingPage&groups=1%3A1%2C2%3A1%2C3%3A1%2C4%3A1&AwaitingReconsent=false; ABTastySession=mrasn=&lp=https%253A%252F%252Fwww.reuters.com%252F; sailthru_pageviews=2; ABTasty=uid=4tv6q62ckzcm65gc&fst=1769695620763&pst=1769908358807&cst=1769911852269&ns=3&pvt=12&pvis=2&th=1530618.0.12.2.3.1.1769695620985.1769911948645.0.3; _chartbeat2=.1769695621564.1769911949126.1001.CSrmrqDhuz7PDzZJDjCYqT0MCOWoJ8.2; _awl=2.1769911937.5-4700809d9d1d47a4fc5cfea9af493440-6763652d617369612d6561737431-0; sailthru_visitor=de36aad3-3cf0-4586-aa13-ba074f023821; cto_bundle=igYZpV9JcjhqbGhZZSUyQk5YWXZBMHRoV2hzR21kNXlRR3VPY0xraWVSWlRtUmlIOXJsQUVMcWxrdWloVXFCVlBxVXlvJTJCQzl6aDhUcyUyRmJ5ZCUyQmtyM3k2M0g3S0ppUzQyYWR3Y1JvT1JoQWRSQk5NMEROYm1FZzlGWTBwMnRxRU1IT25pOGhZciUyRmxEV1djVHdsb09FalZoTWNVT0N3JTNEJTNE; datadome=17yH3vrZ9bhqNvtqqoyK6rysE3tE5QNaaZlpS0_hxOHeNefWm4v_T8b4u4rjc3x0gxv0ngBWXDUsAcW_FWjoEqOpIdV1fbR9JUNqxgImV7heQ1n0ykiUMI5yLbu2SXEA; _gat=1; _dd_s=rum=0&expire=1769912909143; RT="z=1&dm=www.reuters.com&si=d2a41ddb-2036-478b-b242-a5cd4b22cdde&ss=ml33vj4x&sl=1&tt=sy&rl=1&ld=xo&ul=1eib"'
    }
    
    for item in result_list:     
        get_link = item['link']
        readyURL = f"{websiteName}{get_link}"
        contentSoup = fetch_soup(readyURL, headers)
        
        if contentSoup is None:
            print(f"Skipping: {readyURL}")
            continue
        
        paragraphs = contentSoup.find_all('div',
                            # class_='article-body-module__content__bnXL1',
                            attrs={'data-testid': re.compile(r'paragraph-\d+')}
                            )
            
        theArticleText = " ".join([p.text.strip() for p in paragraphs])
        contentList.append(theArticleText)
        
        politeness_delay(2, 4)
        
    return contentList

def politeness_delay(min_seconds=2, max_seconds=5):
    wait_time = random.uniform(min_seconds, max_seconds)
    print(f"Waiting for {wait_time:.2f} seconds before next request...")
    time.sleep(wait_time)
    
def main():
    url = 'https://www.reuters.com/technology/'
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36',
    'Referer': 'https://www.reuters.com/',
    'Accept-Language': 'en-US, en;q=0.9, th;q=0.8',
    'Cookie': '_ga_WBSR7WLTGD=GS2.1.s1769908360$o2$g1$t1769912009$j60$l0$h0; usprivacy=1---; _fbp=fb.1.1769695620210.991327313477132089; _gcl_au=1.1.45759110.1769695621; permutive-id=ff740d36-a56c-4af1-8117-a1c2b56bc3cb; _cc_id=d7e2d3c21f74db1d00cb30390eec6d74; panoramaId_expiry=1770300414582; panoramaId=cba845036a807b8a8ca89bfb5144185ca02c2d230c22e2ccf14b07af87bc434a; panoramaIdType=panoDevice; BOOMR_CONSENT="opted-in"; _cb=C__gHqD73LqiCJC3f; _ml_id=f8d25841-a405-4889-ac0c-afab69991a1e.1832767621.1.1832767621.1832767621; _matheriSegs=MATHER_QS_AB_TEST1-C; ajs_anonymous_id=6497ccc2-7c5e-4437-9a81-398f39d78e43; _ga=GA1.2.592050921.1769695622; _pbjs_userid_consent_data=3524755945110770; _v__chartbeat3=BU2doRuMMl1BgvxVX; idw-fe-id=6db694c5-9a49-4175-99f9-73785472e9c9; OneTrustWPCCPAGoogleOptOut=false; _li_dcdm_c=.reuters.com; _gid=GA1.2.1909588994.1769908360; _iiq_fdata=%7B%22pcid%22%3A%22645af2b5-c525-3882-4804-bfb07cad83d1%22%2C%22pcidDate%22%3A1769908364043%7D; __idcontext=eyJjb29raWVJRCI6IjMyM1lhdFMzRHhyaXUxZnZSd01wUVd2QnhjOCIsImRldmljZUlEIjoiMzIzWWF5RFZvczJMU0cycHdWVWxBbWRERzIyIiwiaXYiOiIiLCJ2IjoiIn0%3D; sailthru_content=834e5a05b5c7c582db1dcbc7018cd575; cnx_userId=2-332e608db48048e98c44af67e9a72dd2; cto_bidid=9z67aF96cVhRJTJCSWNBVEdQWTJNVnNFeWw3Y01uYXB6a0FIRUVuTnlMQWFEY1ZnSENNNXNHeFFLV2gzVW9LRXpadmFNb252Q1k1dUE1SSUyQnFWcFN4cWhSTlBiR2IwejhTdmlTdU1rcGxTOTVwOFo5WDglM0Q; _cb_svref=https%3A%2F%2Fwww.google.com%2F; __gads=ID=c4940f1414c4e225:T=1769695615:RT=1769911841:S=ALNI_MbPw5vA7WhehRM1uDISbABE9MVB1Q; __eoi=ID=dde404477c126c60:T=1769695615:RT=1769911841:S=AA-AfjbjVW6qj0x3RlEzuCfbRUy3; dicbo_id=%7B%22dicbo_fetch%22%3A1769911854600%7D; _ga_WBSR7WLTGD=GS2.1.s1769908360$o2$g1$t1769911948$j59$l0$h0; OptanonConsent=isGpcEnabled=0&datestamp=Sun+Feb+01+2026+09%3A12%3A28+GMT%2B0700+(%E0%B9%80%E0%B8%A7%E0%B8%A5%E0%B8%B2%E0%B8%AD%E0%B8%B4%E0%B8%99%E0%B9%82%E0%B8%94%E0%B8%88%E0%B8%B5%E0%B8%99)&version=202509.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=f7d3518d-26dc-4124-8844-af1d6c24366d&interactionCount=1&isAnonUser=1&landingPath=NotLandingPage&groups=1%3A1%2C2%3A1%2C3%3A1%2C4%3A1&AwaitingReconsent=false; ABTastySession=mrasn=&lp=https%253A%252F%252Fwww.reuters.com%252F; sailthru_pageviews=2; ABTasty=uid=4tv6q62ckzcm65gc&fst=1769695620763&pst=1769908358807&cst=1769911852269&ns=3&pvt=12&pvis=2&th=1530618.0.12.2.3.1.1769695620985.1769911948645.0.3; _chartbeat2=.1769695621564.1769911949126.1001.CSrmrqDhuz7PDzZJDjCYqT0MCOWoJ8.2; _awl=2.1769911937.5-4700809d9d1d47a4fc5cfea9af493440-6763652d617369612d6561737431-0; sailthru_visitor=de36aad3-3cf0-4586-aa13-ba074f023821; cto_bundle=igYZpV9JcjhqbGhZZSUyQk5YWXZBMHRoV2hzR21kNXlRR3VPY0xraWVSWlRtUmlIOXJsQUVMcWxrdWloVXFCVlBxVXlvJTJCQzl6aDhUcyUyRmJ5ZCUyQmtyM3k2M0g3S0ppUzQyYWR3Y1JvT1JoQWRSQk5NMEROYm1FZzlGWTBwMnRxRU1IT25pOGhZciUyRmxEV1djVHdsb09FalZoTWNVT0N3JTNEJTNE; datadome=17yH3vrZ9bhqNvtqqoyK6rysE3tE5QNaaZlpS0_hxOHeNefWm4v_T8b4u4rjc3x0gxv0ngBWXDUsAcW_FWjoEqOpIdV1fbR9JUNqxgImV7heQ1n0ykiUMI5yLbu2SXEA; _gat=1; _dd_s=rum=0&expire=1769912909143; RT="z=1&dm=www.reuters.com&si=d2a41ddb-2036-478b-b242-a5cd4b22cdde&ss=ml33vj4x&sl=1&tt=sy&rl=1&ld=xo&ul=1eib"'
    }
    
    soup = fetch_soup(url, headers)
    
    if soup is None:
        print("Stopping process due to fetching error.")
        return
    
    newsHeadline = extract_headlines(soup)
    
    for item in newsHeadline:
        print(item)
        
    print("-" * 30)
    
    newsContent = extract_content(newsHeadline, soup)
    
    for item in newsContent:
        print(item)
        print("-" * 30)

if __name__ == "__main__":
    main()