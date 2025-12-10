# linkedin-jobs-api-py

[![PyPI version](https://badge.fury.io/py/linkedin-jobs-api-py.svg)](https://badge.fury.io/py/linkedin-jobs-api-py)
[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/downloads/)
[![License MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

**Unofficial LinkedIn Jobs API for Python** - This project is inspired by an npm package [`linkedin-jobs-api`](https://www.npmjs.com/package/linkedin-jobs-api) from Vishwa Gaurav. Scrape LinkedIn job postings with all filters (keywork,location,remote, salary, experience, etc.).


## 🚀 Installation

```bash
pip install linkedin-jobs-api-py  
```

## 📖 Simple usage
```python
from linkedin_jobs_api import query

# Recherche basique
jobs = query(keyword="python developer", location="Paris", limit="10")

for job in jobs:
    print(f"💼 {job['position']} @ {job['company']}")
    print(f"📍 {job['location']} | 💰 {job['salary']}")
    print(f"🔗 {job['jobUrl']}\n")
   ```


## 🔍 All available filters

| Parameter | Possible values                                                                     | Example |
|-----------|----------------------------------------------------------------------------------------|---------|
| `keyword` | Free text                                                                            | `"data scientist"` |
| `location` | City/Country                                                                               | `"Paris"`, `"Remote"` |
| `dateSincePosted` | `"1hr"`,`"24hr"`,`"past week"`,`"past month"`                                          | `"past week"` |
| `jobType` | `"full time"`, `"part time"`, `"contract"`, `"temporary"`, `"internship"`, `"volunteer"` | `"full time"` |
| `remoteFilter` | `"remote"`, `"on site"`, `"hybrid"`                                                    | `"remote"` |
| `salary` | `"40000"`, `"60000"`, `"100000"`, `"120000"`                                           | `"100000"` |
| `experienceLevel` | `"internship"`,`"entry level"`,`"associate"`, `"senior"`, `"director"`,`"executive"`   | `"senior"` |
| `limit` | `"1"`,`"3"`....`"10"`                                                                  | `"5"` |
| `page` | `"0"`, `"1"`, `"2"`...`"999"` (10 jobs/page)                                           | `"1"` |
| `has_verification` | `True`/`False`                                                                         | `True` |
| `under_10_applicants` | `True`/`False`                                                                         | `True` |

## 💡 Complete examples

### 1. Simple search
```python
jobs = query(keyword="frontend", location="Lyon", limit="5")
```

### 2. Remote + Recent full-time
```python
jobs = query(
keyword="backend developer",
remoteFilter="remote",
jobType="full time",
dateSincePosted="past week",
limit="10"
)
```


### 3. Senior + good salary
```python
jobs = query(
keyword="software engineer",
experienceLevel="senior",
salary="100000",
location="France",
limit="8"
)
```

### 4. “Easy” jobs (verified, <10 applicants)
```python
jobs = query(
keyword="product manager",
has_verification=True,
under_10_applicants=True,
sortBy="recent"
)
```

### 5. Pagination (page 2)
```python
jobs = query(keyword="devops", page="1", limit="10") # Jobs 11-20
```

## 📋 Structure of results
```json
{
"position": "Senior Python Developer",
"company": "Google",
"companyLogo": "https://media...png",
"location": "Paris, Île-de-France",
"date": "2025-12-08",
"agoTime": "2 days ago",
"salary": "€80k-€120k",
"jobUrl": "https://www.linkedin.com/jobs/view/..."
}
```

## 🛠️ Development

Clone et install dev
```bash
git clone <repo>
cd linkedin-jobs-api-py
pip install -e .[dev]
```

## ⚠️ Warnings

- **Unofficial use** : Comply with LinkedIn's Terms of Use and rate limits.
- **Browser simulation**: Complete headers simulating an AJAX request from a real browser
- **Rate limiting awareness**: Moderate usage recommended, proxies required for high volumes
- **Changes** : LinkedIn may modify its APIs (regular updates).

## 📄 Licence

MIT License - see [LICENSE](LICENSE)

---

**⭐  Star so useful!!** | **🐛 Issues** : [GitHub](https://github.com/ANSELME-TIC/linkedin-jobs-api-py)



