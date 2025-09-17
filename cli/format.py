
def overviewFormat(articles):
    md=""
    for article in articles:
        md += f"""##  Article Overview

**Title:** {article.title}
**URL:** https://pubmed.ncbi.nlm.nih.gov/{article.pmid}
**Language:** {article.language}
**Publication Date:** {article.date}
**PMID:** {article.pmid}

---

###  Authors & Affiliations

| Author | Affiliation |
|--------|-------------|
"""
        for a in article.people:
            md += f"| {a.firstName +' '+ a.lastName} | {a.affiliation} |\n"
        if article.emails:
            md += "\n**Emails:** "
            md += ", ".join(article.emails)
            md+= "\n"
    return md

def emailFormat(emails):
    return ", ".join(emails)
