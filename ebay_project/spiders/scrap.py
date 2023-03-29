import scrapy

from ..items import EbayProjectItem
class ScrapSpider(scrapy.Spider):
    name = 'scrap'
    # allowed_domains = ['x']
    # start_urls =['https://www.google.com']
    start_urls = ['https://www.ebay.com/b/Electronics/bn_7000259124/']

    def parse(self, response):
        
        links =response.css(".b-visualnav__tile::attr(href)").getall()
        
        
        for link in links:
            yield scrapy.Request(link, callback=self.parse_sub_cat)
    def parse_sub_cat(self,response):
        links =response.css(".b-visualnav__tile::attr(href)").getall()
        
        
        for link in links:
            yield scrapy.Request(link, callback=self.parse_p_links)
    def parse_p_links(self,response):
        links =response.css(".s-item__link::attr(href)").getall()
        
        for link in links:
            yield scrapy.Request(link, callback=self.parse_product)
            
        next_page =response.css(".pagination__next::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse_p_links)
    def parse_product(self,response):
        desc = response.css(".tab-content-m ::text").getall()
        desc = ''.join(desc).replace("\n",'').replace("\t",'')
        data_dict={}
        title =response.css(".x-item-title__mainTitle>span::text").get()
        price =response.css("span[itemprop=price]>span::text").get()
        image = response.css(".ux-image-filmstrip img::attr(src)").getall()
        seller =response.css(".ux-seller-section__item--seller>a>span::text").get()
        if not seller:
            seller =response.css(".no-wrap:nth-child(2)>a::attr(href)").get()
        if not title:
            title =response.css(".product-title::text").get()
        if not price:
            price =response.css(".display-price::text").get()
        if not desc:
            desc = response.css(".description dev.spec-row ::text").getall()
            desc= ''.join(desc)
        if not image:
            image =response.css(".app-filmstrip__image::attr(src)").getall()
            if len(image)==0:
                image =response.css("img[itemprop=image]::attr(src)").get()
        item = EbayProjectItem()
        data_dict['Title']=title
        data_dict['Price']=price
        data_dict['Description']= desc
        data_dict['Images']=image
        data_dict['Product Page URL']= response.url
        data_dict['Category']= response.css(".seo-breadcrumb-text>span::text").get()
        data_dict['SubCategory']=response.css("nav.breadcrumbs li:nth-child(2)>a>span::text").get()
        data_dict['Seller Name']= seller
        item['Title']=data_dict['Title']
        item['Price']= data_dict['Price']
        item['Description']= data_dict['Description']
        item['Product_Page_URL']= data_dict['Product Page URL']
        item['SellerName']= data_dict['Seller Name']
        item['Category']= data_dict['Category']
        item['SubCategory']= data_dict['SubCategory']
        item['Images']= data_dict['Images']
        yield item
