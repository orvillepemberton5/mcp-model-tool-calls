import json,os,re
from urllib.request import Request,urlopen
def call(path,body=None):
 key=os.environ['MODEL_API_KEY'];h={'Authorization':'Bearer '+key,'User-Agent':'mcp-model-tool-calls/1.0'};data=json.dumps(body).encode() if body else None
 if body:h['Content-Type']='application/json'
 with urlopen(Request(os.getenv('MODEL_BASE_URL','https://argolink.io/v1')+path,data=data,headers=h),timeout=90) as r:return json.load(r)
def ask_model(prompt,model='gpt-5.4'): return call('/chat/completions',{'model':model,'messages':[{'role':'user','content':prompt}]})
def list_models(): return call('/models')
def generate_image(prompt,model='gpt-image-2',size='1024x1024'): return call('/images/generations',{'model':model,'prompt':prompt,'size':size})
if __name__=='__main__': print('Expose ask_model, generate_image, list_models through the official FastMCP host adapter.')
