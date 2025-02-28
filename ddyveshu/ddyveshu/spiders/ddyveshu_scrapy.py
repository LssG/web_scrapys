import scrapy


class DdyveshuScrapySpider(scrapy.Spider):
    name = "ddyveshu_scrapy"
    allowed_domains = ["www.ddyveshu.cc"]
    # start_urls = ["https://www.ddyveshu.cc/"]
    start_urls = ["https://www.ddyveshu.cc/13707_13707327/770427587.html"]  # 起始章节的 URL

    def parse(self, response):
        # 提取章节标题
        title = response.css('div.bookname h1::text').get()

        # 提取章节内容
        content = response.css('div#content::text').getall()
        content = "\n".join(content).strip().replace('请记住本书首发域名：ddyveshu.cc。顶点小说手机版阅读网址：m.ddyveshu.cc','')  # 去掉多余的空白和换行

        # 打印提取内容（可选）
        # self.log(f"章节标题: {title}")
        # self.log(f"章节内容: {content[:100]}...")  # 打印部分内容以验证

        # 保存到文件
        with open("天才俱乐部.txt", "a", encoding="utf-8") as f:
            f.write(f"{title}\n\t{content}\n")

        # 查找下一章链接
        next_page = response.css('div.bottem1 a::attr(href)')[2].get()
        print(next_page)
        print(type(next_page))

        next_page_url = response.urljoin(next_page)
        if next_page_url != r'https://www.ddyveshu.cc/13707_13707327/815787420.html':
            self.log(f"下一章链接: {next_page_url}")
            yield scrapy.Request(next_page_url, callback=self.parse)
        else:
            self.log("爬取完成，没有更多章节。")
