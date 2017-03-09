# -*- coding: utf-8 -*-
import re
import requests
import http.cookiejar
import time
import string
import json
from lxml import html
from User import User


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:48.0) Gecko/20100101 Firefox/48.0'}
ajax_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:48.0) Gecko/20100101 Firefox/48.0',
            'X-Requested-With': 'XMLHttpRequest'}

filename = 'cookie'

# 建立一个会话，可以把同一用户的不同请求联系起来；直到会话结束都会自动处理cookies
session = requests.Session()
# 建立LWPCookieJar实例，可以存Set-Cookie3类型的文件。
# 而MozillaCookieJar类是存为'/.txt'格式的文件
session.cookies = http.cookiejar.LWPCookieJar(filename)
# 若本地有cookie则不用再post数据了
try:
    session.cookies.load(filename=filename, ignore_discard=True)
except:
    print('Cookie has not been loaded！')

def login_myAdmin(username, password):

    print '........................................'
    print 'Logging in...at', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    url = 'https://onestopadmin.uts.edu.au/estudent/Login.aspx'
    response = session.get(url, headers=headers, allow_redirects=True)
    page = html.fromstring(response.text)

    #get post data
    viewstate_nodes = page.xpath('//*[@id="__VIEWSTATE"]')
    viewstate_value = viewstate_nodes[0].get('value')
    eventvalidation_nodes = page.xpath('//*[@id="__EVENTVALIDATION"]')
    eventvalidation_value = eventvalidation_nodes[0].get('value')
    viewstategenerator_nodes = page.xpath('//*[@id="__VIEWSTATEGENERATOR"]')
    viewstategenerator_value = viewstategenerator_nodes[0].get('value')

    login_data = {"__EVENTTARGET":'ctl00$Content$cmdLogin',
            "__EVENTARGUMENT":'',
            "__VIEWSTATE": viewstate_value,
            "__VIEWSTATEGENERATOR": viewstategenerator_value,
            "__SCROLLPOSITIONX":0,
            "__SCROLLPOSITIONY":125,
            "__EVENTVALIDATION": eventvalidation_value,
            "ctl00$Content$txtUserName$txtText":username,
            "ctl00$Content$txtPassword$txtText":password}

    result = session.post(url, data=login_data, headers=headers)
    print(result)
    # 保存cookie到本地
    session.cookies.save(ignore_discard=True, ignore_expires=True)

def login_myTimetable(username, password):

    print '........................................'
    print 'Logging in...at', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    url = 'https://mytimetable.uts.edu.au/aplus2017/rest/student/login'
    login_data = {'username': username, 'password': password}
    response = session.post(url, data=login_data, headers=ajax_headers)

    response_dict =  response.json()

    if (response_dict['success'] == True):
        print 'login successfully'
        token = response_dict['token']
        user.setToken(token)
    else:
        print 'Failed to log in'



