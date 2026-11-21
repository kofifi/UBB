# UM

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
um-train
um-evaluate
um-predict data/raw/new.csv -o predictions.csv
```
