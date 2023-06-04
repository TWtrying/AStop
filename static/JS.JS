//全局变量
const Http = new XMLHttpRequest();
var userid = "AStop";
var h=0,m=0;
var text;

//背景模糊
function bgfilter(t){
    if(t==1){
        document.getElementById("header").style.filter = "blur(10px)";
        document.getElementById("body").style.filter = "blur(10px)";
    }
    else{
        document.getElementById("header").style.filter = "none";
        document.getElementById("body").style.filter = "none";
    }
}

function init(){
    console.log("初始化");
    logino();
}
//登录界面打开
function logino(){
    bgfilter(1);
    document.getElementById("login").style.display = "flex";
}
//登录界面关闭
function loginc(){
    console.log("登录");
    userid = document.getElementById("userid").value;
    var url = "http://127.0.0.1:6868/login?id=" + userid;
    Http.open("GET",url);
    Http.send();
    Http.onreadystatechange = function(e){
        if(Http.readyState == 4 && Http.status == 200){
            var t = JSON.parse(Http.responseText);
            console.log(t);
            if(t["code"]==0 || t["code"]==1){
                updateusername();
                bgfilter(0);
                document.getElementById("login").style.display = "none";
            }
            if(t["code"]==2){
                document.getElementById("userid").value = "输入错误!";
            }
        }
    }
}
//停车界面打开
function sscaro(){
    var url = "http://127.0.0.1:6868/sscar?id=" + userid;
    Http.open("GET",url);
    Http.send();
    Http.onreadystatechange = function(e){
        if(Http.readyState == 4 && Http.status == 200){
            var t = JSON.parse(Http.responseText);
            if(t["code"] == '1'){
                document.getElementById("carplace").innerHTML = "车位已满";
            }
            if(t["code"] == '2'){
                document.getElementById("carplace").innerHTML = "请登录";
            }
            if(t["code"] == '3'){
                document.getElementById("carplace").innerHTML = "您已停车";
            }
            if(t["code"] == '4'){
                document.getElementById("carplace").innerHTML = "上次订单未付款";
            }
            else{
                var a = Number(t["code"])-100;
                console.log("ok");
                document.getElementById("carplace").innerHTML = "您的位置在:"+String(a)+"号";
            }
            bgfilter(1);
            document.getElementById("sscar").style.display = "flex";
        }
    }
}
//停车界面关闭
function sscarc(){
    bgfilter(0);
    document.getElementById("sscar").style.display = "none";
}
//结束界面打开
function endcaro(){
    var url = "http://127.0.0.1:6868/endcar?id=" + userid;
    Http.open("GET",url);
    Http.send();
    Http.onreadystatechange = function(e){
        if(Http.readyState == 4 && Http.status == 200){
            var t = JSON.parse(Http.responseText);
            if(t["code"]=='0'){
                var s = t["msg"].split(':');
                document.getElementById("endtext").innerHTML = "您停车用时为:"+s[0]+"时"+s[1]+"分";
            }
            else if(t["code"]=='3')
                document.getElementById("endtext").innerHTML = "上次订单未付款";
            else
                document.getElementById("endtext").innerHTML = "使用愉快!";
            bgfilter(1);
            document.getElementById("endcar").style.display = "flex";
        }
    }
}
//结束界面关闭
function endcarc(){
    var url = "http://127.0.0.1:6868/pay?id=" + userid+"&s="+'0';
    Http.open("GET",url);
    Http.send();
    Http.onreadystatechange = function(e){
        if(Http.readyState == 4 && Http.status == 200){
            var t = JSON.parse(Http.responseText);
            if(t["code"]=='0'){
                window.open('http://127.0.0.1:6868/payindex?id='+userid,'_self');
            }
            bgfilter(0);
            document.getElementById("endcar").style.display = "none";
        }
    }
}

function updateusername(){
    var a = new Date();
    var time = a.getHours();
    if(time >=6 && time<= 11)
        document.getElementById("Ntime").innerHTML="上午好:"+userid;
    else if(time >=12 && time<= 19)
        document.getElementById("Ntime").innerHTML="下午好:"+userid;
    else if(time >=20 && time<= 24)
        document.getElementById("Ntime").innerHTML="晚上好:"+userid;
    else
        document.getElementById("Ntime").innerHTML="凌晨好:"+userid;
}