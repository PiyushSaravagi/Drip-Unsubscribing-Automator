# url = "https://pr.vipkid.com.cn/login"
from selenium import webdriver
from time import sleep
import pandas as pd
import requests

driver = webdriver.Chrome('chromedriver.exe')

user = ""	# Your VIPKID username here
password = "" # Your password here

# ======================================================================
#   LOGGING IN TO VIPKID
# ======================================================================
driver.get("https://pr.vipkid.com.cn/login")
driver.find_element_by_class_name("username").send_keys(user)
driver.find_element_by_class_name("password").send_keys(password)
driver.find_element_by_class_name("login-btn").click()
sleep(10)
driver.get("https://pr.vipkid.com.cn/referral")
sleep(5)

# ======================================================================
#   FILTERING TO SELECT RANGE FROOM YESTERDAY TO TODAY
# ======================================================================
import datetime

now = datetime.datetime.now()
today = now.strftime("%Y-%m-%d")
yesterday = (now - datetime.timedelta(days=1)).strftime("%Y-%m-%d")

driver.find_elements_by_class_name("el-input__inner")[0].click()
sleep(2)
driver.find_elements_by_class_name("el-select-dropdown__item")[3].click()
driver.find_elements_by_class_name("el-input__inner")[1].send_keys(yesterday)
driver.find_elements_by_class_name("el-input__inner")[2].send_keys(today)
driver.find_element_by_class_name("search-btn").click()
sleep(5)

# ======================================================================
#   GETTING ALL NAMES, EMAIL AND PHONE PRESENT ON THE FIRST PAGE
# ======================================================================
name = driver.find_elements_by_class_name("el-table_1_column_1")
email = driver.find_elements_by_class_name("el-table_1_column_2")
phone = driver.find_elements_by_class_name("el-table_1_column_3")

original_data_frame = pd.read_csv("data.csv")
new_data_frame = pd.DataFrame(columns=["name", "email", "phone"])

k = 1
for i in range(1, len(email)):
    new_data_frame.loc[k] = [name[i].text, email[i].text, phone[i].text]
    k = k + 1

# Only one page of data - we are done
if len(driver.find_elements_by_class_name("number")) == 0: exit(0)

total_pages = int(driver.find_elements_by_class_name("number")[-1].text)  # Getting the total number of pages

# ======================================================================
#   MOVING TO NEXT PAGES AND GETTING NAMES, EMAIL AND PHONE PRESENT ON THOSE PAGE
# ======================================================================
for x in range(1, total_pages):
    next_button = driver.find_element_by_class_name("btn-next")
    next_button.click()
    sleep(2)
    name = driver.find_elements_by_class_name("el-table_1_column_1")
    email = driver.find_elements_by_class_name("el-table_1_column_2")
    phone = driver.find_elements_by_class_name("el-table_1_column_3")
    for i in range(1, len(email)):
        new_data_frame.loc[k] = [name[i].text, email[i].text, phone[i].text]
        k = k + 1

print(new_data_frame)

# concated_data_frame = pd.concat([original_data_frame, new_data_frame]).drop_duplicates().reset_index(drop=True)
# print(concated_data_frame)

original_data_frame = original_data_frame.append(new_data_frame)
original_data_frame = original_data_frame.drop_duplicates(subset=['email'], keep='first')
original_data_frame.to_csv("data.csv", index=False)
# print(driver.page_source)
driver.close()

# ======================================================================
#   UNSUBSCRIBING FROM ALL CAMPAIGNS ON DRIP
# ======================================================================
for i in range(0, len(new_data_frame)):
    email = new_data_frame.iloc[i]['email']
    response = requests.post('https://api.getdrip.com/v2/6820235/subscribers/' + email + '/remove',
                             auth=('d1c30dc3e2bbdd9d049a122e1f5220b8', ''))
    if response.status_code == 200:
        print("SUCCESSFULLY REMOVED " + email)






# ========================== PLAYGROUND STARTS HERE ================================#

"""
subscribers_list = dict()
subscribers_list['subscribers'] = [{'email', 'saravagipiyush@gmail.com'}]
import requests

# WORKS
response = requests.get('https://api.getdrip.com/v2/6820235/campaigns/140128164/subscribers?' + str(subscribers_list),
                        auth=('d1c30dc3e2bbdd9d049a122e1f5220b8', ''))


def pretty_print_POST(req):
    print('{}\n{}\n{}\n\n{}'.format(
        '-----------START-----------',
        req.method + ' ' + req.url,
        '\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
        req.body,
    ))

"""
# response = requests.Request('POST', 'https://api.getdrip.com/v2/6820235/campaigns/140128164/subscribers',
#                             headers={'auth': 'd1c30dc3e2bbdd9d049a122e1f5220b8'},
#                             data={'batches': str(subscribers_list)})
# prepared = response.prepare()
# pretty_print_POST(prepared)
# response = requests.Session().send(prepared)
#
# response = requests.get(
#     'https://api.getdrip.com/v2/6820235/campaigns/140128164/unsubscribes?batches=' + str(subscribers_list),
#     auth=('d1c30dc3e2bbdd9d049a122e1f5220b8', ''))
#
# subscribers = [
#     {"email": "saravagipiyush@gmail.com"}
# ]
#
# import requests
# data = [
#   ('subscribers', subscribers),
# ]
#
# response = requests.post('https://api.getdrip.com/v2/6820235/unsubscribes/batches', data=data, auth=('d1c30dc3e2bbdd9d049a122e1f5220b8', ''))
