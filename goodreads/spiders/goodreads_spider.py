from scrapy import Spider, Request
from goodreads.items import GoodreadsItem


class GoodreadsSpider(Spider):
	name='goodreads_spider'
	allowed_urls = ['https://www.goodreads.com']
	start_urls = ['https://www.goodreads.com']

	def parse(self, response):

		genre_names = response.xpath('//*[@id="browseBox"]/div[2]/div/a/text()').extract()[:29]

		genre_hrefs = response.xpath('//*[@id="browseBox"]/div[2]/div/a/@href').extract()[:29]
		genre_href_names = [g.split('/genres/')[1] for g in genre_hrefs]

		genre_urls = [f'https://www.goodreads.com/genres/most_read/{genre}' for genre in genre_href_names]

	
		for i, url in enumerate(genre_urls): #for url in genre_urls:
			yield Request(url=url, callback=self.parse_books, priority=i, meta={'priority': i}) #assign to callback the method it should pass what it receives from the GET request (Request object)

	def parse_books(self, response): # calling this 29 times
		book_hrefs = response.xpath('//div/*[@class="coverWrapper"]/a/@href').extract()

		book_urls = ['https://www.goodreads.com' + book for book in book_hrefs]

		priority_i = response.meta['priority']
		#print("="*55)
		#print(len(book_urls))
		#print("="*55)

		genre_url = response.request.url

		for url in book_urls:
			yield Request(url=url, callback=self.parse_book_details, priority=priority_i, dont_filter=True, meta= {'genre_url': genre_url})

	def parse_book_details(self, response): # calling this 29*100 times
	
		
		book_title = response.xpath('//h1[@id="bookTitle"]/text()').extract()[0].strip()
		author = response.xpath('//a[@class="authorName"]/span/text()').extract()

		rating_avg = response.xpath('//div[@id="bookMeta"]/span[@itemprop="ratingValue"]/text()').extract()[0].strip() 
		ratings_amt = response.xpath('//div[@id="bookMeta"]//meta[@itemprop="ratingCount"]/@content').extract()   
		reviews_amt = response.xpath('//div[@id="bookMeta"]//meta[@itemprop="reviewCount"]/@content').extract() 

		price = response.xpath('//ul[@class="buyButtonBar left"]/li/a/text()').extract_first()
		
		try:
			pages_amt = response.xpath('//div[@id="details"]//div[@class="row"]/span[@itemprop="numberOfPages"]/text()').extract()
		except:
			pages_amt = ""

		try:
			publish_date = response.xpath('//div[@id="details"]//div[@class="row"][2]/text()').extract()[0].strip().split("\n")[1].strip()
		except IndexError:
			publish_date = ""

		genre = response.meta['genre_url'].split('most_read/')[1]

		item = GoodreadsItem()
		item['genre'] = genre
		item['book_title'] = book_title
		item['author'] = author
		item['rating_avg'] = rating_avg
		item['ratings_amt'] = ratings_amt
		item['reviews_amt'] = reviews_amt
		item['price'] = price
		item['pages_amt'] = pages_amt
		item['publish_date'] = publish_date

		yield item


	



		














