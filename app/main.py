from cgitb import reset
import string
from fastapi import FastAPI
import httpx
import boto3
from botocore.exceptions import NoCredentialsError
from dotenv import load_dotenv
import os
app = FastAPI()

# from .v1 import config

@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}

# 送信跟建立事件
@app.get('/api/v1/send_email')
async def send_email():
    # get in request
    rfid = 'DADAFACE'
    date = '2022-10-22T15:27:24.195Z'
    image = ''
    device_id = "pi"

    # uploaded = upload_to_aws('app/image/test.jpg', '2022tsmc-hackathon', 'output_test123.jpg')
    upload_to_aws(image, '2022tsmc-hackathon', '{}-{}.jpg'.format(date,device_id))
    image_url = 'https://2022tsmc-hackathon.s3-ap-northeast-1.amazonaws.com/{}-{}.jpg'.format(date,device_id)
    print(image_url)

    user_email : string

    load_dotenv()
    API_BASE_USER = os.getenv('API_BASE_USER')
    API_BASE_EVENT = os.getenv('API_BASE_EVENT')

    r = httpx.get(API_BASE_USER+'user/rfid/'+rfid)
    uid = (r.json()['detail']['uid'])
    user_email = (r.json()['detail']['email'])
    print(uid,user_email)

    data={
        "uid": uid,
        "result": "denied",
        "time": date,
        "url": image_url
    }
    
    r = httpx.post(API_BASE_EVENT+'event', json=data)

    print(r.text,r.status_code)
    print(r.json())
    return {"message": "ok"}




def upload_to_aws(local_file, bucket, s3_file):
    load_dotenv()
    ACCESS_KEY = os.getenv('ACCESS_KEY')
    SECRET_KEY = os.getenv('SECRET_KEY')

    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)

    try:
        s3.upload_file(local_file, bucket, s3_file, ExtraArgs={'ACL':'public-read'})
        print("Upload Successful")
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False
