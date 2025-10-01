# Find Company Website

Find and validate official company websites using Serper API and intelligent validation.

## Quick Start

1. **Get API Key**: Sign up at [serper.dev](https://serper.dev/) (free)
2. **Set Environment Variable**:
   ```bash
   export SERPER_API_KEY="your_api_key_here"
   ```
3. **Run**:
   ```bash
   # Basic search
   uv run task_examples/find_company_website/find_company_website.py "Apple Inc"
   
   # Advanced validation
   uv run task_examples/find_company_website/validate_company_website.py --company "Apple Inc"
   ```

## What It Does

- **Finds** company websites using Google search via Serper API
- **Filters** out social media, news sites, and non-official pages
- **Validates** ownership by analyzing page content (title, headers, structured data)
- **Supports** international companies with proper character handling

## Files

- `find_company_website.py` - Basic website finder
- `validate_company_website.py` - Advanced validator with retry logic
- `html_utils.py` - HTML parsing and validation helpers
- `serper_client.py` - Serper API client

## Usage Examples

### Basic Search
```bash
uv run task_examples/find_company_website/find_company_website.py "Google LLC"
```

**Output:**
```
Searching for: Google LLC
Found: Google LLC
Website: https://www.google.com/
```

### Advanced Validation
```bash
uv run task_examples/find_company_website/validate_company_website.py --company "Apple Inc"
```

**Output:**
```
[1/3] Validating https://www.apple.com ...
Valid: Apple Inc → https://www.apple.com
----
Company: Apple Inc
Validated: True
Website: https://www.apple.com
Checked: 1
```

## Company Examples

**International:**
- `Apple Inc` → https://www.apple.com/
- `Google LLC` → https://www.google.com/
- `Microsoft Corporation` → https://www.microsoft.com/

**Turkish:**
- `Upsonic Teknoloji A.Ş` → https://upsonic.ai/
- `Trendyol Teknoloji A.Ş` → https://www.trendyol.com/
