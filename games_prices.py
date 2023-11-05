import scrapy
import pandas as pd
import os

class PlaystationSpider(scrapy.Spider):
    name = 'playstoregame'
    start_urls = ['https://store.playstation.com/en-id/category/05a2d027-cedc-4ac0-abeb-8fc26fec7180/']
    
    output_file = 'games_prices.csv'

    def parse(self, response):
        game_data = []

        for span in response.css('span'):
            css_classes = span.css('::attr(class)').extract_first()

            if "psw-t-body psw-c-t-1 psw-t-truncate-2 psw-m-b-2" in css_classes:
                game_data.append({
                    'title': span.css('::text').get()
                })
            elif "psw-m-r-3" in css_classes:
                game_data.append({
                    'price': span.css('::text').get()
                })

        df = pd.DataFrame(game_data)

        # Simpan DataFrame ke file CSV
        if not os.path.exists(self.output_file):
            # Jika file belum ada, simpan header juga
            df.to_csv(self.output_file, index=False)
        else:
            # Jika file sudah ada, tambahkan data tanpa header
            df.to_csv(self.output_file, mode='a', header=False, index=False)

        # Mencari tautan ke halaman berikutnya
        next_page_button = response.css('button[data-qa="ems-sdk-grid#ems-sdk-top-paginator-root#next"]')
        if next_page_button:
            next_page_url = next_page_button.css('button::attr(value)').extract_first()
            yield response.follow(next_page_url, callback=self.parse)
        else:
            self.log("Tidak ada halaman berikutnya. Spider selesai.")


    def closed(self, reason):
        self.log("Spider closed: %s" % reason)
        