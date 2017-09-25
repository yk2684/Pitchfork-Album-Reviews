import scrapy


class AlbumSpider(scrapy.Spider):

    name = 'album_reviews'

    custom_settings = {
        "DOWNLOAD_DELAY": 3,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 3,
        "HTTPCACHE_ENABLED": True
    }

    start_urls = ['http://pitchfork.com/reviews/albums'] + ['http://pitchfork.com/reviews/albums/?page={}'.format(i) for i in range(1,1590)]

    def parse(self, response):

        for href in response.xpath(
            '//div[@class="review"]/a/@href'
        ).extract():

            yield scrapy.Request(
                url= 'http://pitchfork.com' + href,
                callback=self.parse_albums,
                meta={'url': href}
            )


    def parse_albums(self, response):

        album = response.xpath('//h1[@class="review-title"]/text()').extract()

        artist = response.xpath('//ul[@class="artist-links artist-list"]/li/a/text()').extract()

        pub_date = response.xpath('//time[@class="pub-date"]/text()').extract()

        release_date = response.xpath('//span[@class="year"]/text()').extract()

        label = response.xpath('//ul[@class="label-list"]/li/text()').extract()

        rating = response.xpath('//span[@class="score"]/text()').extract()

        reviewer = response.xpath('//a[@class="display-name"]/text()').extract_first()

        genre = response.xpath('//ul[@class="genre-list before"]/li/a/text()').extract()

        bnm = response.xpath('//p[@class="bnm-txt"]/text()').extract()

        yield {
            'album': album,
            'artist': artist,
            'pub_date': pub_date,
            'release_date': release_date,
            'label': label,
            'rating': rating,
            'reviewer': reviewer,
            'genre': genre,
            'bnm': bnm}