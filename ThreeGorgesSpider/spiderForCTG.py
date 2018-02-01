# coding=utf-8
import urllib
import urllib2
import cookielib
import re
import datetime
import signal

# get起始日期
try:
    readDate = open("起始日期.txt", "r")
finally:
    y = int(readDate.readline())
    m = int(readDate.readline())
    d = int(readDate.readline())
    readDate.close()


# 中断时记录起始日期
def recvsign(s, f):
    print '中断！得到信号：', s
    try:
        writeate = open("起始日期.txt", "w")
    finally:
        writeate.write(str(date)[0:4])
        writeate.write(str(date)[5:7])
        writeate.write(str(date)[8:10])
        writeate.close()
        exit(0)


signal.signal(signal.SIGTERM, recvsign)
signal.signal(signal.SIGINT, recvsign)
##signal.signal(signal.SIGKILL,recvsign)

startdate = datetime.datetime(y, m, d)
enddate = datetime.datetime(2016, 3, 1)

print 'start'
while True:
    while startdate != enddate:
        date = startdate.strftime("%Y-%m-%d")
        print date
        postdata = urllib.urlencode({
            'NeedCompleteTime2': date
        })
        req = urllib2.Request(
            url='http://www.ctg.com.cn/sxjt/sqqk/index.html',
            data=postdata
        )
        try:
            result = urllib2.urlopen(req)
        except urllib2.URLError, e:
            print e.reason
            break
        else:
            content = result.read()
            # 三峡入库
            pattern = re.compile(
                '<td valign="top"><table width="100%" border="0" cellpadding="0" cellspacing="0".*?tr>.*?'
                + '<td colspan="2" bgcolor="#DEEFDE"><div align="center">(.*?)'
                + '<td colspan="2" bgcolor="#DEEFDE"><div align="center">', re.S)
            items = re.findall(pattern, content)
            dst = ''.join(items)
            pattern = re.compile('<td.*?\'right\'>(.*?)</td.*?\'right\'>(.*?)</td>', re.S)
            items = re.findall(pattern, dst)
            try:
                fileout = open("三峡入库.txt", "a")
            finally:
                for i in items:
                    k = '\t'.join([str(j) for j in i])
                    fileout.write(date + "\t" + k.replace("&nbsp;", "", ) + '\n')
                fileout.close()

            # 三峡出库
            pattern = re.compile(
                '<td valign="top"><table width="100%" border="0" cellpadding="0" cellspacing="0".*?tr>.*?'
                + '<td colspan="2" bgcolor="#DEEFDE"><div align="center">.*?'
                + '<td colspan="2" bgcolor="#DEEFDE"><div align="center">(.*?)</table>', re.S)
            items = re.findall(pattern, content)
            dst = ''.join(items)
            pattern = re.compile('<td.*?\'right\'>(.*?)</td.*?\'right\'>(.*?)</td>', re.S)
            items = re.findall(pattern, dst)
            try:
                fileout = open("三峡出库.txt", "a")
            finally:
                for i in items:
                    k = '\t'.join([str(j) for j in i])
                    fileout.write(date + "\t" + k.replace("&nbsp;", "", ) + '\n')
                fileout.close

            # 三峡上游水位
            pattern = re.compile(
                '<td valign="top"><table width="100%" border="0" cellpadding="0" cellspacing="0".*?tr>.*?'
                + '<td colspan="2" bgcolor="#DEEFDE"><div align="center">.*?'
                + '<td colspan="2" bgcolor="#DEEFDE"><div align="center">.*?</table.*?>'
                + '<div align="center">(.*?)</table>', re.S)
            items = re.findall(pattern, content)
            dst = ''.join(items)
            pattern = re.compile('<td.*?\'right\'>(.*?)</td.*?\'right\'>(.*?)</td>', re.S)
            items = re.findall(pattern, dst)
            try:
                fileout = open("三峡上游水位.txt", "a")
            finally:
                for i in items:
                    k = '\t'.join([str(j) for j in i])
                    fileout.write(date + "\t" + k.replace("&nbsp;", "", ) + '\n')
                fileout.close

            # 三峡下游水位
            pattern = re.compile(
                '<td valign="top"><table width="100%" border="0" cellpadding="0" cellspacing="0".*?tr>.*?'
                + '<td colspan="2" bgcolor="#DEEFDE"><div align="center">.*?'
                + '<td colspan="2" bgcolor="#DEEFDE"><div align="center">.*?'
                + '<td colspan="2" bgcolor="#DEEFDE"><div align="center">.*?</table.*?>'
                  '<div align="center">(.*?)</table>', re.S)
            items = re.findall(pattern, content)
            dst = ''.join(items)
            pattern = re.compile('<td.*?\'right\'>(.*?)</td.*?\'right\'>(.*?)</td>', re.S)
            items = re.findall(pattern, dst)
            try:
                fileout = open("三峡下游水位.txt", "a")
            finally:
                for i in items:
                    k = '\t'.join([str(j) for j in i])
                    fileout.write(date + "\t" + k.replace("&nbsp;", "", ) + '\n')
                fileout.close

            startdate = startdate + datetime.timedelta(1)
