from celery import shared_task
from .models import *
from organizations.models import *
import time
import newspaper
import re
import tldextract
from bs4 import BeautifulSoup
import urllib.request
import reversion
from urllib.parse import urlparse
from urllib.error import HTTPError

base_wikipedia_url = 'http://en.wikipedia.org/wiki/'

@shared_task
def get_organization_info(url, **kwargs):
    if not 'wikilink' in kwargs:
        try:
            o = urllib.parse.urlsplit(url)
            url_without_path = o.scheme + '://' + o.netloc
            n = newspaper.build(url_without_path)
            n_domains = []
            for category in n.category_urls():
                domain = urllib.parse.urlsplit(category).netloc
                if (domain not in n_domains):
                    n_domains.append(domain)
        except:
            return

        try:
            extracted = tldextract.extract(url_without_path)
            tld = "{}.{}".format(extracted.domain, extracted.suffix)
            url = urllib.parse.urljoin(base_wikipedia_url, tld)
            print('TRYING URL ' + url)
            response = urllib.request.urlopen(create_request(url)).read().decode('utf-8')
            soup = BeautifulSoup(response, 'html.parser')
        except HTTPError:
            url = urllib.parse.urljoin(base_wikipedia_url, n.brand)
            print('TRYING URL ' + url)
            response = urllib.request.urlopen(create_request(url)).read().decode('utf-8')
            soup = BeautifulSoup(response, 'html.parser')
    else:
        url = base_wikipedia_url[:-6] + url
        response = urllib.request.urlopen(create_request(url)).read().decode('utf-8')
        soup = BeautifulSoup(response, 'html.parser')

    try:
        org_name = soup.find('h1', { "class" : "firstHeading" }).text
    except:
        print('nameerror')

    [s.extract() for s in soup('sup')]
    intro = soup.find('p').getText()
    infobox_table = soup.findAll('table', { "class" : "infobox" })
    if (infobox_table):
        infobox_table = infobox_table[0]
        infobox_data = parse_wikipedia_table(infobox_table)

        web_address = '#'
        if ('Website' in infobox_data):
            web_address = infobox_data['Website'].find('a')['href']
        elif ('Web address' in infobox_data):
            web_address = infobox_data['Web address'].find('a')['href']

        if not Organization.objects.filter(name=org_name).exists():
            with reversion.create_revision():
                print('CREATING WITH WIKIPAGE ' + url)
                org = Organization(name=org_name, description=intro, homepage=web_address, wikipedia_page=url)
                org.save()
            if not 'wikilink' in kwargs:
                for domain in n_domains:
                    with reversion.create_revision():
                        d = OrganizationDomain(domain=domain, organization=org)
                        d.save()
        else:
            org = Organization.objects.get(name=org_name)
    else:
        print('NO INFOBOX')
        return


    if 'child' in kwargs:
        org.child_organizations.add(kwargs['child'])

    owner_data = get_owner_data(infobox_data)

    if owner_data[0] == 0:
        get_organization_info(owner_data[1], child=org, wikilink=True)
    elif owner_data[0] == 1:
        with reversion.create_revision():
            parent_org = Organization(name=owner_data[1])
            parent_org.save()
            parent_org.child_organizations.add(org)
            parent_org.save()
    else:
        return


def get_owner_data(infobox_data):
    possible_field_names = ['Owner', 'Parent', 'Owned by', 'Owner(s)', 'Company']
    #(0 = there is link, 1 = there is name, 2 = there is no parent)
    for fieldname in possible_field_names:
        if (fieldname in infobox_data):
            if (infobox_data[fieldname].find('a')):
                #simply get the last link for now
                link = infobox_data[fieldname].find_all('a')[-1]
                return (0, link['href'])
            else:
                #or just get the name
                owner_name = infobox_data[fieldname].text
                return (1, owner_name)
    return [2]

def parse_wikipedia_table(infobox_table):
    infobox_rows = infobox_table.find_all('tr')
    infobox_data = {}
    for row in infobox_rows:
        if row.find('th'):
            key = row.find('th').text
            value = row.find('td')
            infobox_data[key.replace('\xa0', ' ')] =  value
    return infobox_data

def create_request(url):
    return urllib.request.Request(
        url,
        data=None,
        headers={
        'User-Agent': 'Truthbot Web Scraper/1.0 (https://github.com/Jaxkr/Truthbot.org; jacksonroberts25@gmail.com) urllib/Python3'
        }
    )
