import time
import weixin.receive as receive


class Msg:
    def __init__(self, receive_msg: receive.Msg):
        """
        将回复用户的信息按照微信的xml格式进行包装
        :param receive_msg: 
        """
        self.dict = dict()
        # 这里是我发送信息，所以发送给我们收到的微信消息的发送者
        self.dict['ToUserName'] = receive_msg.fromUser
        # 而是谁发送的呢？自然是我们收到的微信消息的接收者，也就是我的公众号
        self.dict['FromUserName'] = receive_msg.toUser
        # 发送时间
        self.dict['CreateTime'] = int(time.time())
        # 发送的信息文本，这里是默认的文本
        self.dict['Content'] = "对不起，我没有看懂你的信息~"
        pass

    def send(self):
        # 发送的xml格式
        xml = """
                    <xml>
                        <ToUserName><![CDATA[{ToUserName}]]></ToUserName>
                        <FromUserName><![CDATA[{FromUserName}]]></FromUserName>
                        <CreateTime>{CreateTime}</CreateTime>
                        <MsgType><![CDATA[text]]></MsgType>
                        <Content><![CDATA[{Content}]]></Content>
                    </xml>
              """
        # 将当前对象的dict属性填入到xml文本中，对应的{ToUserName}、{FromUserName}等
        return xml.format(**self.dict)


class TextMsg(Msg):
    def __init__(self, receive_msg: receive.Msg, content):
        super().__init__(receive_msg)
        self.dict['Content'] = content

    def send(self):
        xml = """
            <xml>
                <ToUserName><![CDATA[{ToUserName}]]></ToUserName>
                <FromUserName><![CDATA[{FromUserName}]]></FromUserName>
                <CreateTime>{CreateTime}</CreateTime>
                <MsgType><![CDATA[text]]></MsgType>
                <Content><![CDATA[{Content}]]></Content>
            </xml>
            """
        return xml.format(**self.dict)


class ImageMsg(Msg):
    def __init__(self, receive_msg: receive.Msg, media_id):
        super().__init__(receive_msg)
        self.dict['MediaId'] = media_id

    def send(self):
        xml = """
            <xml>
                <ToUserName><![CDATA[{ToUserName}]]></ToUserName>
                <FromUserName><![CDATA[{FromUserName}]]></FromUserName>
                <CreateTime>{CreateTime}</CreateTime>
                <MsgType><![CDATA[image]]></MsgType>
                <Image>
                <MediaId><![CDATA[{MediaId}]]></MediaId>
                </Image>
            </xml>
            """
        return xml.format(**self.dict)