# Document Analyzer Example

This example demonstrates how to use the **Upsonic** framework to extract the company name from a Turkish Tax Certificate (Vergi Levhası).

---

## Files
- `extract_company_name.py` → basic example using an Upsonic agent  
- `assets/vergi_levhasi.png` → sample tax certificate  

---

## Run the Example

Activate your environment and run:

```bash
python task_examples/document_analyzer/extract_company_name.py
```

### Expected Output
The program will print the extracted company name, for example:

```yaml
Extracted Company Name: UPSONIC TEKNOLOJİ ANONİM ŞİRKETİ
```

**Note**: Output may vary slightly depending on Upsonic version and OCR results.

## Notes
- Tested with upsonic==0.61.1a1758720414