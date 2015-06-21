tornado-web
===

[tornado-web](https://github.com/evolsnow/tornado-web)是在学习tornado时自己练手的简单(简陋)图片分享网站.

注意
---

* 项目由边学边写而成,对tornado的一些模块十分熟悉,所以代码仍有较大的优化空间;

* 前端引用了bootstrap, 未对网站进一步美化;

* jquery等脚本由需求驱动而学,而写,所以并不专业;

特点
---

* 支持网站的一些基本功能:注册,登录验证,图片上传,添加评论等;

* 后台数据库尝试使用了[mongodb](https://www.mongodb.org/), 通过[motor](https://motor.readthedocs.org/)操作发挥其异步特性;

* 支持新图片上传后其他用户浏览时的实时提醒,基于http的长连接,考虑兼容性暂采用ajax,后期会将websocket方式整合进去;

* 支持"获取最新"和"加载更多"功能,涉及数据库取出元素的排序问题, 详见代码;

用法
---

* Python2测试通过,Python3可能需要更改如下地方:
```python
import StringIO --> from io import StringIO
import Image    --> from PIL import Image
```
* 依赖均写在main.py的头部,暂未拆分模块;

* 请生成并修改cookie secrets字段:
```python
import base64
import uuid
print base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes)
```


License
---

This program is released under the [MIT License](http://www.opensource.org/licenses/MIT).
