from typing import Optional, List
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from JobHarvester.spiders.nofluffjobs import NofluffJobsSpider
from JobHarvester.spiders.protocol import ProtocolSpider
from JobHarvester.spiders.joinit import JoinitSpider
from JobHarvester.spiders.solidjobs import SolidjobsSpider
from datetime import datetime


def get_user_input(prompt: str, valid_options: List[str]) -> str:
    while True:
        user_input = input(prompt).strip()
        if user_input in valid_options:
            print(f"{user_input} inserted.")
            return user_input
        else:
            print(f"Invalid choice.")


def main():
    department = {
        'backend': ['backend'],
        'frontend': ['frontend'],
        'fullstack': ['fullstack'],
        'mobile': ['mobile'],
        'embedded': ['embedded'],
        'testing': ['qa-testing', 'testing','Tester'],
        'devops': ['devops','DevOps'],
        'architecture': ['architecture','Architekt'],
        'security': ['security','Security'],
        'gamedev': ['gamedev, game-dev'],
        'ai': ['ai-ml', 'artificial-intelligence'],
        'data': ['big-data-science', 'data','Analityk','Data%20Science'],
        'sys-administrator': ['sys-administrator', 'it-admin', 'system-analytics','Administrator'],
        'agile': ['agile','Manager%2FAgile'],
        'product-management': ['product-management'],
        'project-manager': ['project-manager','Manager%2FAgile'],
        'bi': ['business-analytics','business-intelligence','Analityk'],
        'ux': ['ux-ui','UX%2FUI%20Designer'],
        'support': ['helpdesk', 'support'],
        'erp': ['sap-erp'],
        'other': ['other','Pozostali%20specjaliści%20IT']
    }

    language = {
        'java': ['java', 'Java'],
        'javascript': ['javascript', 'JavaScript'],
        'python': ['python', 'Python'],
        'html': ['html', 'HTML'],
        'frontend': ['angular', 'Angular', 'Vue.js', 'React native', 'React', 'react.js'],
        'typescript': ['typescript', 'TypeScript'],
        'dotnet': ['.net', 'net', '.NET'],
        'mobile': ['android', 'Android', 'mobile', 'ios', 'iOS', 'Flutter', 'Kotlin'],
        'sql': ['sql', 'SQL'],
        'c': ['c', 'C', 'c++', 'C%23', 'c%23','C%2FC%2B%2B'],
        'cloud': ['aws', 'AWS', 'Azure'],
        'go': ['go', 'Golang'],
        'ruby': ['ruby', 'Ruby on Rails', 'Ruby'],
        'scala': ['scala', 'Scala'],
        'php': ['php', 'PHP'],
        'elixir': ['Elixir'],
        'rust': ['rust '],
        'node': ['node.js','Node.js'],
        'r': ['r']
    }

    current_date = datetime.now().strftime("%Y-%m-%d")

    experience_levels = ['student', 'junior', 'mid', 'senior']

    preset_choice = int(input("Enter preset for spiders (1 or 2): "))
    categories = None
    Joinit_category = None

    if preset_choice == 1:
        print(list(language.keys()))
        language_choice = get_user_input("Enter a language: ", list(language.keys()))
        categories = language[language_choice]
        for category in categories:
            if category in NofluffJobsSpider.language:
                Nofluff_category = category
            if category in ProtocolSpider.language:
                Protocol_category = category
            if category in JoinitSpider.department:
                Joinit_category = category
            if category in SolidjobsSpider.language:
                Solidjobs_category = category

    elif preset_choice == 2:
        print(list(department.keys()))
        department_choice = get_user_input("Enter a department: ", list(department.keys()))
        categories = department[department_choice]
        for category in categories:
            if category in NofluffJobsSpider.department:
                Nofluff_category = category
            if category in ProtocolSpider.department:
                Protocol_category = category
            if category in JoinitSpider.department:
                Joinit_category = category
            if category in SolidjobsSpider.department:
                Solidjobs_category = category

    print(f"Available experience categories:{experience_levels}")
    experience_level = get_user_input("Enter experience level: ", experience_levels)

    if preset_choice == 1:
        universal = language_choice
    else:
        universal = department_choice

    process = CrawlerProcess(get_project_settings())
    if Nofluff_category is not None:
        process.crawl(NofluffJobsSpider, universal_category=universal, preset=preset_choice,
                  experience_level=experience_level,
                  secondary_category=Nofluff_category, date=current_date)
    if Protocol_category is not None:
        process.crawl(ProtocolSpider, universal_category=universal, preset=preset_choice, experience_level=experience_level,
                  secondary_category=Protocol_category, date=current_date)

    if Joinit_category is not None:
        process.crawl(JoinitSpider, universal_category=universal, preset=preset_choice,
                      experience_level=experience_level,
                      secondary_category=Joinit_category, date=current_date)
        
    if Solidjobs_category is not None:
        process.crawl(SolidjobsSpider, universal_category=universal, preset=preset_choice,
                      experience_level=experience_level,
                      secondary_category=Solidjobs_category, date=current_date)

    process.start()


if __name__ == '__main__':
    main()
