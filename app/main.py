from cgitb import reset
import string
from fastapi import FastAPI, File
import httpx
import boto3
from botocore.exceptions import NoCredentialsError
from dotenv import load_dotenv
from datetime import datetime
import os
app = FastAPI()

# from .v1 import config

@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}

# 送信跟建立事件
@app.post('/api/v1/alert')
async def send_email(rfid: str = '', file: bytes = File(...)):
    # get in request
    date = datetime.now()
    image = file
    device_id = "pi"

    with open('tmp.img', 'wb') as f:
        f.write(file)

    image = 'tmp.img'

    # uploaded = upload_to_aws('app/image/test.jpg', '2022tsmc-hackathon', 'output_test123.jpg')
    upload_to_aws(image, '2022tsmc-hackathon', '{}-{}.jpg'.format(date.isoformat(),device_id))
    image_url = 'https://2022tsmc-hackathon.s3-ap-northeast-1.amazonaws.com/{}-{}.jpg'.format(date.isoformat(),device_id)
    print(image_url)

    user_email : string

    load_dotenv()
    API_BASE_USER = os.getenv('API_BASE_USER')
    API_BASE_EVENT = os.getenv('API_BASE_EVENT')
    API_BASE_ROCKET = os.getenv('API_BASE_ROCKET')

    import random
    data={
        "uid": str(random.randint(-3, -1)),
        "result": "red",
        "time": date.isoformat(),
        "url": image_url
    }


    if not rfid == '':
        r = httpx.get(API_BASE_USER+'user/rfid/'+rfid)
        uid = (r.json()['detail']['uid'])
        user_email = (r.json()['detail']['email'])
        print(f"Finish getting user status with result {uid = }, {user_email = }")
        data['uid'] = uid
        data['result'] = "yellow"

    print(API_BASE_ROCKET + f'alert?time={str(datetime.now()).split(".")[0]}&image={image_url.replace(" ", "%20")}')
    r = httpx.get(API_BASE_ROCKET + f'alert?time={str(datetime.now()).split(".")[0]}&image={image_url.replace(" ", "%20")}')
    print(f"Alertbot finish sending with result {r.text = }, {r.status_code = }")
    
    r = httpx.post(API_BASE_EVENT+'event', json=data)

    print(f"Finish creating event with result {r.json() = }, {r.status_code = }")
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
