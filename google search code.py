from google import search
import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import Request,  urlopen
from urllib.error import HTTPError 
 
import re

#%%
search_terms = ['Football','Politics','Science']

for sterm in search_terms:
    urllist = []
    for url in search(sterm, tld='co.in', lang='en', stop=53):
        url = re.sub("#.*$","",url)
        url = re.sub(".*.pdf$","https://www.google.co.in/",url) # remove pdf links
        urllist.append(url)

# drop duplicate URL        
    urllist = list(set(urllist))

    text3 = []
    for url in urllist:
        req = Request(url, headers={'User-Agent': 'Mozilla/43.0.4'}) 
        # Some website doesn't allow automated requested so we are using Mozilla ;
        # Mozilla Firefox need not be the default browser. It only needs to be installed in the system
        # Further your System antivirus might kill python process because of continuous request so disable antivirus for some time
        try:
            page = urlopen(req).read()
            soup = BeautifulSoup(page)
            [s.extract( ) for s in soup('script')] # remove all scripts from page source
            [s.extract( ) for s in soup('style')]  # remove all css styles from page source
            temp3 = soup.get_text(' ')
            temp3 = re.sub('\n',' ',temp3)
            temp3 = re.sub('\s+',' ',temp3)
            text3.append(temp3)
            
        except HTTPError:
            print('IDK')
            text3.append('NA')
        
    out = pd.DataFrame({'url':urllist,
                        'text':text3
                        })
    
    out_text = pd.DataFrame({'text':out.text})
    
    out_xls = pd.DataFrame({'url':out.url})
    
    out_text.to_csv("Y:\\Knowledge Repository\\ISB\\Practicum\\Session-2\\"+sterm+" google search.csv")
    
    out_xls.to_csv("Y:\\Knowledge Repository\\ISB\\Practicum\\Session-2\\"+sterm+" google search list.csv")
    