# Tools
Weird little tools

# Translate by baidu api
translate coursera's subtitle by using baidu's translate api

使用百度翻译 API 翻译 coursera 字幕, 暂时无法测试, 国外访问百度翻译太慢了
为了不片面的翻译句子内容,我把句子以逗号为单位重新再字幕中排列,因此翻译时也是以逗号为单位.
不知道是网络的原因还是代码问题,翻译出的文件会出现重复翻译的内容
假期会申请 bing 的 api 进行测试

提示:
使用前需申请 baidu 翻译 api 的账号,并填充到`appid`和`appkey`中,如果翻译其他语种可以更改`from_lang`和`to_lang`

使用方法:
`python translate_by_BaiduAPI.py original_subtitle.vtt new_subtitle.vtt`

# Translate paddleOCR's content
## 文件夹属性图
- main 母文件夹
|--- output 输出文件夹
|--- work 代码文件夹
|--- data 原图片
## 快速使用
建立以上文件夹, 将原图放到 data 文件夹内, 将 go.py 放到 work 文件夹
在 main 文件夹内按照顺序执行以下命令
1. `cd work` 进入文件夹
2. `clear; python go.py` 执行代码
## 注意
文本翻译慢是因为翻译请求速度限制, 可以考虑修改第 92 行附近 `time.sleep(1)` , 尝试将 1 改小
## 百度翻译api的使用
将 13,14 行附近的 `appid, appkey` 改成自己的
应该有一个图片提示
