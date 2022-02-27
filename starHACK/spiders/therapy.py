import scrapy


class TherapySpider(scrapy.Spider):
    name = 'therapy'

    # allowed_domains = ['psychologytoday.com/us/therapists/ny/new-york']
    
    def get_start_urls(self, url_prefix):
        start_urls = []
        count = 1
        url = url_prefix

        while(count <= 9081):
            new_url = url + str(count)
            start_urls.append(new_url)
            count += 20

        return start_urls

    def start_requests(self):
        headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}

        # start_urls = ['http://psychologytoday.com/us/therapists/ny/new-york/']

        url_prefix = 'https://www.psychologytoday.com/us/therapists/ny/new-york?sid=621a7e899a206&ref='
        start_urls = self.get_start_urls(url_prefix)

        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse, headers=headers)

    def parse(self, response):
        headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}

        for link in response.css('a.profile-title.verified::attr(href)'):
            yield scrapy.Request(url=link.get(), callback=self.parse_therapist, meta={'url': link.get()}, headers=headers)

    def parse_therapist(self, response):
        therapists = response.css('div.container.main-content.profile') # profile

        for therapist in therapists:

            # retrieve the name
            name = therapist.css("h1::text").get().strip()

            # retrieve the description
            description = '\n\n'.join(therapist.css("div.statementPara::text").getall())

            # retrieve the cost
            cost_label = therapists.css("div.finances-office").css("strong::text").get()
            cost = therapist.css("div.finances-office").css("li::text")[1].get().strip()

            if (cost_label != 'Cost per Session:'):
                cost = 'N/A'

            # retrieve the contact info
            phone_number = therapist.css("a.phone-number::text").get()

            # retrieve the insurance info
            insurance_label = therapist.css("div.spec-list.attributes-insurance").css("h5::text").get()

            if (insurance_label == 'Accepted Insurance Plans'):
                insurance = therapist.css("div.spec-list.attributes-insurance").css("div.col-split-xs-1.col-split-md-2").css("li::text").getall()
                insurance = ', '.join([x.strip() for x in insurance])  # strip the new line character + join elements as a string
            else:
                insurance = 'N/A'

            yield {
                'name': name,
                'description': description,
                'phone_number': phone_number,
                'insurance': insurance,
                'cost': cost,
                'url': response.meta.get('url')
            }