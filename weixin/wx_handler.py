from flask import request
from loguru import logger

from weixin.verification import signature as f_signature	# 签名算法
import weixin.receive as receive	# 接收微信消息的地形
import weixin.reply as reply		# 将要答复的信息包装成微信需要的xml格式
from  chatgpt.chatgpt_ import chatgpt_

class WxHandle:
    @staticmethod
    def post():
        """
        响应微信的post请求，微信用户发送的信息会使用Post请求
        :return:
        """
        try:
            logger.info("接收微信消息->\n"+str(request.data))
            # 对微信传来的xml信息进行解析，解析成我们自定义的对象信息
            receive_msg = receive.parse_xml(request.data)
            # 如果解析成功
            if isinstance(receive_msg, receive.Msg):
                # 该微信信息为文本信息
                if receive_msg.type == "text":
                    # 创建一条文本信息准备返回给微信，文本内容为“测试”
                    oo=chatgpt_()
                    isok,replaycontent=oo.chat(receive_msg.content)                    
             
                    print(f"isok:{isok},replaycontent:{replaycontent}")
                    msg = reply.TextMsg(receive_msg,replaycontent)

                    # 发送我创建的文本信息
                    return msg.send()
                else:
                    # 该信息不为文本信息时，发送我定义好的一条文本信息给他
                    return reply.Msg(receive_msg).send()
        except Exception:
            logger.error("解析微信XML数据失败！")
        return "xml解析出错"

    @staticmethod
    def get():
        """
        响应微信的get请求，微信的验证信息会使用get请求      
        :return: 
        """
        # 微信传来的签名，需要和我生成的签名进行比对
        signature = request.args.get('signature')   # 微信已经加密好的签名，供我比对用
        timestamp = request.args.get('timestamp')   # 这是我需要的加密信息
        nonce = request.args.get('nonce')           # 也是需要的加密信息
        # 判断该请求是否正常，签名是否匹配
        try:
            # 微信传来的签名与我加密的签名进行比对，成功则返回指定数据给微信
            if signature == f_signature(timestamp, nonce):
                # 微信要求比对成功后返回他传来的echost数据给他
                return request.args.get('echostr')
            else:
                return ""
        except Exception:
            logger.error("签名失败！")
        return "签名失败！"
