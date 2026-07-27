from playwright.sync_api import sync_playwright

def scrape_gmaps_no_website(keyword, max_results=10):
    leads = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(f"https://www.google.com/maps/search/{keyword.replace(' ', '+')}")
        page.wait_for_selector('a[href*="/maps/place/"]', timeout=15000)
        page.wait_for_timeout(2000)

        listings = page.query_selector_all('a[href*="/maps/place/"]')[:max_results]

        # Grab names directly from the list view (more reliable than the detail page)
        listing_data = []
        for item in listings:
            name = item.get_attribute('aria-label') or "N/A"
            href = item.get_attribute('href')
            listing_data.append({"name": name, "href": href})

        for entry in listing_data:
            if not entry["href"]:
                continue

            page.goto(entry["href"])
            page.wait_for_timeout(3000)  # give the detail panel time to fully load

            # Try several possible selectors for phone, since Google's class names change often
            phone = "N/A"
            phone_selectors = [
                'button[data-tooltip*="phone"]',
                'button[aria-label*="Phone"]',
                'button[data-item-id*="phone"]',
            ]
            for sel in phone_selectors:
                el = page.query_selector(sel)
                if el:
                    phone = el.get_attribute('aria-label') or el.inner_text()
                    phone = phone.replace("Phone:", "").strip()
                    break

            # Try several possible selectors for a website link
            website = None
            website_selectors = [
                'a[data-tooltip*="website"]',
                'a[aria-label*="Website"]',
                'a[data-item-id="authority"]',
            ]
            for sel in website_selectors:
                website = page.query_selector(sel)
                if website:
                    break

            if not website:
                leads.append({
                    "name": entry["name"],
                    "phone": phone,
                    "city": keyword.split()[-1]
                })

        browser.close()
    return leads
