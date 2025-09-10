# PubMed Author Finder

**Know a topic? Pull up articles. Meet authors. Make contact.**

PubMed Author Finder helps you quickly find research papers on any topic and gives you author contact info so you can reach out faster.

---

##  What Is It

 Type in “cancer immunotherapy” and see titles, authors, affiliations, and emails. No more fumbling through PubMed pages manually.

---

## How to Use

Once installed, you can run `PubMedSearch` directly from your terminal.

**Basic search:**

```bash
python main.py "cancer immunotherapy"
```

This will display an overview of the top 10 most relevant articles for the search term.

**Specify number of results:**

```bash
python main.py "cancer immunotherapy" -n 5
```

This returns only the top 5 results.

**Choose output mode:**

```bash
python main.py "cancer immunotherapy" -m emails
```

`-m` or `--mode` can be one of the available application output options (e.g., `relevance`, `pub_date`, `Author`, `JournalName`).

**Sort results:**

```bash
python main.py "cancer immunotherapy" -s date
```

Sort articles by relevance, date, or other supported PubMed sort options.

**Filter by email (optional):**

```bash
python main.py "cancer immunotherapy" -e example@email.com
```

Search and display articles associated with a specific author email.

**Combine options:**

```bash
python main.py "cancer immunotherapy" -n 5 -m emails -s date
```

You can mix and match options to customize your search results.
--

##  Contributing

We welcome your contributions! Please check out our [`CONTRIBUTING.md`](CONTRIBUTING.md) for guidelines on how to submit pull requests, ensure checks pass, and request approvals.

