import scrapy
from scrapy_playwright.page import PageMethod
from ..items import JustjoinitItem
import asyncio


class JoinitSpider(scrapy.Spider):
    name = "joinit"
    base_url = 'https://justjoin.it'

    experience = {
        'junior', 'mid', 'senior', 'c-level'
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

    def __init__(self, *args, **kwargs):
        super(JoinitSpider, self).__init__(*args, **kwargs)
        self.department = self.get_department_input()
        self.experience_categories = self.get_input_categories('experience')

    def get_department_input(self):
        print(f"Available departments: {', '.join(sorted(self.department))}")
        while True:
            department_input = input("Enter a department: ").strip().lower()
            if department_input in self.department:
                return department_input
            else:
                print("Invalid department. Please try again.")

    def get_input_categories(self, category_type):
        available_categories = getattr(self, category_type, set())
        categories = set()
        print(f"Available {category_type} categories: {', '.join(sorted(available_categories))}")
        while True:
            category_input = input(f"Enter a {category_type} category: ").strip().lower()
            if category_input == 'done':
                break
            elif category_input == 'all':
                categories = available_categories.copy()
                break
            elif category_input == 'exclude':
                exclude_input = input(f"Enter categories to exclude (comma-separated): ").strip().lower().split(',')
                categories.update(available_categories - set(exclude_input))
            if category_input in available_categories:
                categories.add(category_input)
            else:
                print(f"Wrong category input, {category_type}.")
        print(categories)
        return categories

    def build_url(self):
        experience_part = ','.join(self.experience_categories)
        url = f'{self.base_url}/all-locations/{self.department}/experience-level_{experience_part}'
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

                category = self.department + ',' + ','.join(self.experience_categories)

                if full_url not in processed_urls:
                    processed_urls.add(full_url)

                    item = JustjoinitItem(
                        url=full_url,
                        title=title,
                        company=company,
                        category=category,
                        salary_range=salary_range,
                    )

                    yield item

            await page.close()
