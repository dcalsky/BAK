BAK
-------
Push up-to-date announcements from multiple school websites to you.

## WEBSITE SUPPORT LIST
Send email or raise issue to tell me which TJ site's announcement is what you most wanna see... 
- [x] MATH(数学学院)
- [x] SSE(软件学院)
- [x] MECHANICAL(机械与能源学院)
- [x] CIVIL(土木学院)
- [x] OFFICIAL(同济大学官网)
- [ ] 4m3(本研一体化)
- [ ] xuanke(选课网)
- [ ] foreign(外国语学院)


## TECH STACK
- MongoDB (NoSQL database)
- RabbitMQ (message queue for http server and email server)
- Docker (deploying multiple containers)
- Scrapy (python network spider framework)
- Flask (lightweight python web framework)
- Miniprogram(Tencent)

## BUILD
*MAKE SURE THAT YOU HAVE ALREADY CONFIGURED REALISTIC SETTING VARIABLES AND DOCKER ENVIRONMENT*

### For server
Just run:
```
$ docker-compose up
```

### For client
Download [wx miniprogram tool](https://mp.weixin.qq.com/debug/wxadoc/dev/devtools/download.html) and open `98k` project. Subsequently, compile and preview it.
