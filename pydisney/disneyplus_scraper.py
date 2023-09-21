from playwright.sync_api import sync_playwright, Route

class DSNY_Scraper:
    def __init__(self):
        self.scraped_url = None

    def login(self, email, password, url):
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto("https://www.disneyplus.com/it-it/login")
            page.locator("#email").type(email)
            page.locator("[data-testid='login-continue-button']").click()
            page.locator("#password").type(password)
            page.locator("[data-testid='password-continue-login']").click()
            page.locator("[data-testid='profile-avatar-0']").click()
            page.wait_for_timeout(500)
            page.goto(url)
            page.route("**/v7/playback/**", self.handle_route)
            
            while self.scraped_url is None:
                page.wait_for_timeout(500)

            browser.close()
            return self.scraped_url

    def handle_route(self, route: Route) -> None:
        # Fetch original response.
        response = route.fetch()
        # Add a prefix to the title.
        body = response.json()
        self.scraped_url = (body['stream']['sources'][0]['complete']['url'])
