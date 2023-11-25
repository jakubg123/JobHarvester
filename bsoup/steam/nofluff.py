import requests
from bs4 import BeautifulSoup


class Scraper:
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
            if category_input in available_categories:
                categories.add(category_input)
            else:
                print(f"Wrong category input, {category_type}.")
        return categories

    def build_url(self):
        base_url = 'https://nofluffjobs.com/'
        experience_part = ','.join(self.experience_categories)
        department_part = ','.join(self.department_categories)
        url = f'{base_url}?criteria=category%3D{department_part}%20seniority%3D{experience_part}'
        print(url)
        return url

    def get_data(self, url):
        req = requests.get(url)
        data = req.text
        return data


# url = 'https://nofluffjobs.com/backend?criteria=category%3Dfrontend,fullstack,mobile,embedded,artificial-intelligence,data,product-management,business-intelligence,business-analyst%20seniority%3Dtrainee,junior'
# data = get_data(url)
# 
# soup = BeautifulSoup(data, "html.parser")
# 
# elements_with_class = soup.select(
#     'body > nfj-root > nfj-layout > nfj-main-content > div > nfj-postings-search > div > div > common-main-loader > nfj-search-results > div > nfj-pagination > ul')
# 
# 
# for item in elements_with_class:
#     print(item.text)

scraper = Scraper()
url = scraper.build_url()
data = scraper.get_data(url)

soup = BeautifulSoup(data, 'html.parser')
sites = soup.select('body > nfj-root > nfj-layout > nfj-main-content > div > nfj-postings-search > div > div > common-main-loader > nfj-search-results > div > nfj-pagination > ul > li')
sites_length = len(sites)

for page in range(1, sites_length):





