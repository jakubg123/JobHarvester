import scrapy


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


    def parse(self, response):
        pass
