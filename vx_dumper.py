from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
import os
import requests
import time

#pipenv shell
#pip install playwright
#playwright install

BASE_URL = "https://vx-underground.org/Papers/Windows/"
OUTPUT_DIR = "vx_papers"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def download_pdf(url, destination):
    try:
        print(f"[DEBUG] Downloading: {destination}")
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        with open(destination, "wb") as file:
            file.write(response.content)
        print(f"[SUCCESS] Saved: {destination}")
    except Exception as e:
        print(f"[ERROR] Failed to download {url} - {e}")

def clean_folder_names(elements):
    seen = set()
    folders = []
    for el in elements:
        name = el.inner_text().strip().replace("/", "")
        if name and name.lower() not in {"windows", "papers"} and name not in seen:
            folders.append(name)
            seen.add(name)
    return folders

with sync_playwright() as p:
    print("[DEBUG] Launching browser...")
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto(BASE_URL)
    page.wait_for_selector('div[phx-click*="change-directory"]')

    print("[DEBUG] Extracting folder list...")
    raw_folders = page.query_selector_all("div[phx-click*='change-directory']")
    folders = clean_folder_names(raw_folders)
    print(f"[DEBUG] {len(folders)} folders found: {folders}")

    for folder in folders:
        sub_url = f"{BASE_URL}{folder}/"
        print(f"\n[DEBUG] Accessing folder: {sub_url}")
        page.goto(sub_url)
        time.sleep(1)

        try:
            page.wait_for_selector("a[href$='.pdf']", timeout=7000)
            pdf_links = page.query_selector_all("a[href$='.pdf']")
        except PlaywrightTimeoutError:
            print(f"[ERROR] No PDFs found in '{folder}', skipping.")
            continue

        folder_path = os.path.join(OUTPUT_DIR, folder)
        os.makedirs(folder_path, exist_ok=True)

        for link in pdf_links:
            href = link.get_attribute("href")
            if not href:
                continue

            file_url = href if href.startswith("http") else sub_url + href.lstrip("/")
            file_name = os.path.basename(href)
            destination = os.path.join(folder_path, file_name)
            download_pdf(file_url, destination)

    browser.close()

print("\n[SUCCESS] All PDF downloads completed.")
