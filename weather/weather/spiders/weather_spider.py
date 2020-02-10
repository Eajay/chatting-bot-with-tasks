import scrapy
import geocoder

class WeatherSpider(scrapy.Spider):
    name = "weather"

    def start_requests(self):
        g = geocoder.ip('me')
        zipcode = g.postal

        # urls = [
        #     'https://weather.com/weather/tenday/l/USVA0023:1:US',
        # ]
        urls = [
            'https://weather.com/weather/tenday/l/'+zipcode
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # location = response.url.split('/')[-1].split(':')[0]
        # filename = 'weather-%s.html' % location
        filename = 'weather.html'
        with open(filename, 'w') as f:
            f.write(response.body.decode('utf-8'))
        self.log('Saved file %s' % filename)

