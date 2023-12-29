import scrapy
from scrapy_playwright.page import PageMethod
import time
from ..items import TheprotocolItem


class ProtocolSpider(scrapy.Spider):
    name = "protocol"

    base_url = 'https://theprotocol.it'


    experience = {
        'student': ['trainee', 'assistant', 'junior'],
        'junior': ['junior', 'mid'],
        'mid': ['mid', 'senior'],
        'senior': ['expert', 'senior', 'lead', 'head'],
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

    language = {
        'java', 'sql', 'rust', 'typescript',
        'ruby', 'react.js', 'r', 'python', 'php',
        'node.js', 'javascript', 'ios', 'html',
        'hibernate', 'go', 'c++', 'c%23', 'c', 'aws',
        'angular', 'android', '.net'
    }

    def __init__(self, *args, preset=None, **kwargs):
        super(ProtocolSpider, self).__init__(*args, **kwargs)
        if preset is not None:
            try:
                self.preset = int(preset)
            except ValueError:
                self.preset = None  # or handle the error as you see fit
        else:
            self.preset = None
        self.handle_preset()

    def handle_preset(self):
        if self.preset == 1:
            self.experience_categories = self.get_input_categories('experience')
            self.department_categories = self.get_input_categories('department')
            self.language_category = set()
        elif self.preset == 2:
            self.experience_categories = self.get_input_categories('experience')
            self.language_category = self.get_language()
            self.department_categories = set()

    def get_language(self):
        print(f"Available languages: {', '.join(sorted(self.language))}")
        while True:
            language_input = input("Enter language: ").strip().lower()
            if language_input in self.language:
                return language_input
            else:
                print("Invalid language. Please try again.")

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
        if self.preset == 1:
            url = f'{self.base_url}/filtry/{department_part};sp/{experience_part};p'
        else:
            url = f'{self.base_url}/filtry/{self.language_category};t/{experience_part};p'

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
                               "section.lniiuf0 > div > div > div.l1785eyd > div"),

                    PageMethod('wait_for_selector',
                               'div.DescriptionAndActions_d1jrj6mc > div.Actions_aa55f06 > button.button_b1cb9caz.button_b1qpzqhe.wrapper_w11iwtu0.primary_po2dfa.contained_c104vegi > div')
                ],
            ),
            callback=self.parse
        )

    async def parse(self, response):
        if 'playwright_page' in response.meta:
            page = response.meta['playwright_page']
            await page.close()
            processed_urls = set()
            for link in response.css('section.lniiuf0 > div > div > div.l1785eyd > div > a'):
                url = link.css('::attr(href)').get()
                full_url = self.base_url + url

                if full_url not in processed_urls:
                    processed_urls.add(full_url)

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

    async def parse_details(self, response):
        full_url = response.meta.get('full_url')
        page = response.meta['playwright_page']
        await page.close()

        job_title = response.css(
            '#offerHeader > div.headline_hrxluye.GridElement_g16c3y1q > div.titleBox_tk35js1.GridElement_g16c3y1q > h1::text').get()
        company = response.css(
            '#offerHeader > div.headline_hrxluye.GridElement_g16c3y1q > div.titleBox_tk35js1.GridElement_g16c3y1q > h2 > a::text').get()

        must_have_elements = response.css(
            '#TECHNOLOGY_AND_POSITION > div:nth-child(1) > div:nth-child(2) > div > div > span')
        must_have_main = list(set([element.css('::text').get().strip() for element in must_have_elements]))

        salary_parts = response.css('p.SalaryInfo_s6hpd6f::text').getall()
        if salary_parts:
            full_salary_text = ''.join(salary_parts).strip()
            full_salary_text = full_salary_text.replace(u'\xa0', u' ')
            salary_range = full_salary_text
        else:
            salary_range = "Not found"

        nice_tohave_elements = response.css(
            '#TECHNOLOGY_AND_POSITION > div:nth-child(1) > div:nth-child(3) > div > div > span')
        nice_tohave_main = list(set([element.css('::text').get().strip() for element in nice_tohave_elements]))

        detailed_requirements = response.css('#TECHNOLOGY_AND_POSITION > div:nth-child(3) > ul > li > span > div')
        detailed_list = list(set([element.css('::text').get().strip() for element in detailed_requirements]))

        item = TheprotocolItem(
            url=full_url,
            title=job_title,
            company=company,
            salary_range=salary_range,
            must_have_main=must_have_main,
            nice_tohave_main=nice_tohave_main,
        )

        yield item
