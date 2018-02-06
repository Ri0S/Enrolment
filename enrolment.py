from selenium import webdriver
from bs4 import BeautifulSoup
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import requests


def login(snum, id, passwd):
    elem = driver.find_element_by_id("user.stu_nbr")
    elem.send_keys(snum)

    elem = driver.find_element_by_id("user.usr_id")
    elem.send_keys(id)

    elem = driver.find_element_by_id("user.passwd")
    elem.send_keys(passwd)

    elem = driver.find_element_by_class_name("login")
    elem.click()

    try:
        WebDriverWait(driver, 0).until(EC.alert_is_present(),
                                       'Timed out waiting for PA creation ' +
                                       'confirmation popup to appear.')
        alert = driver.switch_to.alert

        alert.accept()
        time.sleep(1)
        print("학번, id, 비밀번호 체크")
        driver.close()
        exit()

    except TimeoutException:
        print("no alert")

driver = webdriver.Chrome('')   # chromedriver 경로  link: https://chromedriver.storage.googleapis.com/index.html?path=2.35/
driver.get('http://sugang.knu.ac.kr/Sugang/comm/support/login/loginForm.action?redirUrl=%2FSugang%2Fcour%2FlectReq%2FonlineLectReq%2Flist.action')

snum = ''    # 학번
id = ''      # 아이디
passwd = ''  # 비밀번호
scode = ''   # 과목코드

login(snum, id, passwd)
data = {'lectReqCntEnq.search_open_yr_trm': '20181',
        'lectReqCntEnq.search_subj_cde': scode[0:7],
        'lectReqCntEnq.search_sub_class_cde': scode[7:],
        'searchValue': scode}

while True:
    try:
        elem = driver.find_element_by_id('timeStatus')
        sec = int(elem.text.split('초')[0])
    except:
        sec = 1200
        pass
    if sec < 50:
        elem = driver.find_element_by_class_name("stop")
        elem.click()
        login(snum, id, passwd)

    response = requests.post('http://my.knu.ac.kr/stpo/stpo/cour/lectReqCntEnq/list.action', data=data)
    cnt = int(BeautifulSoup(response.text, 'html.parser').find_all('', class_='lect_req_cnt')[2].text)

    print(cnt)
    if cnt < 70:
        elem = driver.find_element_by_id('lectPackReqGrid_0').find_element_by_class_name('button')  # 수강꾸러미 목록 위에서 부터 0, 1, 2, 3 ...
        elem.click()
        try:
            WebDriverWait(driver, 0).until(EC.alert_is_present(),
                                            'Timed out waiting for PA creation ' +
                                            'confirmation popup to appear.')
            alert = driver.switch_to.alert
            print("alert accepted")
            alert.text  # 수강신청 완료 메세지 확인 후 종료 코드 추가 필요
            alert.accept()

        except TimeoutException:
            print("no alert")

    time.sleep(1)   # 간격
