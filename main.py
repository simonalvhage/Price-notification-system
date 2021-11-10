
import datetime
import secrets
import string
import re
import mysql.connector
global mydb, mycursor
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import websites

def checkifexists(mail, link):
    initdb()
    sql = "SELECT COUNT(mail)FROM customers WHERE (mail = %s AND link = %s)";
    val = (mail, link)
    k = mycursor.execute(sql, val)
    ifexists = mycursor.fetchone()[0]
    if ifexists == 0:
        return False
    else:
        return True

def initdb():
    global mydb
    mydb = mysql.connector.connect(
        host="192.168.1.23",
        user="root",
        password="9807097614!",
        database="pricenotifier"
    )
    global mycursor
    mycursor = mydb.cursor()


def insertintodb(mail, service, link,change, password):

    initdb()
    sql = "INSERT INTO customers (mail, service, link, pricepercentage, password) VALUES (%s, %s, %s, %s, %s)"
    val = (mail, service, link, change, password)
    mycursor.execute(sql, val)
    mydb.commit()

    print(mycursor.rowcount, "record inserted.")

def updatedbwithnewperc(mail, service, link,change, password):

    initdb()
    sql = "UPDATE customers SET pricepercentage = %s WHERE (mail = %s AND link = %s)";
    val = (change, mail, link)
    mycursor.execute(sql, val)
    mydb.commit()

    print(mycursor.rowcount, "record inserted.")


def createpassword(mail):
    initdb()
    sql = "SELECT COUNT(mail)FROM customers WHERE mail = %s";
    mail = (mail,)
    k = mycursor.execute(sql,mail)
    ifexists = mycursor.fetchone()[0]

    if ifexists == 0:
        alphabet = string.ascii_letters + string.digits
        password = ''.join(secrets.choice(alphabet) for i in range(6))  # for a 20-character password
        x = 1
    else:
        sql = "SELECT password FROM customers WHERE mail = %s";
        k = mycursor.execute(sql, mail)
        password = mycursor.fetchone()[0]
        x = 0

    print(password)
    return password,x

def detectservice(link):
    if 'amazon' in link:
        return 'amazon'
    if 'netonnet' in link:
        return 'netonnet'
    if 'elgiganten' in link:
        return 'elgiganten'

def is_time_between(begin_time, end_time, check_time=None):
    # If check time is not given, default to current UTC time
    check_time = check_time or datetime.utcnow().time()
    if begin_time < end_time:
        return check_time >= begin_time and check_time <= end_time
    else: # crosses midnight
        return check_time >= begin_time or check_time <= end_time

def check_if_new_urls():
    initdb()
    k = mycursor.execute("SELECT * FROM customers");
    ifexists = mycursor.fetchall()
    for row in ifexists:
        if row[5] == None:
            infoscraper(row[1], row[2], row[3], row[4])
        else:
            compare_price(row[1], row[2], row[3], row[4])


def infoscraper(mail, service, url, change):
    checkpricefunction = "websites.parsewebsite_" + service
    title, img,price = eval(checkpricefunction + '(url)')
    initdb()
    sql = "UPDATE customers SET product = %s, oldprice = %s, img = %s WHERE (mail = %s AND link = %s AND pricepercentage = %s)";
    val = (title, price, img, mail, url, change)
    mycursor.execute(sql, val)
    mydb.commit()
    print("new record added")


def compare_price(mail, service, url, change):
    checkpricefunction = "websites.parsewebsite_" + service
    title,img,price = eval(checkpricefunction + '(url)')
    if isinstance(img, str):
        print(img)
    else:
        long_img = img['data-a-dynamic-image']
        img = re.findall('"([^"]*)"', long_img)[0]
    price = price.replace(",",".")[:-3]
    initdb()
    sql = "SELECT oldprice FROM customers WHERE(mail = %s AND link = %s AND pricepercentage=%s)";
    val = (mail, url, change)
    k = mycursor.execute(sql, val)
    dbprice = mycursor.fetchone()[0].replace(",",".")
    maxprice = float(dbprice[:-3]) * (1 - (float(change) * 0.01))

    if price == dbprice:
        print("same price")
    elif float(price) < maxprice:
        price = str(price) + " kr"
        sql = "UPDATE customers SET oldprice = %s WHERE (mail = %s AND link = %s AND pricepercentage = %s)";
        val = (price, mail, url, change)
        mycursor.execute(sql, val)
        mydb.commit()

        print("updated price")
        sendemail(mail,service,title, url, price,img)


def sendemail(mail,service,title, url, price,imgurl):
    smtp_server = "smtp.gmail.com"
    port = 587  # For starttls
    message = MIMEMultipart("alternative")
    message["Subject"] = "We have found better prices!"
    message["From"]= "Simons Watchlist <simonswatchlist@gmail.com>"
    message["To"] = mail
    password = "Simonswatchlist98"
    sender_email = "simonswatchlist@gmail.com"
    receiver_email = mail
    print(imgurl)
    html = """\
    <html>
      <body>
        <p>Hi,<br>
           Congratulations, we have found better price on this product:<br><br>
           <center>""" + str(title) + """<br> <img src='""" + str(imgurl) + """' alt="Product" width="200" height="200"><br>
           it now cost only: """ + str(price) + """ <br> <a href='""" + str(url) + """'>Link to product</a>
           <br>
           <br>
           Thank you<br>
           //Simon

        </p>
      </body>
    </html>
    """

    text = MIMEText(html, "html")
    message.attach(text)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )
def deleterecords(mail, code):
    initdb()
    sql = "DELETE FROM customers WHERE mail = %s AND password = %s";
    val = (mail, code)
    mycursor.execute(sql, val)
    mydb.commit()
    return mycursor.rowcount

if __name__ == '__main__':
    check_if_new_urls()
