from urllib.parse import urljoin
from playwright.sync_api import sync_playwright
import json
import traceback
import time

# Base URL used to convert relative paths into absolute URLs
BASE_URL = "https://ekantipur.com"

def make_absolute_url(url: str | None) -> str | None:
    """
    Convert relative or partial URLs into absolute URLs.
    Returns None if URL is missing.
    """
    if not url:
        return None
    return urljoin(BASE_URL, url)

print("SCRIPT STARTED")

try:
    with sync_playwright() as p:
        # Launch Chromium browser (visible + slow for recording)
        browser = p.chromium.launch(headless=False, slow_mo=800)
        page = browser.new_page()

        # ---------------- HOME PAGE ----------------
        page.goto(BASE_URL)
        page.wait_for_load_state("load", timeout=10000)
        print("HOME PAGE LOADED")
        time.sleep(2)

        # ---------------- ENTERTAINMENT SECTION ----------------
        print("CLICKING ENTERTAINMENT SECTION")
        page.click("text=मनोरञ्जन")
        page.wait_for_load_state("networkidle")
        page.wait_for_selector("article h2", timeout=10000)
        print("ENTERTAINMENT PAGE LOADED")

        # 🔽 Visible scrolling (for demo & lazy loading)
        for _ in range(3):
            page.mouse.wheel(0, 800)
            time.sleep(1)

        time.sleep(3)  # pause so you can explain in video

        # Extract category name dynamically
        category_el = page.locator("h1").first
        category_name = (
            category_el.text_content().strip()
            if category_el.count() > 0
            else None
        )

        # Locate article cards
        cards = page.locator("article")
        total_articles = cards.count()
        print("TOTAL ARTICLES FOUND:", total_articles)

        # Extract top 5 articles
        top_n = min(total_articles, 5)
        entertainment_news = []

        for i in range(top_n):
            card = cards.nth(i)
            print(f"Extracting article {i + 1}/{top_n}")

            title_el = card.locator("h2").first
            img_el = card.locator("img").first
            author_el = card.locator(".author").first

            raw_img = None
            if img_el.count() > 0:
                raw_img = (
                    img_el.get_attribute("src")
                    or img_el.get_attribute("data-src")
                    or img_el.get_attribute("data-original")
                )

            entertainment_news.append({
                "title": title_el.text_content().strip() if title_el.count() > 0 else None,
                "image_url": make_absolute_url(raw_img),
                "category": category_name,
                "author": author_el.text_content().strip() if author_el.count() > 0 else None
            })

        print("ENTERTAINMENT DATA EXTRACTED")

        # ---------------- BACK TO HOME PAGE ----------------
        page.goto(BASE_URL)
        page.wait_for_load_state("load", timeout=10000)
        print("BACK TO HOME PAGE")
        time.sleep(2)

        # ---------------- CARTOON SECTION ----------------
        print("CLICKING CARTOON SECTION")
        page.click("text=कार्टुन")
        time.sleep(3)  # visible click for recording

        cartoon_heading = page.locator("text=कार्टुन").first
        cartoon_section = cartoon_heading.locator("xpath=ancestor::section[1]")

        if cartoon_section.count() > 0:
            cartoon_section = cartoon_section.first

            title_el = cartoon_section.locator("h2").first
            img_el = cartoon_section.locator("img").first
            author_el = cartoon_section.locator(".author").first

            raw_img = None
            if img_el.count() > 0:
                raw_img = (
                    img_el.get_attribute("src")
                    or img_el.get_attribute("data-src")
                    or img_el.get_attribute("data-original")
                )

            cartoon = {
                "title": title_el.text_content().strip() if title_el.count() > 0 else None,
                "image_url": make_absolute_url(raw_img),
                "author": author_el.text_content().strip() if author_el.count() > 0 else None
            }
        else:
            cartoon = {"title": None, "image_url": None, "author": None}

        print("CARTOON DATA EXTRACTED")

        # ---------------- WRITE OUTPUT ----------------
        output = {
            "entertainment_news": entertainment_news,
            "cartoon_of_the_day": cartoon
        }

        with open("output.json", "w", encoding="utf-8") as f:
            json.dump(output, f, ensure_ascii=False, indent=2)

        print("FILE SAVED SUCCESSFULLY ✅")
        time.sleep(2)
        browser.close()

except Exception:
    print("SCRIPT FAILED ❌")
    traceback.print_exc()
