import asyncio
from playwright.async_api import async_playwright

# Seed URLs (example pattern)
seeds = list(range(56, 66))
base_url = "https://example.com/seed{}"  # replace with actual prefix

async def extract_and_sum(page, url):
    await page.goto(url)
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
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        total_sum = 0
        for seed in seeds:
            url = base_url.format(seed)
            sum_seed = await extract_and_sum(page, url)
            print(f"Seed {seed} sum: {sum_seed}")
            total_sum += sum_seed
        print("✅ TOTAL SUM:", total_sum)
        await browser.close()

asyncio.run(main())
