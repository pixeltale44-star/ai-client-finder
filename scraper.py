from playwright.sync_api import sync_playwright

def scrape_gmaps_no_website(keyword, max_results=10):
    leads = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(f"https://www.google.com/maps/search/{keyword.replace(' ', '+')}")
        page.wait_for_selector('a[href*="/maps/place/"]')

        listings = page.query_selector_all('a[href*="/maps/place/"]')[:max_results]

        for item in listings:
            item.click()
            page.wait_for_timeout(2000)

            name_el = page.query_selector('h1')
            name = name_el.inner_text() if name_el else "N/A"

            phone_el = page.query_selector('button[data-tooltip*="phone"]')
            phone = phone_el.inner_text() if phone_el else "N/A"

            website = page.query_selector('a[data-tooltip*="website"]')

            if not website:
                leads.append({
                    "name": name,
                    "phone": phone,
                    "city": keyword.split()[-1]
                })

        browser.close()
    return leads
