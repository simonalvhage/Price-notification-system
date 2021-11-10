from main import detectservice,checkifexists,updatedbwithnewperc,insertintodb,infoscraper

def scheduler(mail, link, change, password):
    service = detectservice(link)
    if checkifexists(mail, link):
        updatedbwithnewperc(mail,service,link,change,password)
    else:
        insertintodb(mail,service,link,change,password)
        infoscraper(mail,service,link,change)