import scrapy
from scrapy_playwright.page import PageMethod
from ..items import JustjoinitItem
import asyncio


class JoinitSpider(scrapy.Spider):
    name = "joinit"
    base_url = 'https://justjoin.it'

    custom_settings = {
        'CONCURRENT_REQUESTS': 16
    }

    experience_mapping = {
        'student': ['junior'],
        'junior': ['junior', 'mid'],
        'mid': ['mid', 'senidor'],
        'senior': ['senior', 'c-level'],
    }

    department = {
        'javascript',
        'html', 'php', 'ruby', 'python',
        'java', 'net', 'scala', 'c',
        'mobile', 'testing', 'devops', 'admin',
        'ux', 'pm', 'game',
        'analytics', 'security', 'data',
        'go', 'support', 'erp', 'architecture', 'other'
    }


    def __init__(self, *args, universal_category=None, preset=None, experience_level=None, secondary_category=None,
                 date, **kwargs):
        super(JoinitSpider, self).__init__(*args, **kwargs)
        self.experience_level = experience_level
        self.preset = int(preset)  ## just to standarize it for the pipeline
        self.experience_categories = self.experience_mapping.get(experience_level)
        self.secondary_categories = secondary_category
        self.date = date
        self.universal_category = universal_category

    def build_url(self):
        experience_part = ','.join(self.experience_categories)
        url = f'{self.base_url}/all-locations/{self.secondary_categories}/experience-level_{experience_part}'
        return url

    def start_requests(self):
        url = self.build_url()
        yield scrapy.Request(
            url,
            meta=dict(
                playwright=True,
                playwright_include_page=True,
                playwright_page_methods=[
                    PageMethod("wait_for_selector",
                               "#__next > div.MuiBox-root.css-1v89lmg > div.css-c4vap3 > div > div.MuiBox-root.css-1fmajlu > div > div")
                    #
                ],
            ),
            callback=self.parse
        )

    async def parse(self, response):
        if 'playwright_page' in response.meta:
            page = response.meta['playwright_page']
            processed_urls = set()
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight);")
            await asyncio.sleep(4)

            for row in response.css(
                    '#__next > div.MuiBox-root.css-1v89lmg > div.css-c4vap3 > div > div.MuiBox-root.css-1fmajlu > div > div > div > div > div > div > div > div'):
                url = row.css('a::attr(href)').get()
                title = row.css('div > div > h2::text').get()
                company = row.css('div > div.MuiBox-root > div.MuiBox-root > div > div > span ::text').get()
                full_url = self.base_url + url
                salary_spans = row.css(
                    'div.css-6u2lxy > div.MuiBox-root.css-6vg4fr > div > div.css-1b2ga3v > span::text').getall()

                if salary_spans and len(salary_spans) > 2:
                    salary_range = f"{salary_spans[0]} - {salary_spans[1]} {salary_spans[2]}"
                elif len(salary_spans) == 2:
                    salary_range = f"{salary_spans[0]} {salary_spans[1]}"
                else:
                    salary_range = 'Unknown'

                combined_string = company.replace(' ', '_') + '_' + title.replace(' ', '_')
                item_id = combined_string.lower()

                # category = self.department + ',' + ','.join(self.experience_categories)

                if full_url not in processed_urls:
                    processed_urls.add(full_url)

                    item = JustjoinitItem(
                        item_id=item_id,
                        date=self.date,
                        url=full_url,
                        title=title,
                        company=company,
                        # category=category,
                        salary_range=salary_range,
                    )

                    yield item

            await page.close()
