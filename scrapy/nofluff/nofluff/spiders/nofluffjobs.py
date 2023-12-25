import scrapy
import json
from scrapy.crawler import CrawlerProcess
from scrapy_playwright.page import PageMethod
from ..items import NofluffItem
import asyncio
from selenium import webdriver
from scrapy.http import HtmlResponse
from selenium.webdriver.chrome.options import Options


class NofluffJobsSpider(scrapy.Spider):
    name = "nofluffjobs"

    base_url = 'https://nofluffjobs.com'

    experience = {
        'student' : ['trainee', 'junior'],
        'junior' : ['junior', 'mid'],
        'mid' : ['mid', 'senior'],
        'senior' : ['expert', 'senior'],
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
    # as your query gets more specified.

    def __init__(self, *args, preset=None, **kwargs):
        super(NofluffJobsSpider, self).__init__(*args, **kwargs)
        self.language_category = set()
        self.preset = int(preset)
        self.experience_indicator = None
        self.handle_preset()

    def handle_preset(self):
        if self.preset == 1:
            self.experience_categories = self.get_input_categories('experience')
            self.language_category = self.get_language()
        elif self.preset == 2:
            self.experience_categories = self.get_input_categories('experience')
            self.department_categories = self.get_input_categories('department')

    def build_url(self):
        experience_part = ','.join(self.experience_categories)
        if self.preset == 1:
            url = f'{self.base_url}/?criteria=requirement%3D{self.language_category}%20seniority%3D{experience_part}'
        else:
            department_part = ','.join(self.department_categories)
            url = f'{self.base_url}/?criteria=category%3D{department_part}%20seniority%3D{experience_part}'
        return url

    def get_language(self):
        print(f"Available languages: {', '.join(sorted(self.language))}")
        while True:
            language_input = input("Enter language: ").strip()
            if language_input in self.language:
                return language_input
            else:
                print("Invalid language. Please try again.")

    def get_input_categories(self, category_type):
        available_categories = getattr(self, category_type, {})

        if category_type == 'experience':
            print("Available experience categories:")
            for key, values in available_categories.items():
                print(f"{key}: {', '.join(values)}")

            while True:
                category_input = input(f"Enter an {category_type} category: ").strip().lower()
                if category_input in available_categories:
                    self.category_indicator = category_input
                    return set(available_categories[category_input])
                else:
                    print(f"Invalid {category_type} category input. Please try again.")

        else:
            print(f"Available {category_type} categories: {', '.join(sorted(available_categories))}")
            categories = set()
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
                elif category_input in available_categories:
                    categories.add(category_input)
                else:
                    print(f"Invalid {category_type} category input. Please try again.")
            print("Selected categories:", categories)
            return categories

    def start_requests(self):
        url = self.build_url()
        yield scrapy.Request(url, callback=self.parse)

    async def parse(self, response):

        for job_link in response.css(
                'body > nfj-root > nfj-layout > nfj-main-content > div > nfj-postings-search > div > div > common-main-loader > nfj-search-results > nfj-postings-list > div.list-container.ng-star-inserted > a.posting-list-item::attr(href)').getall():
            full_url = self.base_url + job_link
            yield response.follow(job_link, self.parse_job_details, meta={'full_url': full_url})

        next_page_url = response.css('a[aria-label="Next"]::attr(href)').get()

        if next_page_url:
            full_url = self.base_url + next_page_url
            yield response.follow(full_url, self.parse)

    def parse_job_details(self, response):
        full_url = response.meta.get('full_url')

        title = response.css('#posting-header > div > div > h1::text').get()

        company = response.css('#postingCompanyUrl::text').get().strip()

        salary_range = response.css('h4.tw-mb-0::text').get().strip().replace('\xa0', ' ')


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
