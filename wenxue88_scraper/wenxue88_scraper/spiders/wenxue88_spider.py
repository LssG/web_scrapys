import scrapy


class Wenxue88SpiderSpider(scrapy.Spider):
    name = "wenxue88_spider"
    allowed_domains = ["wenxue88.com"]
    start_urls = ["https://wenxue88.com/jingyingdeaoman/jydam1000.html"]

    def __init__(self, *args, **kwargs):
        super(Wenxue88SpiderSpider, self).__init__(*args, **kwargs)
        self.file = open("精英的傲慢.txt", "w", encoding='utf-8')  # 创建文本文件用于保存内容
        self.count = 0

    def closed(self, reason):
        self.file.close()  # 关闭文件

    def parse(self, response):
        # 提取章节标题
        title = response.css('h2::text').get()

        # 提取章节内容
        content = response.css('td.hycolor p::text').getall()
        content = "\n".join(content)  # 合并内容为单个字符串

        # 写入标题和内容到文本文件
        self.file.write(f"{title}\n")
        self.file.write(f"{content}\n\n")
        print(self.count)
        # if self.count > 2:
        #     return
        self.count += 1

        # 查找“下一章”的链接
        next_page = response.css('tr td.zw_txt:nth-child(2) a::attr(href)').get()
        if next_page:
            next_page_url = response.urljoin(next_page)  # 转换为绝对路径
            self.log(f"下一章链接: {next_page_url}")
            yield scrapy.Request(next_page_url, callback=self.parse)
        else:
            self.log("已经到达最后一章，爬取结束。")
            self.close()
