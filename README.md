This web scraper is a handy tool I built using Scrapy and Scrapy-Playwright. It's all about making job hunting easier by pulling in listings from some of the top job boards in Poland like JustjoinIt, NofluffJobs, and Theprotocol. It's pretty neat because it saves a bunch of time that you'd otherwise spend hopping between different sites to check out job offers.

Right now, it's pretty simple to use. You've got two main choices when you start:

Department-Wise Search: If you pick preset '1', you can look for jobs in specific areas, like backend or frontend roles. This is super useful if you're looking for something specific in the tech field.

Language-Focused Search: With preset '2', you can filter jobs based on the programming languages they need. It's great for coders who have specialized in one or two languages and want to find jobs that match their skill set.

I'm thinking of adding some more features down the line, like letting you search by location or adding more job sites to the mix.


To use it you need:
mongodb configured on a specific port, you may also change it in the 'settings.py'
python venv requirements - !pip install -r 'requirements.txt'


