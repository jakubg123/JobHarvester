import scrapy
from scrapy_playwright.page import PageMethod
from ..items import JustjoinitItem


class SolidjobsSpider(scrapy.Spider):
    name = "solidjobs"
    
    base_url = 'https://solid.jobs'

    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'JobHarvester.middlewares.RandomUserAgentMiddleware': None,
        },
        'ITEM_PIPELINES': {
            'JobHarvester.pipelines.MongoPipeline': None,
        }

    }

    experience_mapping = {
        'student': ['Staż', 'Junior'],
        'junior': ['Junior', 'Regular'],
        'mid': ['Regular', 'Senior'],
        'senior': ['Senior']
    }

    department = {
        'Programista',
        'Tester', 'Architekt', 'Analityk', 'Administrator',
        'DevOps', 'Support', 'Security', 'Data%20Science',
        'UX%2FUI%20Designer', 'Manager%2FAgile', 'Rekruter',
        'Pozostali%20specjaliści%20IT'  # niezla strona  czyWybranoPsa() pdk
    }

    language = {
        'JavaScript', 'Python', '.NET', 'Java',
        'PHP', 'Android', 'iOS', 'Scala', 'Ruby',
        'C%2FC%2B%2B', 'Angular', 'React', 'React',
        'Golang', 'Pozostali%20programiści'
    }

    def __init__(self, *args, universal_category=None, preset=None, experience_level=None, secondary_category=None,date, **kwargs):
        super(SolidjobsSpider, self).__init__(*args, **kwargs)
        self.experience_level = experience_level
        self.preset = int(preset)
        self.experience_categories = self.experience_mapping.get(experience_level)
        self.secondary_categories = secondary_category
        self.date = date
        self.universal_category = universal_category

    def build_url(self):
        if int(self.preset) == 1:
            pass
        else:
            url = f'https://solid.jobs/offers/it;experiences={self.experience_categories};subcategories={self.secondary_categories}'
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
                               "body > app-root > mat-sidenav-container > mat-sidenav-content > div > main > div > div.body-content.px-0.px-lg-3.order-lg-12.col-12.col-lg-9.col-xl-10 > app-offer-list > div > div.col-12.col-xl-7.px-2 > div > virtual-scroller > div.scrollable-content > div:nth-child(1)")
                ],
            ),
            callback=self.parse
        )

    async def parse(self, response):
        if 'playwright_page' in response.meta:
            page = response.meta['playwright_page']
            await page.close()
        for job in response.css('div.scrollable-content > div:nth-child(1) > offer-list-item'):
            title = job.css('div.align-self-start.mb-auto > h2 > a::text').get()
            company = job.css('a.mat-tooltip-trigger.mr-1.color-dark-grey.color-blue-onhover::text').get()
            salary = job.css('div.font-weight-500.d-flex.mb-s > a::text').get()
            url = job.css('div.align-self-start.mb-auto > h2 > a::attr(href)').get()

            full_url = self.base_url + url

            title = title.strip().replace(u'\xa0', u' ') if title else title
            company = company.strip().replace(u'\xa0', u' ') if company else company
            salary = salary.strip().replace(u'\xa0', u' ') if salary else salary

            combined_string = company.replace(' ', '_') + '_' + title.replace(' ', '_')
            item_id = combined_string.lower()

            item = JustjoinitItem(
                item_id=item_id,
                date=self.date,
                url=full_url,
                title=title,
                company=company,
                salary_range=salary,
            )

            yield item
