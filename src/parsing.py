from lxml import etree
import re
from researcher import Researcher

def parse_xml(response):
    parser = etree.XMLParser(ns_clean=True, recover=True)
    return etree.fromstring(response.getvalue(), parser)

def extract_basics(article):
    return (
        article.findtext('.//PMID'),
        article.findtext('.//ArticleTitle'),
        article.findtext('.//Language')
    )

def extract_publish_date(article):
    pub = article.find('.//PubDate')
    if pub is None:
        return ""
    parts = [pub.findtext(tag) for tag in ('Year', 'Month', 'Day')]
    return "-".join(filter(None, parts))

def extract_authors_and_emails(article):
    emails = set()
    authors = []
    for auth in article.findall('.//Author'):
        last = auth.findtext('LastName')
        first = auth.findtext('ForeName')
        initials = auth.findtext('Initials')
        affiliation = auth.findtext('.//Affiliation') or ""
        email = extract_email(affiliation)
        if email:
            emails.add(email)
        authors.append(Researcher(last, first, initials, affiliation, email))
    return emails, authors

def extract_email(text):
    match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text or "")
    return match.group(0) if match else None
