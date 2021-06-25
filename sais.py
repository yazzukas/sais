
from requests_html import HTMLSession  # https://pypi.org/project/requests-html/
from datetime import date

session = HTMLSession()

r = session.get('https://www.sais.ee/PublicInfo/Rankings')
koolid = r.html.find('body > div.body > div.container > div', first=True)
#print(about.text)
#print(about.absolute_links)

f = open(str(date.today()) + ".txt", "w")

for kooli_link in koolid.absolute_links:
    #print(kooli_link)
    r = session.get(kooli_link)
    kooli_nimi = r.html.find('body > div.body > div.container > div > h1', first=True)
    eriala_vastuvõetud_lingid = r.html.find('body > div.body > div.container > div > table:nth-child(3) > tbody', first=True)
    if eriala_vastuvõetud_lingid is not None:
        for link in eriala_vastuvõetud_lingid.absolute_links:
            if "Accepted" in link:
                #print(link)

                r = session.get(link)
                eriala = r.html.find('body > div.body > div.container > div > h1',first=True)
                vastuvõetud_õpilased = r.html.find('body > div.body > div.container > div > table > tbody', first=True)

                for vastuvõetud_õpilane in vastuvõetud_õpilased.text.splitlines():
                    if "Kandidaat ei avalikusta nime" not in vastuvõetud_õpilane:
                        #print(vastuvõetud_õpilane)
                        f.write(vastuvõetud_õpilane + "; " + kooli_nimi.text + "; " + eriala.text + "\n")

f.close()
