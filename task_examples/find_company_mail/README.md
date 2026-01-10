# Find Company Mail

Find a company's email by querying the web with the format `mail: {company}` and extracting emails from search results.

## Usage

```bash
python task_examples/find_company_mail/find_company_mail.py --company "Linktera"
```

Example output:

```json
{
  "company": "Linktera",
  "email": "info@linktera.com"
}
```

## Notes

- Uses Serper (`SERPER_API_KEY` in your `.env`) to perform the query `mail: {company}`.
- Extracts emails from result titles, snippets, and links.

