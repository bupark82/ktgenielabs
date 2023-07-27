import os
import streamlit as st
from dotenv import load_dotenv
load_dotenv() # load environment variables from .env file

client_id = os.environ["CLIENT_ID"]
client_key = os.environ["CLIENT_KEY"]
client_secret = os.environ["CLIENT_SECRET"]

from datetime import datetime
import hmac, hashlib

# timestamp 생성
timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3] 

# HMAC 기반 signature 생성
signature = hmac.new(
      key=client_secret.encode("UTF-8"), msg= f"{client_id}:{timestamp}".encode("UTF-8"), digestmod=hashlib.sha256
  ).hexdigest()

import json
import requests
url = "https://aiapi.genielabs.ai/kt/nlp/sentiment-analysis"

headers = {
     "x-client-key":client_key,
     "x-client-signature":signature,
     "x-auth-timestamp": timestamp,
     "Content-Type": "application/json",
     "charset": "utf-8",
 }   
body = json.dumps({"text": "재미있게 잘봤습니다 후속편을 기다리게 만드네요", "top_n": 3}) 
response = requests.post(url, data=body, headers=headers, verify=False)
if response.status_code == 200:
    try:
        print(response.json())
    except json.decoder.JSONDecodeError:
        print(f'json.decoder.JSONDecodeError occured.\nresponse.text: "{response.text}"')
else:
    print(f"response.status_code: {response.status_code}\nresponse.text: {response.text}")

st.write("""
         # My first app
         Hello *world!* \n
         재미있게 잘  봤습니다 후속편을 기다리게 만드네요
         """)
st.write( 
    response.json()
    )
st.write( 
    response.json()['result']['emotion']
    )

st.write(
    response.json()['text']
)
