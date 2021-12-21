import boto3
import time
import smtplib
import os
from dotenv import load_dotenv

from email.mime.text import MIMEText

# 크롤링을 위한 selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# 환경 변수를 가져오기 위함.
load_dotenv()

CONTACT_FLOW_ID = os.getenv('CONTACT_FLOW_ID')
INSTANCE_ID = os.getenv('INSTANCE_ID')
SOURCE_PHONE_NUMBER = os.getenv('SOURCE_PHONE_NUMBER')
DESTINATION_PHONE_NUMBER = os.getenv('DESTINATION_PHONE_NUMBER')
SMTP_PW = os.getenv('SMTP_PW')
SMTP_EMAIL = os.getenv('SMTP_MAIL')


def isMorning():
    morning = time.strftime('%H:%M:%S', time.localtime(time.time()))
    if morning == '08:00:00' and True:
        callToNumber()


def callToNumber():
    # AWS를 이용한 전화 걸기
    client = boto3.client('connect')
    client.start_outbound_voice_contact(
        DestinationPhoneNumber=DESTINATION_PHONE_NUMBER,
        ContactFlowId=CONTACT_FLOW_ID,
        InstanceId=INSTANCE_ID,
        SourcePhoneNumber=SOURCE_PHONE_NUMBER,
        AnswerMachineDetectionConfig={
            'EnableAnswerMachineDetection': False,
            'AwaitAnswerMachinePrompt': False
        },
    )


def runNewsCrawlingByNaver():
    # 네이버 IT 뉴스
    url = "https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=105"

    chromeOptions = webdriver.ChromeOptions()
    chromeOptions.add_argument('headless')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chromeOptions)
    driver.get(url)

    headTopics = driver.find_elements(By.CLASS_NAME, 'cluster_head_topic')

    # 뉴스 토픽 리스트
    print("[1] 뉴스 토픽 추출 완료")
    topicList = []
    for topic in headTopics:
        if topic.text != '':
            topicList.append(" - " + topic.text)

    runEmailSend("\n".join(topicList))


def runEmailSend(msg):
    smtp = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    smtp.login(SMTP_EMAIL, SMTP_PW)
    msg = MIMEText(msg)

    msg['Subject'] = 'Good Morning News'
    smtp.sendmail(SMTP_EMAIL, SMTP_EMAIL, msg.as_string())
    smtp.quit()
    print("[2] 이메일 발송 완료")


runNewsCrawlingByNaver()
