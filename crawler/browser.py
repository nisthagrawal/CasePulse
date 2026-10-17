import logging
from contextlib import async_contextmanager
from playwright.async_api import async_playwright, Browser, BrowserContext, Page

logger = logging.getLogger(__name__)

ECOURTS_UTTARAKHAND_URL = "https://hcservices.ecourts.gov.in/ecourtindiaHC/index_highcourt.php?state_cd=15&dist_cd=1&stateNm=Uttarakhand"
ECOURTS_ORDER_DATE_URL = "https://hcservices.ecourts.gov.in/ecourtindiaHC/cases/s_orderdate.php?court_code=1&dist_cd=1&stateNm=Uttarakhand%2F1000&state_cd=15"

class BrowserManager:
    def __init__(self, headless: bool = False):
        self.headless = headless
        self.playwright = None
        self.browser: Browser = None
        self.context: BrowserContext = None
        self.page: Page = None

    async def start(self):
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(
            headless=self.headless,
            args=["--no-sandbox", "--disable-setuid-sandbox"]
        )
        self.context = await self.browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        self.page = await self.context.new_page()
        return self.page

    async def stop(self):
        if self.context:
            await self.context.close()
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()

@async_contextmanager
async def get_browser_page(headless: bool = False):
    bm = BrowserManager(headless=headless)
    page = await bm.start()
    try:
        yield page
    finally:
        await bm.stop()
