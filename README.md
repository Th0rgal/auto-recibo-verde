# Automatic invoices for Portugal

This selenium script allows to automatically submit an invoice to Portugal government website.
You can consult the invoices you submited [here](https://irs.portaldasfinancas.gov.pt/recibos/portal/consultar).

### To install:
```
python3 -m venv ./venv
source venv/bin/activate
pip install -r requirements.txt
```

### To use:
Copy `.info.template.py` in `info.py` and update with your credentials.
```
source venv/bin/activate
python declare.py
```
This should open chrome and fill info for you. You'll have a summary displayed and you just need to confirm it.