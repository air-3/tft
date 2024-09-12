import scrapy
import json
import os

IdSeason = "s12"

CHESS_JS_URL_KEY = "urlChessData"   # 棋子js文件url key
RACE_JS_URL_KEY = "urlRaceData"    # 种族js文件url key
JOB_JS_URL_KEY = "urlJobData"     # 职业js文件url key
EQUIP_JS_URL_KEY = "urlEquipData"   # 装备js文件url key
BUFF_JS_URL_KEY = "urlBuffData"    # 海克斯js文件url key
ADVENTURE_JS_URL_KEY = "urlAdventureData"    # 奇遇js文件url key

class TftspiderSpider(scrapy.Spider):
    name = "tftspider"
    allowed_domains = ["lol.qq.com","game.gtimg.cn"]
    start_urls = ["https://lol.qq.com/zmtftzone/public-lib/versionconfig.json"]

    def parse(self, response):
        # 解析JSON数据
        data = json.loads(response.text)

        chessJsUrl = ""
        raceJsUrl = ""
        jobJsUrl = ""
        equipJsUrl = ""
        buffJsUrl = ""
        adventureJsUrl = ""
        for i in data:
            if (i["idSeason"] == IdSeason):
                chessJsUrl = i[CHESS_JS_URL_KEY]
                raceJsUrl = i[RACE_JS_URL_KEY]
                jobJsUrl = i[JOB_JS_URL_KEY]
                equipJsUrl = i[EQUIP_JS_URL_KEY]
                buffJsUrl = i[BUFF_JS_URL_KEY]
                adventureJsUrl = i[ADVENTURE_JS_URL_KEY]
                break


        print(chessJsUrl + "开始！！！")
        yield scrapy.Request(url=chessJsUrl, callback=self.parse_chess_js)
        print(chessJsUrl + "结束！！！")

        print(raceJsUrl + "开始！！！")
        yield scrapy.Request(url=raceJsUrl, callback=self.parse_race_js)
        print(raceJsUrl + "结束！！！")

        print(jobJsUrl + "开始！！！")
        yield scrapy.Request(url=jobJsUrl, callback=self.parse_job_js)
        print(jobJsUrl + "结束！！！")

        print(equipJsUrl + "开始！！！")
        yield scrapy.Request(url=equipJsUrl, callback=self.parse_equip_js)
        print(equipJsUrl + "结束！！！")

        print(buffJsUrl + "开始！！！")
        yield scrapy.Request(url=buffJsUrl, callback=self.parse_hex_js)
        print(buffJsUrl + "结束！！！")

        print(adventureJsUrl + "开始！！！")
        yield scrapy.Request(url=adventureJsUrl, callback=self.parse_adventure_js)
        print(adventureJsUrl + "结束！！！")


    # 解析棋子文件
    def parse_chess_js(self, response):
        data = json.loads(response.text)

        # 保存文件本身
        file_name = response.url.split('/')[-1].replace("js","json")
        file_path = os.path.join("./tft_data/", file_name.replace(".json",""), file_name)
        yield self.save_json(file_path, data)

        # 解析文件，保存图片
        for item in data["data"]:

            # 下载大图
            image_url = "https://game.gtimg.cn/images/lol/tftstore/s12/624x318/" + item["chessId"] + ".jpg"
            file_name = item["displayName"] + ".jpg"
            file_path = os.path.join("./tft_data/chess/img/", file_name)
            meta = {"file_path": file_path}
            yield scrapy.Request(image_url, callback=self.download_img,  meta = meta)

            # 下载头像
            head_image_url = "https://game.gtimg.cn/images/lol/act/img/tft/champions/" + item["chessId"] + ".png"
            file_name = item["displayName"] + ".png"
            file_path = os.path.join("./tft_data/chess/img_head/", file_name)
            meta = {"file_path": file_path}
            yield scrapy.Request(head_image_url, callback=self.download_img, meta=meta)

    # 解析种族js
    def parse_race_js(self, response):
        data = json.loads(response.text)

        # 保存文件本身
        file_name = response.url.split('/')[-1].replace("js", "json")
        file_path = os.path.join("./tft_data/", file_name.replace(".json", ""), file_name)
        yield self.save_json(file_path, data)

        # 解析文件，保存图片
        for item in data["data"]:
            image_url = item["imagePath"]

            file_name = item["name"] + ".png"
            file_path = os.path.join("./tft_data/race/img/", file_name)

            meta = {"file_path": file_path}
            yield scrapy.Request(image_url, callback=self.download_img, meta=meta)

    # 解析职业js
    def parse_job_js(self, response):
        data = json.loads(response.text)

        # 保存文件本身
        file_name = response.url.split('/')[-1].replace("js", "json")
        file_path = os.path.join("./tft_data/", file_name.replace(".json", ""), file_name)
        yield self.save_json(file_path, data)

        # 解析文件，保存图片
        for item in data["data"]:
            image_url = item["imagePath"]

            file_name = item["name"] + ".png"
            file_path = os.path.join("./tft_data/job/img/", file_name)

            meta = {"file_path": file_path}
            yield scrapy.Request(image_url, callback=self.download_img, meta=meta)

    # 解析装备js
    def parse_equip_js(self, response):
        data = json.loads(response.text)

        # 保存文件本身
        file_name = response.url.split('/')[-1].replace("js", "json")
        file_path = os.path.join("./tft_data/", file_name.replace(".json", ""), file_name)
        yield self.save_json(file_path, data)

        # 解析文件，保存图片
        for item in data["data"]:
            image_url = item["imagePath"]

            file_name = item["name"] + ".png"
            file_path = os.path.join("./tft_data/equip/img/", file_name)

            meta = {"file_path": file_path}
            yield scrapy.Request(image_url, callback=self.download_img, meta=meta)

    # 解析海克斯js
    def parse_hex_js(self, response):
        data = json.loads(response.text)

        # 保存文件本身
        file_name = response.url.split('/')[-1].replace("js", "json")
        file_path = os.path.join("./tft_data/", file_name.replace(".json", ""), file_name)
        yield self.save_json(file_path, data)

        # 解析文件，保存图片
        for item in data["data"].values():
            image_url = item["imgUrl"]

            file_name = item["name"] + ".png"
            file_path = os.path.join("./tft_data/hex/img/", file_name)

            meta = {"file_path": file_path}
            yield scrapy.Request(image_url, callback=self.download_img, meta=meta)

    # 解析奇遇js
    def parse_adventure_js(self, response):
        data = json.loads(response.text)

        # 保存文件本身
        file_name = response.url.split('/')[-1].replace("js", "json")
        file_path = os.path.join("./tft_data/", file_name.replace(".json", ""), file_name)
        yield self.save_json(file_path, data)

        # 解析文件，保存图片
        for item in data["data"].values():
            image_url = item["logoUrl"]

            file_name = item["title"] + ".png"
            file_path = os.path.join("./tft_data/adventure/img/", file_name)

            meta = {"file_path": file_path}
            yield scrapy.Request(image_url, callback=self.download_img, meta=meta)

    def download_img(self, response):

        file_path = response.meta['file_path']
        folder_path = os.path.dirname(file_path)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        with open(file_path, 'wb') as f:
            f.write(response.body)

    def save_json(self, file_path, data):
        folder_path = os.path.dirname(file_path)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        with open(file_path, 'w') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)







