import time

#时间,操作,是否成功
#1>>> 2023:05:28:14:20:54 增加 ok

class AStoplog:
    Index =None
    LogFile = None

    def __init__(self,name='AStop\log.txt') -> None:
        print('日志打开')
        self.Index = 1
        self.LogFile = open(name,'r',encoding='utf-8')
        s = self.LogFile.readline()
        if(s != ''):
            self.Index = int(s.split(' ')[0][:-3])
            while s:
                s = self.LogFile.readline()
                if s!='':
                    self.Index = int(s.split(' ')[0][:-3])
            self.Index+=1
        self.LogFile.close()
        self.LogFile = open(name,'a',encoding='utf-8')
            

    def WLog(self,mode,msg):
        LogTime = time.strftime('%Y:%m:%d:%H:%M:%S',time.localtime(time.time()))
        msg = "{}>>> {} {} {}\n".format(self.Index,LogTime,mode,msg)
        self.Index+=1
        t = self.LogFile.write(msg)
        self.LogFile.flush()
        print('日志写入'+str(t))
        return

    def _del_(self):
        self.LogFile.close()