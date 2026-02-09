import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from pathlib import Path
import os

# ========= 配置 =========
SMTP_SERVER = "smtp.qq.com"
SMTP_PORT = 465

SENDER_EMAIL = os.environ["SENDER_EMAIL"]
SENDER_PASSWORD = os.environ["SENDER_PASSWORD"]
RECEIVER_EMAIL = os.environ["RECEIVER_EMAIL"]

PDF_PATH = Path("files/report.pdf")

# ========= 构造邮件 =========
msg = MIMEMultipart()
msg["From"] = SENDER_EMAIL
msg["To"] = RECEIVER_EMAIL
msg["Subject"] = "定时发送的打印文件"

msg.attach(MIMEText("附件为定时发送的 PDF 文件，请查收。", "plain", "utf-8"))

# 附件
with open(PDF_PATH, "rb") as f:
    pdf = MIMEApplication(f.read(), _subtype="pdf")
    pdf.add_header(
        "Content-Disposition",
        "attachment",
        filename=PDF_PATH.name
    )
    msg.attach(pdf)

# ========= 发送 =========
with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
    server.login(SENDER_EMAIL, SENDER_PASSWORD)
    server.send_message(msg)

print("邮件发送成功")
