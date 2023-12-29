import sys

sys.path.append('/JobHarvester/justjoinit')
sys.path.append('/JobHarvester/nofluff')
sys.path.append('/JobHarvester/theprotocol')

from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from scrapy.utils.project import get_project_settings

from justjoinit.justjoinit.spiders.joinit import JoinitSpider
from nofluff.nofluff.spiders.nofluffjobs import NofluffJobsSpider
from theprotocol.theprotocol.spiders.protocol import ProtocolSpider


if __name__ == "__main__":

    departament = {
        'backend': ['backend'],
        'frontend': ['frontend'],
        'fullstack': ['fullstack'],
        'mobile': ['mobile'],
        'embedded': ['embedded'],
        'testing': ['qa-testing', 'testing'],
        'devops': ['devops'],
        'architecture': ['architecture'],
        'security': ['security'],
        'gamedev': ['gamedev, game-dev'],
        'ai': ['ai-ml', 'artificial-intelligence'],
        'data': ['big-data-science', 'data'],
        'sys-administrator': ['sys-administrator', 'it-admin', 'system-analytics'],
        'agile': ['agile'],
        'product-management': ['product-management'],
        'project-manager': ['project-manager'],
        'bi': ['business-analytics''business-intelligence'],
        'ux': ['ux-ui'],
        'support': ['helpdesk', 'support'],
        'erp': ['sap-erp'],
        'other': ['other']
    }

    language = {
        'java': ['java', 'Java'],
        'javascript': ['javascript', 'JavaScript'],
        'python': ['python', 'Python'],
        'html': ['html', 'HTML'],
        'frontend': ['angular', 'Angular', 'Vue.js', 'React native', 'React', 'react.js'],
        'typescript': ['typescript', 'TypeScript'],
        'dotnet': ['.net', 'net', '.NET'],
        'mobile': ['android', 'mobile', 'ios', 'iOS', 'Flutter', 'Kotlin'],
        'sql': ['sql', 'SQL'],
        'c': ['c', 'C', 'c++', 'C%23', 'c%23'],
        'cloud': ['aws', 'AWS', 'Azure'],
        'go': ['go', 'Golang'],
        'ruby': ['ruby', 'Ruby on Rails', 'Ruby'],
        'scala': ['scala', 'Scala'],
        'php': ['php', 'PHP'],
        'elixir': ['Elixir'],
        'rust': ['rust '],
        'node': ['node.js'],
        'r': ['r']
    }

    user_language = None

    exp = ['student', 'junior', 'mid', 'senior']

    preset = input("Enter preset for spiders:")
    if int(preset) == 1:
        keys = ' '.join(language.keys())
        print(keys)
        while True:
            user_input = input("Enter a language: ").strip()
            if user_input in language:
                print(f"{user_input} inserted.")
                break
            else:
                print(f"Language not in dict.")

        values = language[user_input]
        for value in values:
            if value in NofluffJobsSpider.language:
                user_language = value
                break

    elif int(preset) == 2:
        keys = ' '.join(departament.keys())
        print(keys)
        while True:
            user_input = input("Enter a department: ").strip()
            if user_input in departament:
                print(f"{user_input} inserted.")
                break
            else:
                print(f"Department not in dict.")

        values = departament[user_input]
        for value in values:
            if value in NofluffJobsSpider.department:
                user_language = value
                break

    print(exp)
    while True:
        experience_level = input("Enter experience level:")
        if experience_level in exp:
            break

    process = CrawlerProcess(get_project_settings())

    process.crawl(NofluffJobsSpider, preset=preset, experience_level=experience_level, secondary_category=user_language)
    process.start()
