
import urllib.request
import urllib.parse
import json
import xlsxwriter
import time

def open_url(url,page_num,keywords):
    try:
        #设置post请求参数
        page_data=urllib.parse.urlencode([
                                   ('pn',page_num),
                                   ('kd',keywords)
                                   ])
        #设置headers
        page_headers={
            # User-Agent(UA) 服务器能够识别客户使用的操作系统及版本、CPU 类型、浏览器及版本、浏览器渲染引擎、浏览器语言、浏览器插件等。也就是说伪装成浏览器进行访问
          'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
          'Connection':'keep-alive',
          'Host':'www.lagou.com',
          'Origin':'https://www.lagou.com',
          'Cookie':'user_trace_token=20180216213417-15d771c4-131e-11e8-b071-5254005c3644; LGUID=20180216213417-15d77971-131e-11e8-b071-5254005c3644; ab_test_random_num=0; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=0; index_location_city=%E5%B9%BF%E5%B7%9E; _ga=GA1.2.1562325486.1518788057; JSESSIONID=ABAAABAABEEAAJA390B4E144EAEE25D48D9161EE1DE1E12; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1518788058,1518838484,1519288273; _gat=1; _gid=GA1.2.230939111.1519288273; LGSID=20180222163112-bd82e18f-17aa-11e8-8d2d-525400f775ce; PRE_UTM=m_cf_cpt_baidu_pc; PRE_HOST=bzclk.baidu.com; PRE_SITE=http%3A%2F%2Fbzclk.baidu.com%2Fadrc.php%3Ft%3D06KL00c00f7Ghk60yUKm0FNkUsjPx34p00000PW4pNb00000TN3zu1.THL0oUhY1x60UWYsnW0YrH0YndtzndqsusK15HbsnhR4nA7Bnj0snAf1njn0IHd7rjDdwH9AP1RvwDf3nbNAwWDsrH6znj7arRD4wWTYwfK95gTqFhdWpyfqn101n1csPHnsPausThqbpyfqnHm0uHdCIZwsT1CEQLILIz4_myIEIi4WUvYE5LNYUNq1ULNzmvRqUNqWu-qWTZwxmh7GuZNxTAn0mLFW5HRYPj6k%26tpl%3Dtpl_10085_15730_11224%26l%3D1500117464%26attach%3Dlocation%253D%2526linkName%253D%2525E6%2525A0%252587%2525E9%2525A2%252598%2526linkText%253D%2525E3%252580%252590%2525E6%25258B%252589%2525E5%25258B%2525BE%2525E7%2525BD%252591%2525E3%252580%252591%2525E5%2525AE%252598%2525E7%2525BD%252591-%2525E4%2525B8%252593%2525E6%2525B3%2525A8%2525E4%2525BA%252592%2525E8%252581%252594%2525E7%2525BD%252591%2525E8%252581%25258C%2525E4%2525B8%25259A%2525E6%25259C%2525BA%2526xp%253Did%28%252522m6c247d9c%252522%29%25252FDIV%25255B1%25255D%25252FDIV%25255B1%25255D%25252FDIV%25255B1%25255D%25252FDIV%25255B1%25255D%25252FH2%25255B1%25255D%25252FA%25255B1%25255D%2526linkType%253D%2526checksum%253D220%26ie%3Dutf-8%26f%3D8%26tn%3D02049043_23_pg%26wd%3D%25E6%258B%2589%25E5%258B%25BE%25E7%25BD%2591%26oq%3D%25E6%258B%2589%25E5%258B%25BE%25E7%25BD%2591%26rqlang%3Dcn%26ssl_s%3D0%26ssl_c%3Dssl6_1616e49070a; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F%3Futm_source%3Dm_cf_cpt_baidu_pc; _putrc=31CCBBEF3D9BD900; login=true; unick=%E9%B9%BF%E8%8F%B2; gate_login_token=5a273aeaf8e9271238beea63ccd937fec36f1661f0c89026; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1519288642; LGRID=20180222163721-99a7c9b0-17ab-11e8-8d2d-525400f775ce; TG-TRACK-CODE=index_search; SEARCH_ID=45d8793b697c4da1975be619b38a68c',
          'Accept':'application/json, text/javascript, */*; q=0.01',
          'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
            # 用于告诉服务器我是从哪个页面链接过来的，服务器基此可以获得一些信息用于处理。如果不加入，服务器可能依旧会判断为非法请求
          'Referer':'https://www.lagou.com/jobs/list_Python?labelWords=&fromSearch=true&suginput=',
          'X-Anit-Forge-Token':'None',
          'X-Requested-With':'XMLHttpRequest'
          }
        #打开网页
        req=urllib.request.Request(url,headers=page_headers)
        content=urllib.request.urlopen(req,data=page_data.encode('utf-8')).read().decode('utf-8')
        return content
    except Exception as e:
        print(str(e))

