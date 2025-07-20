import asyncio
from playwright.async_api import async_playwright

async def extract_and_sum(page, url):
    await page.goto(url)
    await page.wait_for_selector("table")
    tables = await page.query_selector_all("table")
    total = 0
    for table in tables:
        text = await table.inner_text()
        for word in text.split():
            try:
                total += int(word.replace(",", ""))
            except ValueError:
                continue
    return total

async def main():
    base_url = "https://sanand0.github.io/tdsdata/js_table/?seed={}"
    seeds = range(56, 66)  # Seeds 56 to 65

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        grand_total = 0
        for seed in seeds:
            url = base_url.format(seed)
            page_sum = await extract_and_sum(page, url)
            print(f"Seed {seed} total: {page_sum}")
            grand_total += page_sum

        print("✅ TOTAL SUM:", grand_total)

        await browser.close()

asyncio.run(main())
