import scrapy
from scrapy_playwright.page import PageMethod
import time
from ..items import TheprotocolItem


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
            processed_urls = set()  # Set to track processed URLs
            for link in response.css('section.lniiuf0 > div > div > div.l1785eyd > div > a'):
                url = link.css('::attr(href)').get()
                full_url = self.base_url + url

                if full_url not in processed_urls:
                    processed_urls.add(full_url)  # Add URL to the set

                    yield response.follow(link, self.parse_details, meta={
                        'full_url': full_url,
                        'playwright': True,
                        'playwright_include_page': True,
                        'playwright_page_methods': [

                            # PageMethod("wait_for_selector",
                            #            "#__next > div > div.c1kpnzt5.GridElement_g16c3y1q > div > div > div:nth-child(1) "
                            #            "> div:nth-child(2) > div > aside > div > div:nth-child(2) > "
                            #            "div.DescriptionAndActions_d1jrj6mc > div.Actions_aa55f06 > "
                            #            "button.button_b1cb9caz.button_b1qpzqhe.wrapper_w11iwtu0.primary_po2dfa"
                            #            ".contained_c104vegi > div"),

                            # PageMethod("click",
                            #            "#__next > div > div.c1kpnzt5.GridElement_g16c3y1q > div > div > div:nth-child(1) "
                            #            "> div:nth-child(2) > div > aside > div > div:nth-child(2) > "
                            #            "div.DescriptionAndActions_d1jrj6mc > div.Actions_aa55f06 > "
                            #            "button.button_b1cb9caz.button_b1qpzqhe.wrapper_w11iwtu0.primary_po2dfa"
                            #            ".contained_c104vegi > div"),

                            PageMethod("wait_for_selector",
                                       "#offerHeader"),
                            # PageMethod('wait_for_selector',
                            #            '__next > div > div.c1kpnzt5.GridElement_g16c3y1q > div > div > div > div > div > div > div > div > div.mainWrapperClass_m104iqca'),
                            PageMethod('wait_for_selector',
                                       '#TECHNOLOGY_AND_POSITION'),
                        ],
                    })

                # job_title = item.css('#offer-title::text').get()
                # company = item.css('div.mainWrapper_mlnqt8l.GridElement_g16c3y1q > div > div > div::text').get()
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

                # yield {
                #     'url' : url,
                #     'job_title': job_title,
                #     'company': company,
                # 'salary_range': salary_range,
                # must_have_main: must_have_main
                # }

    async def parse_details(self, response):
        full_url = response.meta.get('full_url')
        page = response.meta['playwright_page']

        await page.close()

        job_title = response.css(
            '#offerHeader > div.headline_hrxluye.GridElement_g16c3y1q > div.titleBox_tk35js1.GridElement_g16c3y1q > h1::text').get()
        company = response.css(
            '#offerHeader > div.headline_hrxluye.GridElement_g16c3y1q > div.titleBox_tk35js1.GridElement_g16c3y1q > h2 > a::text').get()

        # Extract unique must-have elements
        must_have_elements = response.css('#TECHNOLOGY_AND_POSITION > div > div > div > div > span')
        must_have_main = list(set([element.css('::text').get().strip() for element in must_have_elements]))

            # item = ProtocolSpider(
            # url=url,
            # title=job_title,
            # company=company,
            # # category=category_list,
            # salary_range=salary_range,
            # must_have_main=must_have_main,
            # # nice_tohave_main=nice_tohave_main,

        yield {
            'url': full_url,
            'job_title': job_title,
            'company': company,
            'must_have_main': must_have_main
        }
