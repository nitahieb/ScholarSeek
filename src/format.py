
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

##  Authors & Affiliations

| Author | Affiliation |
|--------|-------------|
"""
        for a in article.people:
            md += f"| {a.firstName +' '+ a.lastName} | {a.affiliation} |\n"
    md+= f"**Emails:** {article.emails}"
    return md
