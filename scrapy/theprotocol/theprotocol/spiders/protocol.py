import scrapy
from scrapy_playwright.page import PageMethod


class ProtocolSpider(scrapy.Spider):
    name = "protocol"

    base_url = 'https://theprotocol.it'

    experience = {
        'trainee', 'assistant', 'junior', 'mid', 'senior', 'expert', 'lead', 'manager', 'head'
    }

    department = {
        'backend',
        'frontend', 'fullstack', 'mobile', 'embedded',
        'qa-testing', 'devops', 'architecture', 'security',
        'gamedev', 'ai-ml', 'big-data-science', 'helpdesk',
        'it-admin', 'agile', 'product-management',
        'project-manager', 'business-analytics', 'ux-ui',
        'sap-erp', 'system-analytics',
    }

    def __init__(self, *args, **kwargs):
        super(ProtocolSpider, self).__init__(*args, **kwargs)
        self.experience_categories = self.get_input_categories('experience')
        self.department_categories = self.get_input_categories('department')

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
        department_part = ','.join(self.department_categories)
        # language_part = ','.join(self.language_categories)
        # if language_part != '':
        url = f'{self.base_url}/filtry/{department_part};sp/{experience_part};p'
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
                               "section.lniiuf0 > div > div > div.l1785eyd > div")
                ],
            ),
            callback=self.parse
        )

    async def parse(self, response):
        if 'playwright_page' in response.meta:
            page = response.meta['playwright_page']
            await page.close()

            for item in response.css('section.lniiuf0 > div > div > div.l1785eyd > div > a'):
                url = item.css('::attr(href)').get()
                job_title = item.css('#offer-title::text').get()
                company = item.css('div.mainWrapper_mlnqt8l.GridElement_g16c3y1q > div > div > div::text').get()
                # salary_range_element = item.css('div > div > div > div > div > span.boldText_b1wsb650::text').get()
                # salary_range = salary_range_element if salary_range_element is not None else None
                # must_have_main = item.css(
                #     'div.section_s1lmyctb.GridElement_g16c3y1q > div > div > div > div > span::text').get()

                # item = ProtocolSpider(
                #     url=url,
                #     title=job_title,
                #     company=company,
                #     # category=category_list,
                #     salary_range=salary_range,
                #     must_have_main=must_have_main,
                #     # nice_tohave_main=nice_tohave_main,
                # )

                yield {
                    'url' : url,
                    'job_title': job_title,
                    'company': company,
                    # 'salary_range': salary_range,
                    # must_have_main: must_have_main
                }
