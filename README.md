# Upsonic Examples

This repository contains simple examples that demonstrate how to use the **Upsonic** framework.

---

## Quickstart

1. **Clone the repo**
   ```bash
   git clone https://github.com/Upsonic/Examples.git
   cd Examples
   ```

2. **Install dependencies**
   Make sure you have Python 3.10+ and install required packages:
   ```bash
   pip install upsonic pydantic
   ```

3. **Set your API key**
   Export your OpenAI API key:
   ```bash
   export OPENAI_API_KEY="your_api_key_here"
   ```

## Example: Extract Company Name from Document

These examples show how to extract the company name from a Turkish Vergi Levhası (Tax Certificate) PNG using the Upsonic framework.

### Direct Client
Run:
```bash
python examples/extract_company_name_direct.py
```

### Agent Client
Run:
```bash
python examples/extract_company_name_agent.py
```

## Expected Output
```yaml
Extracted Company Name: UPSONIC TEKNOLOJİ ANONİM ŞİRKETİ
```