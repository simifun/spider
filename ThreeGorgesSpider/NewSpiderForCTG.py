# coding=utf-8
import urllib
import urllib2
import cookielib
import re
import datetime
import signal
import json

# get起始日期
try:
    readDate = open("date.txt", "r")
finally:
    y = int(readDate.readline())
    m = int(readDate.readline())
    d = int(readDate.readline())
    readDate.close()


# 中断时记录起始日期
def recvsign(s, f):
    print '中断！得到信号：', s
    try:
        writeate = open("date.txt", "w")
    finally:
        writeate.write(str(date)[0:4] + '\n')
        writeate.write(str(date)[5:7] + '\n')
        writeate.write(str(date)[8:10] + '\n')
        writeate.close()
        exit(0)


signal.signal(signal.SIGTERM, recvsign)
signal.signal(signal.SIGINT, recvsign)
##signal.signal(signal.SIGKILL,recvsign)

startdate = datetime.datetime(y, m, d)
enddate = datetime.datetime(2016, 3, 1)

print 'start'
while startdate != enddate:
    date = startdate.strftime("%Y-%m-%d")
    print date
    postdata = urllib.urlencode({
        'time': date
    })
    req = urllib2.Request(
        url='http://www.ctg.com.cn/eportal/ui?moduleId=50c13b5c83554779aad47d71c1d1d8d8'
            + '&&struts.portlet.mode=view&struts.portlet.action=/portlet/waterFront!getDatas.action',
        data=postdata
    )
    try:
        result = urllib2.urlopen(req)
    except urllib2.URLError, e:
        print e.reason
        try:
            writeate = open("date.txt", "w")
        finally:
            writeate.write(str(date)[0:4] + '\n')
            writeate.write(str(date)[5:7] + '\n')
            writeate.write(str(date)[8:10] + '\n')
            writeate.close()
            exit(0)
        break
    else:
        content = result.read()
        dictContent = eval(content)
        # 三峡入库

        rkList = list(dictContent['rkList'])
        try:
            fileout = open("三峡入库.txt", "a")
        finally:
            for i in range(0, rkList.__len__())[::-1]:
                rkDic = eval(str(rkList[i]))
                lineDate = date + "\t" + rkDic['v'] + "\t" + rkDic['time'] + '时\n'
                fileout.write(lineDate)
            fileout.close()

        # 三峡出库
        ckList = list(dictContent['ckList'])
        try:
            fileout = open("三峡出库.txt", "a")
        finally:
            for i in range(0, ckList.__len__())[::-1]:
                ckDic = eval(str(ckList[i]))
                lineDate = date + "\t" + ckDic['v'] + "\t" + ckDic['time'] + '时\n'
                fileout.write(lineDate)
            fileout.close()

        # 三峡上游水位
        syList = list(dictContent['syList'])
        try:
            fileout = open("三峡上游水位.txt", "a")
        finally:
            for i in range(0, syList.__len__())[::-1]:
                syDic = eval(str(syList[i]))
                lineDate = date + "\t" + syDic['v'] + "\t" + syDic['time'] + '时\n'
                fileout.write(lineDate)
            fileout.close()

        # 三峡下游水位
        xyList = list(dictContent['xyList'])
        try:
            fileout = open("三峡下游水位.txt", "a")
        finally:
            for i in range(0, xyList.__len__())[::-1]:
                xyDic = eval(str(xyList[i]))
                lineDate = date + "\t" + xyDic['v'] + "\t" + xyDic['time'] + '时\n'
                fileout.write(lineDate)
            fileout.close()

        startdate = startdate + datetime.timedelta(1)
