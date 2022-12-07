from lxml import etree	# 用来解析xml格式的数据的库


def parse_xml(web_data):
    """
    解析微信传递来的消息，根据消息类型转换为不同的对象
    :param web_data:
    :return:
    """
    # 解析xml数据
    xml = etree.XML(web_data)
    # 查看消息类型
    msg_type = xml.find('MsgType').text
    if msg_type == 'text':
        # 为文本时生成文本对象
        return TextMsg(xml)
    elif msg_type == 'image':
        # 为图像是生成图像对象
        return ImageMsg(xml)
    return None


class Msg:
    """
    定义消息的基本格式，是一些类型消息的父类，解析XML格式的微信信息
    """
    def __init__(self, xml):
        self.toUser = xml.find('ToUserName').text   # 公众号的微信号
        self.fromUser = xml.find('FromUserName').text   # 发送消息的用户的openid
        self.time = xml.find('CreateTime').text     # 创建时间
        self.type = xml.find('MsgType').text        # 消息类型
        self.id = xml.find('MsgId').text            # 该消息的id，每天消息都有独立的id


class TextMsg(Msg):
    """
    解析文字类信息
    """
    def __init__(self, xml):
        Msg.__init__(self, xml)     # 为父类的属性赋值
        self.content = xml.find('Content').text.encode("utf-8")     # 传递来的信息需要经过utf-8编码


class ImageMsg(Msg):
    """
    解析图片信息
    """
    def __init__(self, xml):
        Msg.__init__(self, xml)
        self.picUrl = xml.find('PicUrl').text
        self.mediaId = xml.find('MediaId').text