def get_studyplan_page():

    get_url = 'https://onestopadmin.uts.edu.au/eStudent/SM/StudyPlanDtls10.aspx?r=UTS.EST.WEB02&f=UTS.EST.STUDYPLN.WEB&t=UTS.EST.ENRDTLS.WEB'
    resp = session.get(get_url, headers=headers, allow_redirects=True)
    page = html.fromstring(resp.text)

    #check if the user has multiple courses
    page_headers = page.xpath('//*[@id="ctl00_h1PageTitle"]')
    if (page_headers[0].text_content().find('Choose a Study Plan') != -1):
        courses_list = page.xpath('//*[@id="ctl00_Content_grdComponentPlans"]/tbody//tr/td[4]')
        print "You have ", len(courses_list), "courses:"
        for course in courses_list:
            print course.text_content()

        course_specified = 1

        #get specified course selector
        courses_seclector_list = page.xpath('//*[@id="ctl00_Content_grdComponentPlans"]/tbody/tr/td[2]/input')
        course_specified_seclector = courses_seclector_list[course_specified].get('value')

        #get post data
        viewstate_nodes = page.xpath('//*[@id="__VIEWSTATE"]')
        viewstate_value = viewstate_nodes[0].get('value')
        eventvalidation_nodes = page.xpath('//*[@id="__EVENTVALIDATION"]')
        eventvalidation_value = eventvalidation_nodes[0].get('value')
        viewstategenerator_nodes = page.xpath('//*[@id="__VIEWSTATEGENERATOR"]')
        viewstategenerator_value = viewstategenerator_nodes[0].get('value')


        post_url = 'https://onestopadmin.uts.edu.au/eStudent/SM/StudyPlanDtls10.aspx?r=UTS.EST.WEB02&f=UTS.EST.STUDYPLN.WEB&t=UTS.EST.ENRDTLS.WEB'
        studyplan_data = {"__EVENTTARGET":'ctl00$Content$grdComponentPlans',
            "__EVENTARGUMENT":'ViewSsp$1',
            "hdnCurrentTabValue": 'UTS.EST.ENRDTLS.WEB',
            "__VIEWSTATE": viewstate_value,
            "__VIEWSTATEGENERATOR": viewstategenerator_value,
            "__SCROLLPOSITIONX":0,
            "__SCROLLPOSITIONY":125,
            "__VIEWSTATEENCRYPTED": '',
            "__EVENTVALIDATION": eventvalidation_value,
            "rbSelectSsp": course_specified_seclector}

        #submit the specified course using its post data
        result = session.post(post_url, data=studyplan_data, headers=headers)
        studyplan_page_html = result.text
        return studyplan_page_html

    else:
        studyplan_page_html = resp.text
        return studyplan_page_html

def get_home_page():

    token = user.getToken()
    home_url = 'https://mytimetable.uts.edu.au/aplus2017/student?ss=' + token
    rp = session.get(home_url, headers=ajax_headers, allow_redirects=True)
    return rp.text

def login(username, password, choice='myAdmin'):

    if (choice == 'myAdmin'):
        login_myAdmin(username, password)
    elif (choice == 'myTimetable'):
        login_myTimetable(username, password)
    else:
        print 'Failed to log in'



def parse_html(html_page):

    tree = html.fromstring(html_page)

    print '........................................'

    subjects_available = tree.xpath('//*[contains(@class, "cssSelectableRow")]')
    #number of available subjects
    print len(subjects_available), "subject(s) available:"

    subjects_name = tree.xpath('//*[contains(@class, "cssSelectableRow")]/div[@class="cssMainContentRight"]//span[@class="cssContentTopText"]')
    for subject in subjects_name:
        print subject.text_content()

    print '........................................'

    target = user.target_subject
    for subject in subjects_name:
        if (subject.text_content() == target):
            print "Subject found! Message has been sent!"
            user.send_SMS("Target subject found!")
            return 
    print "Sorry, target Subject not found."

def extractFrom(page):

    page_home = html.fromstring(page)
    temp_nodes = page_home.xpath('/html/body/script')
    temp_node = temp_nodes[0]
    # Get json data using re
    matchObj = re.search(r'data=(.*);', temp_node.text_content())
    json_data = matchObj.group(1)

    return json.loads(json_data)



def handle(choice='myAdmin'):

    if(choice == 'myAdmin'):
        page = get_studyplan_page()
        parse_html(page)
    if(choice == 'myTimetable'):
        page = get_home_page()
        student_dict = extractFrom(page)

        student_allocated_dict = student_dict['student']['allocated']
        student_enrolment_dict = student_dict['student']['student_enrolment']

        subject_list = []
        subject_acts_list = []

        for subject in student_enrolment_dict:

            subject_dict = student_enrolment_dict[subject]

            for group in subject_dict['groups']:

                acts_url = 'https://mytimetable.uts.edu.au/aplus2017/rest/student/' + user.accountID + '/subject/' + subject + '/group/' + group + '/activities/?ss=' + user.getToken()
                rp = session.get(acts_url, headers=headers, allow_redirects=True)
                acts_dict =  rp.json()

                for act in acts_dict:
                    print act, ':', acts_dict[act]['selectable']



if __name__ == '__main__':

    user = User()

    user.detail()

    login(user.accountID, user.password, user.loginChoice)

    handle(user.loginChoice)

  