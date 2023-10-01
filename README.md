# Tools
Weird little tools

# Translate by baidu api
translate coursera's subtitle by using baidu's translate api

使用百度翻译 API 翻译 coursera 字幕, 暂时无法测试, 国外访问百度翻译太慢了
为了不片面的翻译句子内容,我把句子以逗号为单位重新再字幕中排列,因此翻译时也是以逗号为单位.
不知道是网络的原因还是代码问题,翻译出的文件会出现重复翻译的内容
假期会申请 bing 的 api 进行测试

使用方法:
`python translate_by_BaiduAPI.py original_subtitle.vtt new_subtitle.vtt`
