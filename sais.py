
from requests_html import HTMLSession  # https://pypi.org/project/requests-html/
from datetime import date
import time

tic = time.perf_counter()

session = HTMLSession()
r = session.get('https://www.sais.ee/PublicInfo/Rankings')
koolid = r.html.find('body > div.body > div.container > div', first=True)

for kooli_link in koolid.absolute_links:
    r = session.get(kooli_link)
    kooli_nimi = r.html.find('body > div.body > div.container > div > h1', first=True).text
    eriala_vastuvõtt = r.html.find('body > div.body > div.container > div > table:nth-child(3) > tbody', first=True)
    if eriala_vastuvõtt is not None:
        for link in eriala_vastuvõtt.absolute_links:
            if "Accepted" in link:
                r = session.get(link)
                eriala_nimi = r.html.find('body > div.body > div.container > div > h1', first=True).text
                vastuvõetud_õpilased = r.html.find('body > div.body > div.container > div > table > tbody', first=True).text.splitlines()
                with open(str(date.today()) + ".txt", "w") as fail:
                    for vastuvõetud_õpilane in vastuvõetud_õpilased:
                        if "Kandidaat ei avalikusta nime" not in vastuvõetud_õpilane:
                            fail.write(vastuvõetud_õpilane + "; " + kooli_nimi + "; " + eriala_nimi + "\n")
toc = time.perf_counter()
print(toc - tic)