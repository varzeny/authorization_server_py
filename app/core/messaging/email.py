# email.py

# lib
from aiosmtplib import send
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# module
from app.core.config import SETTING

# define
class Smtp:
    isinstance:dict = {}

    @classmethod
    def __getitem__(cls, name:str):
        """클래스 인덱싱"""
        return cls.isinstance.get(name)
    
    
    def __init__(self, name:str, smtp_host:str, smtp_port:int, sender_id:str, sender_pw:str):
        self.name = name
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.sender_id = sender_id
        self.sender_pw = sender_pw
        Smtp.isinstance[self.name] = self

    async def send_email(self, receiver_addr, subject:str, data:str)->bool:
        try:
            mail = MIMEMultipart()
            mail["From"] = self.sender_id
            mail["To"] = receiver_addr
            mail["Subject"] = subject

            body = data
            mail.attach( MIMEText(body, "plain") )

            await send(
                mail,
                hostname= self.smtp_host,
                port= self.smtp_port,
                username= self.sender_id,
                password= self.sender_pw,
                start_tls=True
            )
            return True
        
        except Exception as e:
            print("ERROR from send_email : ", e)
            return False


# script
ENV = SETTING["app"]["core"]["messaging"]["email"]
EMAIL = Smtp(
    name=ENV.get("name"),
    smtp_host=ENV.get("smtphost"),
    smtp_port=ENV.get("smtpport"),
    sender_id=ENV.get("senderid"),
    sender_pw=ENV.get("senderpw")
)











# async def send_email(smtp_host:str, smtp_port:int, sender_addr:str, sender_pw:str, receiver_addr:str, subject:str, bodyData:str)->bool:

#     # print(smtp_host, smtp_port, sender_addr, sender_pw, receiver_addr, subject, bodyData)

#     result = None

#     msg = MIMEMultipart()
#     msg["From"] = sender_addr
#     msg["To"] = receiver_addr
#     msg["Subject"] = subject

#     body = bodyData    # 뭔가 가공할거면 여기서
#     msg.attach(MIMEText(body, "plain"))
#     try:
#         await send(
#             msg,
#             hostname=smtp_host,
#             port=smtp_port,
#             username=sender_addr,
#             password=sender_pw,
#             start_tls=True
#         )
#         result = True
#     except Exception as e:
#         print("ERROR from send_email : ", e)
#         result = False
#     finally:
#         # await smtp_client.quit()
#         return result



# # "Your verify code has arrived."