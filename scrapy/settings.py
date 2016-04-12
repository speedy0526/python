#coding=utf-8
DOWNLOADER_MIDDLEWARES = {
        'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware' : None,
        'useragent.RotateUserAgentMiddleware' :400
}
