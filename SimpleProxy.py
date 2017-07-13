#-*-coding:utf-8-*-

import requests
import time
from multiprocessing import Pool#多进程
import random
from lxml import etree
import MySQLdb as db
import pandas as pd

'''浏览器伪装——随机获取HTTP_User_Agent'''
def getUserAgent():
    user_agents = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
    "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10"
    ]
    user_agent = random.choice(user_agents)
    return user_agent

# 定制请求头
def Header():
    user_agent = getUserAgent()
    headers = {
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding":"gzip, deflate, sdch",
        "Accept-Language":"zh-CN,zh;q=0.8",
        "Cache-Control":"max-age=0",
        "Connection":"keep-alive",
        "Host":"www.xicidaili.com",
        "Upgrade-Insecure-Requests":"1",
        'User-Agent':user_agent
    }
    return headers

'''代理IP爬取——西刺国内高匿代理'''
def getProxies():
    init_proxies = []
    # 爬取前10页
    for i in range(1,2):
        url = 'http://www.xicidaili.com/nn/'+str(i)
        headers = Header()
        try:
            data = requests.get(url,headers=headers,timeout=30).text
        except Exception, e:
            print '爬取异常：————',e
        selector = etree.HTML(data)
        tr_se = selector.xpath('//tr[@class="odd"]')
        # iplist = []
        for line in tr_se:
            htpl = line.xpath('td[6]/text()')[0]#http or https
            if 'HTTP'==htpl:
                ver_time = line.xpath('td[7]/div/@title')[0][:-1]#连接速度
                if float(ver_time) < 5:
                    ip_adres = line.xpath('td[2]/text()')[0]#ip地址
                    port = line.xpath('td[3]/text()')[0]#端口
                    # sur_time = line.xpath('td[9]/text()')#存活时间
                    ip = 'http://'+ip_adres+':'+port
                    init_proxies.append(ip)
        return init_proxies


'''
Function：代理ip验证
@curr_ip：原始未验证代理IP-list
'''
def testProxy(curr_ip):
    tarUrl = 'http://www.plateno.com/list.html'
    # print proxies_temp
    tmp_proxies = []#存放可用ip
    for prox in curr_ip:
        proxies_temp={
        "http": prox,
        }
        headers = Header()
        try:
            data = requests.get(tarUrl,headers=headers,timeout=8,proxies=proxies_temp)
            # 当相应状态是200则是可用的
            if data.status_code==200:
                print prox,'可用'
                tmp_proxies.append(prox)#ip可用就把此IP追加到tmp_proxies

        except Exception, e:
            print '代理ip错误：',prox
        time.sleep(2)
    return tmp_proxies
        

'''
Function：创建数据库表
'''
def createtable():
    con = db.connect('localhost','root','123456','simpleproxies',charset='utf8')
    cur = db.cursor()
    cursor.execute('DROP TABLE IF EXISTS testip')
    sql = '''
        create table testip(
        sid int primary key not null auto_increment,
        ip varchar(300),
        ver_time varchar(60)
        )
    '''
    cur.execute(sql)#创建数据表SQL语句
    cur.close()
    con.close()#关闭数据库连接
    return True


'''
Function：写入数据库
@iplist：验证后的ip
'''
def InsertDB(iplist):
    # print iplist
    # createtable()#不存在表就创建一个
    # ip地址，用户名，密码，库名，编码方式
    con = db.connect('127.0.0.1','root','123456','simpleproxies',charset='utf8')
    cur = con.cursor()#使用cursor方法获取操作游标
    print iplist
    cur.execute("truncate table testip")
    for ip in iplist:
        try:
            print ip
            cur.execute("insert into testip(ip) values('%s');"%(ip))
        except Exception, e:
            print 'Insert Error：',e
    con.commit()
    cur.close()
    con.close()
    return True

'''
Function：查询数据库里的IP进行验证
return：可用IP list
'''
def selectDB():
    con = db.connect('localhost','root','123456','simpleproxies',charset='utf8')
    cur = con.cursor()
    sql = 'select ip from testip'
    selectiplist = []#存储从数据库查询出来的ip
    try:
        cur.execute(sql)#执行sql语句
        # fetchone(): 该方法获取下一个查询结果集。结果集是一个对象
        # fetchall():接收全部的返回结果行.
        # rowcount: 这是一个只读属性，并返回执行execute()方法后影响的行数。
        results = cur.fetchall()
        for row in results:
            ip = row[0]
            # print ip
            selectiplist.append(ip)
            
    except Exception as e:
        print 'select Error：',e
    # 把从数据库查询出来的数据进行第二次验证
    Secverification = testProxy(selectiplist)

    cur.close()
    con.close()
    return Secverification

'''
Function：数据库删除操作
'''
def deleteDB(delip):
    con = db.connect('localhost','root','123456','simpleproxies',charset='utf8')
    cur = con.cursor()#使用cursor()方法获取操作游标
    sql = "DELETE FROM testip WHERE ip='%s'"%delip
    try:
        cur.execute(sql)#执行SQL语句
        con.commit()#提交修改
    except Exception as e:
        con.rollback()#发生错误时回滚
    cur.close()
    con.close()

'''
Function：函数调用
'''
def main():
    gepo = getProxies()
    testlist = testProxy(gepo)
    print type(testlist),testlist
    InsertDB(testlist)


if __name__ == '__main__':
    # main()
    selectDB()#查询数据库里的IP进行验证

