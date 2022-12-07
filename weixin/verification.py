import hashlib
from config.config import TOKEN

def signature(timestamp, nonce):
    """
    根据微信公众号文档写的微信需要的签名算法
    :param timestamp:
    :param nonce:
    :return:
    """
    # 接收微信服务器传来的时间戳和随机值，与我们自己设定的Token值进行排序后组成一个字符串
    signature_list = [TOKEN, timestamp, nonce]
    # 对列表进行排序
    signature_list.sort()
    # 组成字符串
    ciphertext = "".join(signature_list)
    # 进行sha1算法加密
    sha1 = hashlib.sha1()
    # python3.x后的算法写法
    sha1.update(ciphertext.encode("utf-8"))
    # 返回加密后的签名
    return sha1.hexdigest()


