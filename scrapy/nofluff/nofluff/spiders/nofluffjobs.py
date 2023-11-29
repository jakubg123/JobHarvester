import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy_playwright.page import PageMethod


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

    def __init__(self, *args, **kwargs):
        super(NofluffJobsSpider, self).__init__(*args, **kwargs)
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

    def start_requests(self):
        url = self.build_url()
        yield scrapy.Request(url, callback=self.parse)


    def parse(self, response):
        element = response.css('body > nfj-root > nfj-layout > nfj-main-content > div > nfj-postings-search > div > div > common-main-loader > nfj-search-results > nfj-postings-list > div.list-container.ng-star-inserted > a.posting-list-item')
        for item in element:
            href = item.attrib['href']
            full_link = f'{self.base_url}{href}'
            yield {
                'link': full_link
            }
        next_page_url = response.css('a[aria-label="Next"]::attr(href)').get()

        if next_page_url:
            full_url = self.base_url + next_page_url
            yield response.follow(full_url, self.parse)

    def build_url(self):
        experience_part = ','.join(self.experience_categories)
        department_part = ','.join(self.department_categories)
        url = f'{self.base_url}/?criteria=category%3D{department_part}%20seniority%3D{experience_part}'
        return url
