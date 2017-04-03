#This class contains main crawler defination
#Settings as start_urls, Name of crawler and
# parsing methods can be found here
#
#

#Imports related to scrapy + logging + Model
from scrapy import Spider
from scrapy import Request
import logging
from scrapy.utils.log import configure_logging
from ScrapeExpertisefinder.items import ExpertiseInfoItem



#Configuring logs for Main crawler Module.
#Log file name can be changed below
#Log Level can be modified to INFO , ERROR , WARNING , DEBUG etc
#Format specifies file format

configure_logging(install_root_handler=False)
logging.basicConfig(
    filename='log.txt',
    format='%(levelname)s: %(message)s',
    level=logging.ERROR
)



#Spider/crawler
#This class contains parse method and crawler rules
#Check out for start_urls
#

class ScrapeExpertisefinder(Spider):
    #Defining Name of Spider | It will be used for running spider
    #Use - scrapy crawl <spider-name>  [scrapeData in our case]
    name='ExpertiseCrawler'
    # Domains allowed during scrape session | Outer domains will be filtered
    # This section need not to be altered in our case
    # So it can be left unaltered
    allowed_domain=[ 'http://network.expertisefinder.com/' ]

    #Start URLS for scraping
    #Change here for different URL
    #We can add multiple url here, seaprated by a comma(,)
    # example ['url1' , 'url2' , 'url3' ]
    start_urls=[
                 "http://network.expertisefinder.com/searchexperts?query=adhd"
               ]




    #Default Parse Method will be used for fetching all Expertise section and loop over them to parse
    #Scrapy makes call to start_urls SET and then response is parsed
    #by this block in ASYNC manner
    def parse(self, response):


        #Fetching each info as a block and iterating over it -
        for expertiseBlock in response.xpath("//div[contains(@class,'grayBorderedBox sresult')]"):
            #Fetching 1st section details and passing it to next async call
            #Fetching Next URL for parse Async call
            url = expertiseBlock.xpath(".//a[2]/@href").extract_first()

            #Change relative URL to absolute for making call
            absolute_urls=response.urljoin(url)
            print(absolute_urls)
            #make a new Scrapy Request | handle it using different parser parse_college_data (below).

            yield Request(absolute_urls,callback=self.parse_expertise_data)



    #Parse method, will be used for parsing University data :
    def parse_expertise_data(self,response):

            #Cleaing Response body
            # response = response.replace(body=response.body.replace('<br/>','\n'))
            # response = response.replace(body=response.body.replace('<br>', '\n'))

            #Fetching Name and university
            expertiseInfoOne=response.xpath("//h1/text()").extract_first()
            if expertiseInfoOne and len(expertiseInfoOne)>1:
                expertiseInfoOne=expertiseInfoOne.split(',')
                name = expertiseInfoOne[0]
                university=expertiseInfoOne[1]
            else:
                name = "n/a"
                university='n/a'

            expertiseSubSection=response.xpath("//div[contains(@id,'nameSection')]/p")

            #Job info
            job_title = expertiseSubSection.xpath(".//span[1]/text()").extract_first()
            department = expertiseSubSection.xpath(".//span[2]/text()").extract_first()

            #Fetching contact section here
            contactSubSection=response.xpath("//span[contains(@id,'contactInfo')]")

            #Fetching City/State
            city_state = contactSubSection.xpath(".//span[1]/span[2]/text()").extract_first()
            if city_state:
                city_state = city_state.split(',')
                city=city_state[0]
                state=city_state[1]
            else:
                city='n/a'
                state='n/a'



            email = contactSubSection.xpath(".//span[2]/a/text()").extract_first()
            phone = contactSubSection.xpath(".//span[3]/span[3]/span/text()").extract_first()

            print(phone)

            url = response.xpath("//a[text()='Faculty Page']/@href").extract_first()
            if url =='':
                url = 'n/a'



            #Filling all information into items Object Here -
            item=ExpertiseInfoItem()
            item['University']=university
            item['Name'] = name
            item['Job_Title'] = job_title
            item['Department'] = department
            item['City'] = city
            item['Email'] = email
            item['State'] = state
            item['url'] = url
            item['Phone'] = phone


            #Saving data to CSV file
            yield item



    #Method to filter text data
    def filterString(stringHere):
       return  " ".join(stringHere.split()).replace(",", "")
