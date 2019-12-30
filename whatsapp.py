import autobrowse
import threading
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import configparser

driver = autobrowse.create_driver()

config = configparser.ConfigParser()
config.read('config.ini')
sheet_name = str(config['Sheet']['gsheet'])
numcol = int(config['Sheet']['mobile_number'])
mcol = int(config['Sheet']['msg'])
tcol = int(config['Sheet']['times'])

# Accessing google spreadsheet
scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scope)
client = gspread.authorize(creds)

rep = True
skip = False

def send_msg_direct(driver, msg):
    if(autobrowse.wait_for_element_x(driver, "//div[@class=\"_3u328 copyable-text selectable-text\"]", 1)):
        print("site is not loading properly, skipping current msg")
        return True
    text_box = driver.find_element_by_xpath("//div[@class=\"_3u328 copyable-text selectable-text\"]")
    text_box.send_keys(msg+autobrowse.Keys.ENTER)
    autobrowse.time.sleep(.5)
    return False

def send_msg(num, driver, msg, time):
    print("Sending message to",num)
    autobrowse.wait_time = 50
    searchbar = driver.find_element_by_css_selector("input[data-tab=\"2\"]")
    searchbar.send_keys(autobrowse.Keys.CONTROL, "a")
    searchbar.send_keys(num)
    autobrowse.time.sleep(.5)
    if(autobrowse.wait_for_element_x(driver, "//div[contains(@style,\"translateY(72px)\")]", 1)):
        print("Unable to find",num,"in contact")
        searchbar.send_keys(autobrowse.Keys.CONTROL, "a")
        searchbar.send_keys(autobrowse.Keys.BACKSPACE)
        return True
    for _ in range(time):
        x = send_msg_direct(driver, msg)
    searchbar.send_keys(autobrowse.Keys.CONTROL, "a")
    searchbar.send_keys(autobrowse.Keys.BACKSPACE)
    return x

def bulk_msg(driver, msgs, numbers, times):
    i = 0
    for num in numbers:
        try:
            time = int(times[i])
        except:
            time = 1
        send_msg(num, driver, msgs[i], time)
        i += 1

def replyer(driver):
    global rep
    while rep:
        latest_msgs = driver.find_elements_by_xpath("//span[contains(@class,\"_19RFN\")]")
        for m in latest_msgs:
            try:
                line = m.text
            except:
                continue
            if len(line) > 0:
                if(line[0]=="/"):
                    try:    
                        m.click()
                    except:
                        continue
                    intake = line[1:].split()
                    msg = " "
                    if(intake[0]=="echo"):
                        msg = msg.join(intake[1:])
                    elif(intake[0]=="help"):
                        msg = "This is Help Page: \n Write /echo means the reply will be echoed"
                    else:
                        msg = "Write /help to get help about commands"
                    send_msg_direct(driver, msg)

def final_run(skip, rep, driver, client):
    driver.get("https://web.whatsapp.com/")
    driver.save_screenshot("static/qr.png")
    j = 1
    while(autobrowse.wait_for_element_x(driver, "//input[@data-tab=\"2\"]", 1)):
        print(j)
        j += 1
        continue
    while (not skip):
        t = threading.Thread(target=replyer, args=(driver,), daemon=True)
        t.start()
        msg = "Enter 1 to send bulk msg / 2 to "
        if(rep):
            msg+="stop"
        else:
            msg+="start"
        msg+=" auto replying / 3 to exit: "
        code = input(msg)
        if(code=="1"):
            b = False
            if(rep):
                rep = False
                b = True
            sheet = client.open(sheet_name).sheet1
            numbers = sheet.col_values(numcol)[1:]
            msgs = sheet.col_values(mcol)[1:]
            times = sheet.col_values(tcol)[1:]
            bulk_msg(driver, msgs, numbers, times)
            rep = b
        elif(code=="2"):
            rep = not rep
        else:
            break