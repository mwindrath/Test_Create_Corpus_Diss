import requests
from bs4 import BeautifulSoup
import os
import time
import random
import warnings


warnings.filterwarnings("ignore")

def parse_xml(url):
        response = requests.get(url,verify=False)
        soup = BeautifulSoup(response.text, 'xml')
        sleep_time = random.uniform(5, 30)
        time.sleep(sleep_time)
        antwort = soup.prettify()
        return antwort


base_url = "https://digisam.ub.uni-giessen.de/ubg-ihd-fhl/oai/?verb=GetRecord&metadataPrefix=mets&identifier="


with open('links.txt', 'r') as file:
    # Read all the lines of the file into a list
    lines = file.readlines()


lines = [line.rstrip('\n') for line in lines]
# Print the list of lines
print(lines)

#id = "5334643"

for id in lines:

    # HTTP-Anfrage an die Webseite senden
    response = requests.get(base_url+id,verify=False)
    print(response.status_code)
    if response.status_code == 200:
        print(f"bearbeite {id} ...")
        soup = BeautifulSoup(response.text, 'xml')
        mets_xml = os.path.join(id,f"{id}-mets.xml")
        if not os.path.isfile(mets_xml):
            print(f"Lade {mets_xml} herunter...")
            with open(mets_xml, 'w') as file:
                        file.write(soup.prettify())
            sleep_zeit = random.uniform(5, 20)
            time.sleep(sleep_zeit)

        # Alle <mets:file>-Elemente mit MIMETYPE="text/xml" finden
        for file_tag in soup.find_all('file', {'MIMETYPE': 'text/xml'}):
            # Das erste Kind-Element des <mets:file>-Elements finden
            child_tag = file_tag.find(True, recursive=False)
            print(child_tag)
            if child_tag is not None:
                # Den Attributwert von xlink:href extrahieren
                print(child_tag.get('xlink:href'))
                url_text = child_tag.get('xlink:href')
                name = child_tag.get('xlink:href').split("/")[-1]
                alto_xml = os.path.join(id,f"{name}.xml")
                if not os.path.isfile(alto_xml):
                    print(f"Lade {alto_xml} herunter...")
                    with open(alto_xml, 'w') as file:
                        file.write(parse_xml(url_text))
                    sleep_zeit = random.uniform(5, 20)
                    time.sleep(sleep_zeit)
        
    else:
        print(response.status_code)
    