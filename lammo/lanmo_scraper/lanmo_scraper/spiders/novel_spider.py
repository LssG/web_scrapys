import scrapy

class NovelSpider(scrapy.Spider):
    name = "novel_spider"
    allowed_domains = ["biquge365.net"]
    start_urls = ["https://m.biquge365.net/chapter/518381/26793529.html"]  # 设置第一章的URL

    def __init__(self, *args, **kwargs):
        super(NovelSpider, self).__init__(*args, **kwargs)
        self.file = open("网游之圣光降临（笔趣阁）.txt", "w", encoding='utf-8')  # 创建文本文件用于保存内容
        self.count = 0

    def closed(self, reason):
        self.file.close()  # 关闭文件

    def parse(self, response):
        # 获取章节标题
        title = response.css('h1::text').get()

        # 获取章节内容
        content = response.css('div#txt::text').getall()
        content = [x.strip() for x in content]
        content = "\n".join(content)

        # 写入标题和内容到文本文件
        self.file.write(f"{title}\n")
        self.file.write(f"{content}\n\n")
        print(self.count)
        # if self.count > 2:
        #     return
        self.count += 1

        # 查找“下一章”的链接
        next_page = response.css('div.fanye1 ul li:nth-child(4) a::attr(href)').re_first(r'/chapter/\d+/[\d]+\.html')
        response
        if next_page:
            # 如果发现下一章的链接不是目录链接，继续请求下一章
            next_page_url = response.urljoin(next_page)
            yield scrapy.Request(next_page_url, callback=self.parse)
        else:
            self.log("已经到达最后一章，爬取结束。")
