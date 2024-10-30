from typing import Any
import scrapy
from urllib.parse import urlparse, parse_qs


from blocket.items import BlocketItem


class CategorySpider(scrapy.Spider):
    name = 'category'
    # start_urls = ["https://jobb.blocket.se/lediga-jobb?filters=juridik&sort=PUBLISHED"]
    #start_urls = ["https://jobb.blocket.se/lediga-jobb?filters=offentlig-foervaltning&sort=PUBLISHED"]
    start_urls = ["https://jobb.blocket.se/lediga-jobb?filters=bank-finans-och-foersaekring&sort=PUBLISHED"]
    #https://jobb.blocket.se/lediga-jobb?filters=bank-finans-och-foersaekring&sort=PUBLISHED&page=2


    def parse(self, response, **kwargs: Any) -> Any:
        # Current page number
        parsed_url = urlparse(response.url)
        query_params = parse_qs(parsed_url.query)
        current_page = query_params.get("page", ['1'])[0]

        print(f"Start parsing category page {current_page} ")
        print(f"Start parsing category page {response.url} ")

        if self.settings.get('VACANCY_PAGE_PARSING_ENABLED'):
            urls = response.css("div.sc-b071b343-0.eujsyo a")
            for idx, url in enumerate(urls):
                yield response.follow(
                    url,
                    callback=self.parse_vacancy_page,
                    meta={'category_page_num': current_page, 'link_number': idx+1}
                )
        else:
            # If no need parse vacancy page
            for vacancy_block in response.css("div.sc-b071b343-0.eujsyo"):
                item = BlocketItem()

                item['url'] = vacancy_block.css("a::attr(href)").get()
                item['title'] = vacancy_block.css("h2::text").get()
                item['company'] = vacancy_block.css("span.sc-f047e250-8.bimSjp::text").get()
                item['date_added'] = vacancy_block.css("p.sc-f047e250-1.gRACBc::text").get()
                item['location'] = vacancy_block.css("p.sc-f047e250-1.gRACBc span:nth-child(2)::text").get()
                item['category'] = vacancy_block.css("span.sc-f047e250-9.emzpag::text").getall()

                yield item

        # Find pages count:
        page_count = response.css('div.sc-9aebc51e-3.eMQydw a:last-of-type::text').get()
        page_count = int(page_count) if page_count else None

        next_page_url = response.css(
            "a.sc-c1be1115-0.heGCdS.sc-539f7386-0.gWJszl.sc-9aebc51e-2.jHuKGp:last-of-type::attr(href)").get()

        if next_page_url is not None:
            print(f"Found new category page {next_page_url}")
            yield response.follow(next_page_url, callback=self.parse)
        else:
            print(f"New category page not found")

        print(f"Finish parsing category page {current_page} / {page_count} ")


    def parse_vacancy_page(self, response) -> Any:
        meta = response.meta
        print(f"Parsing vacancy {meta.get('link_number')} from page {meta.get('category_page_num')} {response.url}")

        item = BlocketItem()

        item['url'] = response.url
        item['title'] = response.css("h1::text").get()
        item['company'] = response.css("a.sc-5fe98a8b-2.iapiPt::text").get()
        item['date_added'] = response.css("div.sc-dd9f06d6-2.dVNNPW:nth-of-type(4) span::text").get()
        item['date_expires'] = response.css("div.sc-dd9f06d6-2.dVNNPW:nth-of-type(2) span::text").get()
        item['location'] = response.css("div.sc-dd9f06d6-2.dVNNPW:nth-of-type(6) a::text").get()
        item['category'] = response.css("div.sc-dd9f06d6-2.dVNNPW:nth-of-type(8) a::text").getall()
        item['type'] = response.css("div.sc-dd9f06d6-2.dVNNPW:nth-of-type(10) a::text").getall()
        item['description'] = response.css("div.sc-d56e3ac2-5.sc-5fe98a8b-10.brdyEP.flrgoh *::text").getall()

        yield item
