import scrapy
import json
from scrapy.crawler import CrawlerProcess
from scrapy_playwright.page import PageMethod
from ..items import NofluffItem


class NofluffJobsSpider(scrapy.Spider):
    name = "nofluffjobs"

    base_url = 'https://nofluffjobs.com'

    experience = {
        'trainee', 'junior', 'mid', 'senior', 'expert'
    }

    department = {
        'backend',
        'frontend', 'fullstack', 'mobile', 'embedded',
        'testing', 'devops', 'architecture', 'security',
        'game-dev', 'artificial-intelligence', 'data',
        'sys-administrator', 'agile', 'product-management',
        'project-manager', 'business-intelligence', 'ux',
        'support', 'erp', 'other'
        # https://nofluffjobs.com/?page=1&criteria=category%3Dbackend,frontend%20seniority%3Dtrainee,junior,mid,senior,expert
    }

    language = {
        'Java', 'React', 'Python', 'React native',
        '.NET', 'Angular', 'C#', 'Vue.js', 'SQL',
        'JavaScript', 'Golang', 'TypeScript', 'Scala',
        'HTML', 'Kotlin', 'PHP', 'C', 'Ruby', 'C++',
        'Ruby on Rails', 'Azure', 'Android', 'AWS',
        'iOS', 'Elixir', 'Flutter'
    }

    # language dict specifies tech you want to work with, so the more you specify the less lobs will be returned
    # as your query gets more specified.

    def __init__(self, *args, **kwargs):
        super(NofluffJobsSpider, self).__init__(*args, **kwargs)
        self.experience_categories = self.get_input_categories('experience')
        self.department_categories = self.get_input_categories('department')
        self.language_categories = self.get_input_categories('language')

    def get_input_categories(self, category_type):
        available_categories = getattr(self, category_type, set())
        categories = set()
        print(f"Available {category_type} categories: {', '.join(sorted(available_categories))}")
        while True:
            category_input = input(f"Enter a {category_type} category: ")
            if category_type != 'language':
                category_input = category_input.strip().lower()
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

    def start_requests(self):
        url = self.build_url()
        yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        for job_link in response.css('body > nfj-root > nfj-layout > nfj-main-content > div > nfj-postings-search > div > div > common-main-loader > nfj-search-results > nfj-postings-list > div.list-container.ng-star-inserted > a.posting-list-item::attr(href)').getall():
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

        salary_range = response.css('h4.tw-mb-0::text').get().strip().replace('\xa0', ' ')

        categories = response.css('div > aside > div > a')
        category_list = [element.css('::text').get().strip() for element in categories]

        must_have_elements = response.css('#posting-requirements > section:nth-child(1) > ul > li > span')
        must_have_main = [element.css('::text').get().strip() for element in must_have_elements]
        
        nice_tohave_elements = response.css('#posting-nice-to-have > ul > li > span')
        nice_tohave_main = [element.css('::text').get().strip() for element in nice_tohave_elements]


        item = NofluffItem(
            url=full_url,
            title=title,
            company=company,
            category=category_list,
            salary_range=salary_range,
            must_have_main=must_have_main,
            nice_tohave_main=nice_tohave_main,
        )

        item_dict = dict(item)
        formatted_json = json.dumps(item_dict, indent=4, ensure_ascii=False)
        self.logger.debug(formatted_json)
        yield item

    def build_url(self):
        experience_part = ','.join(self.experience_categories)
        department_part = ','.join(self.department_categories)
        language_part = ','.join(self.language_categories)
        if language_part != '':
            url = f'{self.base_url}/?criteria=requirement%3D{language_part}%20category%3D{department_part}%20seniority%3D{experience_part}'
        else:
            url = f'{self.base_url}/?criteria=category%3D{department_part}%20seniority%3D{experience_part}'
        return url
