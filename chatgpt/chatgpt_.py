import openai
import sys
from  config.config import OPENAI_KEY

class chatgpt_():

    def __init__(self,apitype="",dict_args_input={}):
        
        self.dict_args={
        "model":"text-davinci-003",
        "temperature":0.9,
        "max_tokens":550,
        "top_p":1,
        "frequency_penalty":0.0,
        "presence_penalty":0.6,
        }
        # if apitype in (""):
        #     pass
        for k,v in dict_args_input:
            self.dict_args[k]=v

    def chat(self,mess):
        isok,response=self.openapi_(mess)
        
        if isok:
            sb_mess=[]
            for c in response.choices:
                sb_mess.append(c.text)
            return isok,sb_mess 
        else:
            return isok,"error:{response}"

    def openapi_(self,mess):
        openai.api_key = OPENAI_KEY
        try :
            response = openai.Completion.create(
            model=self.dict_args["model"],
            prompt=str(mess),
            temperature=self.dict_args["temperature"],
            max_tokens=self.dict_args["max_tokens"],
            top_p=self.dict_args["top_p"],
            frequency_penalty=self.dict_args["frequency_penalty"],
            presence_penalty=self.dict_args["presence_penalty"],
            #stop=[" Human:", " AI:"]
            )
            return True,response
        except Exception as ex:
            return False,str(ex)
        



if __name__ == '__main__':
    if(len(sys.argv)>1):
        isok,responsestr=chatgpt_().chat(sys.argv[1])
        print(responsestr)