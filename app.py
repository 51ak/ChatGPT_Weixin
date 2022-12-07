from flask import Flask, request
from loguru import logger
from weixin.wx_handler import WxHandle

# 配置web框架
app = Flask(__name__)
# 日志文件保存10天日志，最大存储500M
logger.add("./log/runtime_{time}.log", retention="10 days", rotation="500 MB")



# 暴露路由，接收get和post请求
@app.route('/', methods=["GET", "POST"])
def default():
      return "hello ,51ak"

# 暴露路由，接收get和post请求
@app.route('/weixin/sms.ashx', methods=["GET", "POST"])
def wx_listener():
    # 通过getattr获取到WxHandle的静态get或post方法，lower是为了将大写method值转为小写，与WxHandle中的方法名对应
    fun = getattr(WxHandle, request.method.lower())
    # 调用得到的get或post方法
    return fun()


if __name__ == "__main__":
    # 监听8800端口
    app.run(host="0.0.0.0", port=80)
