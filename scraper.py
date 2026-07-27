from playwright.sync_api import sync_playwright

def scrape_gmaps_no_website(keyword, max_results=10):
    leads = []
    debug_log = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(f"https://www.google.com/maps/search/{keyword.replace(' ', '+')}")
        page.wait_for_selector('a[href*="/maps/place/"]', timeout=15000)
        page.wait_for_timeout(2000)

        listings = page.query_selector_all('a[href*="/maps/place/"]')[:max_results]

        listing_data = []
        for item in listings:
            name = item.get_attribute('aria-label') or "N/A"
            href = item.get_attribute('href')
            listing_data.append({"name": name, "href": href})

        for entry in listing_data:
            if not entry["href"]:
                continue

            page.goto(entry["href"])
            page.wait_for_timeout(3000)

            # --- Phone number: try a few possible selectors, since Google's
            # internal class names change over time ---
            phone = "N/A"
            phone_selectors = [
                'button[data-tooltip*="phone"]',
                'button[aria-label*="Phone"]',
                'button[data-item-id*="phone"]',
            ]
            for sel in phone_selectors:
                el = page.query_selector(sel)
                if el:
                    phone = (el.get_attribute('aria-label') or el.inner_text()).replace("Phone:", "").strip()
                    break

            # --- Website detection ---
            # Only count it as a real website if there's an actual link with a
            # genuine external href. Google shows a grayed-out "Add website"
            # suggestion button on listings that have NO website, and that
            # button's tooltip also happens to contain the word "website" —
            # so we check for a real http(s) link instead of matching on
            # tooltip text alone.
            found_website = False
            matched_href = None
            website_el = page.query_selector('a[data-item-id="authority"]')
            if website_el:
                href_val = website_el.get_attribute('href')
                if href_val and href_val.startswith('http'):
                    found_website = True
                    matched_href = href_val

            debug_log.append({
                "name": entry["name"],
                "phone": phone,
                "has_website": found_website,
                "matched_href": matched_href
            })

            if not found_website:
                leads.append({
                    "name": entry["name"],
                    "phone": phone,
                    "city": keyword.split()[-1]
