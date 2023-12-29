import scrapy
import json

from ..items import NofluffItem


class NofluffJobsSpider(scrapy.Spider):
    name = "nofluffjobs"

    base_url = 'https://nofluffjobs.com'

    experience_mapping = {
        'student': ['trainee', 'junior'],
        'junior': ['junior', 'mid'],
        'mid': ['mid', 'senior'],
        'senior': ['expert', 'senior'],
    }

    department = {
        'backend',
        'frontend', 'fullstack', 'mobile', 'embedded',
        'testing', 'devops', 'architecture', 'security',
        'game-dev', 'artificial-intelligence', 'data',
        'sys-administrator', 'agile', 'product-management',
        'project-manager', 'business-intelligence', 'ux',
        'support', 'erp', 'other'
    }

    language = {
        'Java', 'React', 'Python', 'React native',
        '.NET', 'Angular', 'C%23', 'Vue.js', 'SQL',
        'JavaScript', 'Golang', 'TypeScript', 'Scala',
        'HTML', 'Kotlin', 'PHP', 'C', 'Ruby', 'C++',
        'Ruby on Rails', 'Azure', 'Android', 'AWS',
        'iOS', 'Elixir', 'Flutter'
    }

    # language dict specifies tech you want to work with, so the more you specify the less lobs will be returned
    # that's why I've decided to enable selecting only one language

    def __init__(self, *args, preset=None, experience_level=None, secondary_category=None, **kwargs):
        super(NofluffJobsSpider, self).__init__(*args, **kwargs)
        self.preset = int(preset)
        self.experience_categories = self.experience_mapping.get(experience_level)
        self.secondary_categories = secondary_category

    def build_url(self):
        experience_part = ','.join(self.experience_categories)
        if self.preset == 1:
            url = f'{self.base_url}/?criteria=requirement%3D{self.secondary_categories}%20seniority%3D{experience_part}'
        else:
            url = f'{self.base_url}/?criteria=category%3D{self.secondary_categories}%20seniority%3D{experience_part}'
        return url

    def start_requests(self):
        url = self.build_url()
        yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):

        for job_link in response.css(
                'body > nfj-root > nfj-layout > nfj-main-content > div > nfj-postings-search > div > div > common-main-loader > nfj-search-results > nfj-postings-list > div.list-container > a.posting-list-item::attr(href)').getall():
            full_url = self.base_url + job_link
            yield response.follow(job_link, self.parse_job_details, meta={'full_url': full_url})

        next_page_url = response.css('a[aria-label="Next"]::attr(href)').get()

        if next_page_url:
            full_url = self.base_url + next_page_url
            yield response.follow(full_url, self.parse)

    def parse_job_details(self, response):
        full_url = response.meta.get('full_url')

        title = response.css('#posting-header > div > div > h1::text').get().strip()

        company = response.css('#postingCompanyUrl::text').get().strip()

        salary_elements = response.css('common-posting-salaries-list > div > h4.tw-mb-0::text').getall()
        salary_range = ' '.join(salary_elements).strip()
        salary_range = salary_range.replace(',', '').replace('\xa0', ' ')

        # salary_range = response.css('h4.tw-mb-0::text').get().strip().replace('\xa0', ' ')

        must_have_elements = response.css('#posting-requirements > section:nth-child(1) > ul > li > span')
        must_have_main = [element.css('::text').get().strip() for element in must_have_elements]

        nice_tohave_elements = response.css('#posting-nice-to-have > ul > li > span')
        nice_tohave_main = [element.css('::text').get().strip() for element in nice_tohave_elements]

        item = NofluffItem(
            url=full_url,
            title=title,
            company=company,
            salary_range=salary_range,
            must_have_main=must_have_main,
            nice_tohave_main=nice_tohave_main,
        )

        item_dict = dict(item)
        formatted_json = json.dumps(item_dict, indent=4, ensure_ascii=False)
        self.logger.debug(formatted_json)
        yield item