#获取招聘职位信息
def get_position(url,page_num):
    try:
        page_content=open_url(url,page_num,keywords)
        data=json.loads(page_content)
        content=data.get('content')
        result=[('positionId','职位ID'),('positionName','职位名称'),('salary','薪资'),('createTime','发布时间'),('workYear','工作经验'),('education','学历'),('positionLables','职位标签'),('jobNature','职位类型'),('firstType','职位大类'),('secondType','职位细类'),('positionAdvantage','职位优势'),('city','城市'),('district','行政区'),('businessZones','商圈'),('publisherId','发布人ID'),('companyId','公司ID'),('companyFullName','公司名'),('companyShortName','公司简称'),('companyLabelList','公司标签'),('companySize','公司规模'),('financeStage','融资阶段'),('industryField','企业领域'),('industryLables','企业标签')]
        positionResult=content.get('positionResult').get('result')# 输出返回的整个json信息中的职位相关信息
        if(len(positionResult)>0):
            for position in positionResult:
                #print(position['companyFullName'] + ':' + position['education'])
                with open("position3.txt",'a') as fh:
                    fh.write("---------------------------\n")
                for r in result:
                    with open("position3.txt",'a') as fh:
                        fh.write(str(r[1])+":"+str(position.get(r[0]))+"\n")
        return len(positionResult)
    except Exception as e:
        print(str(e))




#爬取拉勾网招聘职位信息
if __name__=="__main__":
    #爬取起始页
    url='https://www.lagou.com/jobs/positionAjax.json?city=%E5%B9%BF%E5%B7%9E&needAddtionalResult=false&isSchoolJob=0'
    #设置查询的关键词
    keywords="Python"
    page_num=1
    while True:
        print("正在爬取第"+str(page_num)+"页......")
        result_len=get_position(url,page_num)
        if(result_len>0):
            page_num+=1
        else:
            break

    print("爬取完成")

'''
import requests
import xlsxwriter
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
    'Referer': 'https://www.lagou.com/jobs/list_Python?px=default&gx=&isSchoolJob=1&city=%E5%B9%BF%E5%B7%9E',
    'Cookie': 'user_trace_token=20171010203203-04dbd95d-adb7-11e7-946a-5254005c3644; LGUID=20171010203203-04dbddae-adb7-11e7-946a-5254005c3644; index_location_city=%E5%B9%BF%E5%B7%9E; JSESSIONID=ABAAABAABEEAAJA8BF3AD5C8CFD40070BD3A86E50B0F9E4; PRE_UTM=; PRE_HOST=; PRE_SITE=https%3A%2F%2Fwww.lagou.com%2F; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fjobs%2Flist_Python%3FlabelWords%3D%26fromSearch%3Dtrue%26suginput%3D; TG-TRACK-CODE=index_navigation; SEARCH_ID=0cc609743acc4bf18789b584210f6ccb; _gid=GA1.2.271865682.1507638722; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1507638723; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1507720548; _ga=GA1.2.577848458.1507638722; LGSID=20171011190218-a611d705-ae73-11e7-8a7a-525400f775ce; LGRID=20171011191547-882eafd3-ae75-11e7-8a92-525400f775ce'
}


def getJobList(page):
    formData = {
        'first': 'false',daw
        'pn': page,
        'kd': 'Python'
    }
    res = requests.post(
        # 请求的url
        url='https://www.lagou.com/jobs/positionAjax.json?city=%E5%B9%BF%E5%B7%9E&needAddtionalResult=false&isSchoolJob=0',
        # 添加headers信息
        headers=headers
    )
    result = res.json()
    jobsInfo = result['content']['positionResult']['result']
    return jobsInfo

# 创建一个excel表格
workbook = xlsxwriter.Workbook('Python职位信息.xlsx')
# 为创建的excel表格添加一个工作表
worksheet = workbook.add_worksheet()

# 将数据写入工作表中
def writeExcel(row=0, positionId='职位ID', positionName='职位名称', salary='薪资', createTime='发布时间', workYear='工作经验',
                       education='学历', firstType='职位大类', city='城市', companyFullName='公司名'):
    if row == 0:
        worksheet.write(row, 0, positionId)
        worksheet.write(row, 1, positionName)
        worksheet.write(row, 2, salary)
        worksheet.write(row, 3, createTime)
        worksheet.write(row, 4, workYear)
        worksheet.write(row, 5, education)
        worksheet.write(row, 6, firstType)
        worksheet.write(row, 7, city)
        worksheet.write(row, 8, companyFullName)
    else:
        worksheet.write(row, 0, job['positionId'])
        worksheet.write(row, 1, job['positionName'])
        worksheet.write(row, 2, job['salary'])
        worksheet.write(row, 3, job['createTime'])
        worksheet.write(row, 4, job['workYear'])
        worksheet.write(row, 5, job['education'])
        worksheet.write(row, 6, job['firstType'])
        worksheet.write(row, 7, job['city'])
        worksheet.write(row, 8, job['companyFullName'])
# 在第一行中写入列名
writeExcel(row=0)
# 从第二行开始写入数据
row = 1
# 这里爬取前五页招聘信息做一个示范
for page in range(1, 7):
    # 爬取一页中的每一条招聘信息
    for job in getJobList(page=page):
        # 将爬取到的信息写入表格中
        writeExcel(row = row,positionId=job['positionId'], positionName=job['positionName'], salary=job['salary'], createTime=job['createTime'], workYear=job['workYear'],
                       education=job['education'], firstType=job['firstType'], city=job['city'], companyFullName=job['companyFullName'])
        row += 1
    print('第 %d 页已经爬取完成' % page)
    # 做适当的延时
    time.sleep(0.5)
# 关闭表格文件
workbook.close()
print('爬取的结果在Python职位信息.xlsx中')
'''

