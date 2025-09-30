# Find Company Website Example

This example demonstrates how to use the **Upsonic** framework together with the **Serper API** to find the official website of a company when you only know its name.

---

## Files
- `find_company_website.py` → script that searches for the company's website using Serper API  
- `serper_client.py` → small helper for making Serper API requests  

---

## Setup
1. Get a free API key from [Serper](https://serper.dev/).  
2. Export it in your shell so the code can read it:
   ```bash
   export SERPER_API_KEY="your_api_key_here"
   ```

## Run the Example
From the repo root, run directly with `uv`:

```bash
uv run task_examples/find_company_website/find_company_website.py
```

## Example Output
```makefile
Company: Upsonic Teknoloji
Website: https://upsonic.ai/
```

## Notes
Tested with upsonic==0.61.1a1758720414

This script shows how to find the website.
