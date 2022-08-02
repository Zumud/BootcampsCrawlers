import re
from scrapy.spiders import SitemapSpider, CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class LeWagonSpider(SitemapSpider):
    name = "LeWagon"
    # allowed_domains = ['lewagon.com']
    # start_urls = ['https://www.lewagon.com/campuses']
    sitemap_urls = ['https://www.lewagon.com/sitemap.xml.gz']
    sitemap_follow = [r'lewagon\.com\/[^\/]+\/[^\/]*course\/.+']

    # rules = (
    #     # Extract links matching 'category.php' (but not matching 'subsection.php')
    #     # and follow links from them (since no callback means follow=True by default).
    #     Rule(LinkExtractor(restrict_xpaths=('//a[@class="card-link"]',))),
    #
    #     # Extract links matching 'item.php' and parse them with the spider's method parse_item
    #     Rule(LinkExtractor(allow=('item\.php',)), callback='parse'),
    # )

    # def start_requests(self):
    #     urls = ['https://www.lewagon.com/campuses']
    #     for url in urls:
    #         yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        is_english_page = response.xpath("/html/@lang").get() == 'en'
        web_topics = 'HTML, CSS, JavaScript, Git, Terminal, Object-Oriented principles, Ruby, Relational Database, SQL, ORM'
        ds_topics = 'Python, matplotlib, seaborn, Relational Database, SQL, Statistics, Probability, Linear Algebra, Machine Learning, Scikit-learn, Deep Learning, Data Engineering, Jupyter, Google Cloud Platform, MLflow'
        next_batch_details = response.xpath("//div[@class='next-batches'][1]/div[@class='card-next-batch'][1]//span//text()").getall()
        title = response.xpath("//title/text()").get()[:-11]
        if ' course in ' in title:
            [course, location] = title.split(' course in ')
        elif ' Course ' in title:
            [course, location] = title.split(' Course ')
        else:
            course = location = None
        if is_english_page and next_batch_details and course and location:
            cost = re.findall(pattern=r"\(([^)]+)\)|$", string=next_batch_details[-1])[0]
            yield {
                'bootcamp_name': 'Le Wagon',
                'course': course,
                'location': location,
                'rating': 4.98,
                'financing_option': 'Yes' if response.xpath("//section[@id='financing']").get() is not None else 'No',
                'ISA': 'Yes' if response.xpath("//section[@id='financing']//span[contains(text(), 'ISA')]").get() is not None else 'No',
                'topics': web_topics if course is 'Web Development' else ds_topics,
                'next_batch': (' '.join(next_batch_details[0].split())).split(' - ')[0],
                'cost': cost,
                'website': response.url,
                'logo_url': 'https://coursereport-production.imgix.net/uploads/school/logo/153/original/Icon_Red.png?w=100&h=100&dpr=1&q=75'
                # 'email', 'language', 'format', 'duration', 'time zone', 'placement rate', 'average time to job'
                # 'job guaranty', 'ROI'
            }
