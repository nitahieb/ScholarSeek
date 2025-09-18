# Scholar Seek

**Know a topic? Pull up articles. Meet authors. Make contact.**

Scholar Seek is a modern web application that helps researchers quickly find research papers on any topic and provides author contact information for easy collaboration.

![Scholar Seek Web Interface](https://github.com/user-attachments/assets/29e0dca0-2be9-40b6-ac7c-122956a26936)

## 🌐 Web Application

The primary way to use Scholar Seek is through our intuitive web interface. Simply search for any research topic and get instant access to relevant PubMed articles, author details, and contact information.

**Features:**
- Clean, modern interface with user authentication  
- Real-time PubMed search with instant results
- Author contact information extraction
- Multiple output formats (overview and email lists)
- Advanced filtering and sorting options

---

## 🚀 Running the Web App Locally

### Frontend (React + TypeScript)
```bash
cd frontend
npm install
npm run dev
```
The frontend will be available at `http://localhost:5173`

### Backend (Django + REST API)
```bash
poetry install
cd backend
python manage.py runserver
```
The backend API will be available at `http://localhost:8000`

---

##  What Is It

Type in "cancer immunotherapy" and see titles, authors, affiliations, and emails. No more fumbling through PubMed pages manually.

---

## Using the GitHub Action

You can interact with Scholar Seek directly from GitHub using the provided GitHub Action workflow. This is useful for running searches and retrieving results without setting up the app locally.

### How to Trigger

- **Manually:** Go to the **Actions** tab in your GitHub repository, select `Run application`, and click **Run workflow**. Fill in the input fields as needed.

### Supported Parameters

| Parameter      | Description                                 | Required | Default     | Options/Example Values           |
| -------------- | ------------------------------------------- | -------- | ----------- | ------------------------------- |
| `search`       | Topic or query to search for                | Yes      | –           | "cancer immunotherapy"          |
| `mode`         | Output type                                 | No       | overview    | overview, emails                |
| `email`        | Filter by author email                      | No       | (empty)     | "author@email.com"              |
| `searchnumber` | Number of results to return                 | No       | 10          | 1, 5, 20                        |
| `sortby`       | Sort order for PubMed search                | No       | relevance   | relevance, pub_date, Author, JournalName |

### Modes

- `overview`: Returns a summary of articles for the search term.
- `emails`: Returns author emails for the search term.

### Example: Manual Run

1. Go to **Actions** > **Run application** > **Run workflow**.
2. Enter your search term (e.g., `cancer immunotherapy`).
3. Choose a mode (e.g., `emails` to get author emails).
4. Optionally set `searchnumber`, `sortby`, or `email`.
5. Click **Run workflow**. Results will appear in the workflow summary.

---

## How to Use the CLI Script

You can also run Scholar Seek as a command-line tool directly from your terminal.

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


```bash
python main.py "cancer immunotherapy" -e example@email.com
```

Search and display articles associated with a specific author email.

**Combine options:**

```bash
python main.py "cancer immunotherapy" -n 5 -m emails -s date
```

You can mix and match options to customize your search results.

---

## 🏭 Production Deployment

ScholarSeek is production-ready with comprehensive security, performance, and monitoring features.

### Quick Production Setup

1. **Build for production**:
   ```bash
   ./scripts/build-production.sh
   ```

2. **Configure environment**:
   ```bash
   cp backend/.env.production.template backend/.env.production
   # Edit with your production settings
   ```

3. **Deploy**:
   ```bash
   export DJANGO_ENVIRONMENT=production
   ./scripts/deploy-production.sh
   ```

### Production Features

- ✅ **Security**: HTTPS, HSTS, secure cookies, CORS protection
- ✅ **Performance**: Static file optimization, database connection pooling
- ✅ **Monitoring**: Health checks, structured logging, error reporting
- ✅ **Scalability**: Docker support, load balancer ready
- ✅ **Reliability**: Automated backups, disaster recovery procedures

### Documentation

- **[Deployment Guide](DEPLOYMENT.md)** - Complete production setup instructions
- **[Production Checklist](PRODUCTION_CHECKLIST.md)** - Comprehensive production readiness verification

---

##  Contributing

We welcome your contributions! Please check out our [`CONTRIBUTING.md`](CONTRIBUTING.md) for guidelines on how to submit pull requests, ensure checks pass, and request approvals.

## Linting with Ruff

We use [Ruff](https://github.com/charliermarsh/ruff) as our Python linter to maintain code quality and consistency.

**Install Ruff:**

```bash
pip install ruff
```

**Run Ruff manually:**

```bash
ruff check .
```

This will analyze your project and display any style or linting issues.

**Recommended:** Use the [Ruff VS Code extension](https://marketplace.visualstudio.com/items?itemName=charliermarsh.ruff) for inline linting and autofix suggestions while editing your code.

---
