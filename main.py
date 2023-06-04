import re
import time
from flask import Flask,render_template,request
from Log import AStoplog

SUMSTOP = 100


def is_car(str) -> int:
    if re.findall("^[京津沪渝冀豫云辽黑湘皖鲁新苏浙赣鄂桂甘晋蒙陕吉闽贵粤青藏川宁琼A-Z][A-Z]{1}[A-Z0-9]{4}[A-Z0-9挂学警港澳]{1}$", str):
        return 1
    return 0

def gettime() -> str:
    return str(time.strftime('%H:%M',time.localtime(time.time())))

def getvalue(str) -> str:
    value = request.values.get(str)
    if value != None:
        return value
    return 'error'

class AStop:
    Id = {}
    Book = []
    h=0
    m=0
    #初始化用户类
    def __init__(self):
        for i in range(100):
            self.Book.append('0')

    ''' 分配车位
    传入id(车牌)
    返回值为
        100+车位号(成功)
        1(车位已满)
        2(车牌未登录)
        3(车牌已停车)
    '''   
    def getstop(self,id) -> int:
        if self.Book.count('0') == 0:
            print("车位已满")
            return 1
        if id not in self.Id:
            print("当前车牌未登录")
            return 2
        if id in self.Book:
            print("当前车牌已停车")
            return 3
        t = self.Book.index('0')
        self.Book[t] = id
        return t+101
    
    ''' 删除车位
    传入id(车牌)
    返回值为
        0(成功)
        1(车牌未停车)
    '''   
    def outstop(self,id) -> int:
        if id not in self.Book:
            print("未停车")
            return 1
        print("删除车位")
        self.Book[self.Book.index(id)] = '0'
        return 0


    ''' 添加Id
    传入id(车牌)
    返回值为
        0(成功)
        1(已存在)
        2(车牌错误)
    '''
    def add_id(self,id) -> int:
        print("*****添加用户*****")
        if id in self.Id:
            print("当前车牌已存在")
            return 1
        if is_car(id) == 0:
            print("当前车牌格式错误")
            return 2
        self.Id.update({id:'0'})
        return 0
    
    ''' 实时停车
    传入id(车牌)
    返回值为
        0(成功)
        1(车位已满)
        2(车牌未登录)
        3(车牌已停车)
        4(未付款)
    '''
    def sscar(self,id):
        print("*****实时停车*****")
        if self.Id[id][0] == 'd:':
            return 4
        t = self.getstop(id)
        if t == 1:
            return 1
        if t == 2:
            return 2
        if t == 3:
            return 3
        time = gettime()
        self.Id[id] = time
        return t

            
    ''' 结束停车
    传入id(车牌)
    返回值为
        0(成功)
        1(车牌未停车)
        3(未结账)
    '''
    def endcar(self,id):
        print("*****结束停车*****")
        if self.Id[id][0] == 'd':
            print('未结账')
            return 3
        if self.Id[id] == '0':
            print('车牌未停车')
            if id in self.Book:
                self.Book[self.Book.index(id)] = '0'
            return 1
        time = gettime().split(':')
        otime = self.Id[id].split(':')
        self.Id[id] = '0'
        time[0] = int(time[0])
        time[1] = int(time[1])
        otime[0] = int(otime[0])
        otime[1] = int(otime[1])
        print(time)
        print(otime)
        if otime[0] <= time[0]:
            h = time[0]-otime[0]
        else:
            h=time[0]+24 - otime[0]
        
        if otime[1] > time[1]:
            h=h-1
            m=time[1]+60-otime[1]
        else:
            m=time[1]-otime[1]
        t = self.outstop(id)
        if t == 1:
            return 1
        if h==0 and m==0:
            self.Id[id] = '0'
        else:
            self.Id[id] = 'd:'+str(h)+':'+str(m)
        print(self.Id[id])
        return 0
    




stop = Flask(__name__)

a = AStop()
log = AStoplog()
#主页面
@stop.route('/')
def run():
    log.WLog('页面','打开主页')
    return render_template('index.HTML')

#登录页面
@stop.route('/login',methods=["GET"])
def login():
    id = getvalue('id')
    t = a.add_id(id)
    log.WLog('登录','登录账户'+id+'状态码:'+str(t))
    return {'code':t,'msg':'0'}

@stop.route('/sscar',methods=["GET"])
def sscar():
    id = getvalue('id')
    t = a.sscar(id)
    log.WLog('停车','停车账户'+id+'状态码:'+str(t))
    return {'code':t,'msg':'0'}

@stop.route('/endcar',methods=["GET"])
def endcar():
    id = getvalue('id')
    t = a.endcar(id)
    if t == 0:
        if a.Id[id] != '0':
            time = a.Id[id].split(':')
            log.WLog('离开','离开账户'+id+'状态码:'+str(t))
            return {'code':t,'msg':str(time[1])+':'+str(time[2])}
        else:
            log.WLog('离开','离开账户'+id+'状态码:'+str(t))
            return {'code':t,'msg':'0:0'}
    log.WLog('离开','离开账户'+id+'状态码:'+str(t))
    return {'code':t,'msg':'0'}

@stop.route('/payindex',methods=["GET"])
def payindex():
    id = getvalue('id')
    log.WLog('页面',id+'打开支付')
    return render_template('dd.HTML',userid=id)

@stop.route('/pay',methods=["GET"])
def pay():
    s = getvalue('s')
    id = getvalue('id')
    if s == '1':
        if id in a.Id:
            a.Id[id] = '0'
            log.WLog('支付',id+'申请支付'+'状态码:0')
            return {'code':0,'msg':'0'}
        log.WLog('支付',id+'申请支付'+'状态码:1')
        return {'code':1,'msg':'0'}
    else:
        if id in a.Id:
            if a.Id[id][0] == 'd':
                log.WLog('支付',id+'扫码支付'+'状态码:0')
                return {'code':'0','msg':a.Id[id]}
        log.WLog('支付',id+'扫码支付'+'状态码:1')
        return {'code':'1','msg':'0'}


@stop.route('/admin',methods=["GET"])
def admin():
    return render_template('admin.HTML')


@stop.route('/adminop',methods=["GET"])
def anminop():
    return 'ok'

stop.run(host='127.0.0.1',port=6868)