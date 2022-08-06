from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class Bloomtech(CrawlSpider):
    """This crawler extract all data related to all courses for bloomtech (Lambda school)"""
    name = 'Bloomtech'
    allowed_domains = ['bloomtech.com']
    start_urls = ['https://www.bloomtech.com/']

    rules = (
        Rule(
            # Extract links matching 'courses' in the restricted xpath and parse them with the spider's method parse
            LinkExtractor(allow=('courses',), restrict_xpaths=('//div[contains(@class, "courses")]',)),
            callback='parse'
        ),
    )

    def parse(self, response, **kwargs):
        course_name = response.xpath("//h1[contains(@class, 'first-title')]/text()").get()[:-7]
        yield {
            'bootcamp_name': 'Bloomtech',
            'course': course_name,
            'location': 'Online',
            'rating': 4.26,
            'financing_option': 'Yes' if 'Tuition Options' in response.xpath("//div[@id='tuition']//h2/text()").get() else 'No',
            'ISA': 'No',
            'topics': ', '.join(response.xpath("//div[@class='course-checks']//text()").getall()),
            'next_batch': 'Flexible Schedule',
            'cost': '$5,500' if 'Web3' in course_name else '$21,950',
            'website': response.url,
            'logo_url': 'https://coursereport-production.imgix.net/uploads/school/logo/408/original/Bloom_Institute_of_Technology_logo.png?w=200&h=200&dpr=1&q=75'
            # 'email', 'language', 'format', 'duration', 'time zone', 'placement rate', 'average time to job'
            # 'job guaranty', 'ROI'
        }
