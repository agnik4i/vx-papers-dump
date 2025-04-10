# VX Papers Dump

This tool automates the download of PDF papers from [VX Underground](https://vx-underground.org/Papers/Windows/) using Playwright and Python.

> ⚠️ **DISCLAIMER**  
> Just helping a friend study.  
> VXUnderground, don't ban me — love u guys ❤️

---

##  Features
- Crawls all subdirectories under `Papers/Windows/`
- Automatically downloads all `.pdf` files
- Organizes everything by folder
- Headless browser automation via Playwright

##  Requirements

- Python 3.9+
- `playwright`
- `requests`

Install dependencies:
```bash
pipenv shell
pip install playwright
playwright install
