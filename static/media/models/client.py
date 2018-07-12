#coding=utf-8
import os
import math
import pandas as pd
import csv
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
import matplotlib.pyplot as plt
from tkinter.filedialog import askopenfilename
from PIL import Image
from PIL import ImageTk
import tkinter
from tkinter import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg,NavigationToolbar2TkAgg
from tkinter.scrolledtext import ScrolledText
from  tkinter  import ttk
from urllib import parse, request
import pandas as pd 
import requests
import random
import tkinter.messagebox
from tkinter.filedialog import askdirectory
import json
tf.reset_default_graph()
rnn_unit=10       #隐层数量
input_size=14
output_size=1
lr=0.0006         #学习率
train_num=3000
iterator_num=1000
key=1
#——————————————————导入数据——————————————————————
#base_url = "http://192.168.0.100:5000"base_url = "http://192.168.0.100:5000"
base_url = "http://192.168.43.197:5000"
def getStockData(公司名称, 开始日期, 结束日期):
    url = base_url + "/api/stock_data"
    dic = {
        "公司名称": 公司名称,
        "开始日期": 开始日期,
        "结束日期": 结束日期
    }
    dic = parse.urlencode(dic)
    response = request.urlopen(url + "?" + dic)
    data = response.read()
    data = data.decode("unicode_escape")
    # print(data)
    data = pd.read_json(data)
    # print(data)
    return data
data_path='4.csv'

#——————————————————导入数据——————————————————————


reader = csv.reader(open(data_path,'r'))
rows = [row for row in reader]
title=rows[0]
trow=[]
for row in rows:
    if 'None' in row:
        trow.append(row)
for row in trow:
    rows.remove(row)
trow=[]
for row in rows:
    if '0' in row:
        trow.append(row)
for row in trow:
    rows.remove(row)
b= np.array(rows)   
b[:, [0,2]] = b[:,[2,0]]

data=b[1:-1,2:]

for i in range(data.shape[0]):
    a=data[i][0].split('-')
    b=a[0]+a[1]+a[2]
    a=int(b)
    data[i][0]=a

data= np.array(data,dtype=float)   
data=data[::-1]
trow=[]
for i in range(data.shape[0]-1):
    trow.append(data[i+1][2])
trow.append(data[data.shape[0]-1][2])
data1=np.array(trow)
data1= np.array(data1,dtype=float)
data=np.c_[data,data1]   
#f=open('1.csv')
#df=pd.read_csv(f)     #读入股票数据
#data=df.iloc[:,3:17].values  #取第3-10列
#data= data.astype(float)


def loaddata(data_name):
    load=getStockData(data_name,"1991-01-01","2018-12-31")
    a=load.columns.values.tolist()
    drawPic.data.config(state=NORMAL)
    drawPic.data.delete(1.0,END)
    drawPic.data.update()
    for i in range(len(a)):
        if i!=0:
            drawPic.data.insert(END,"\t")
        drawPic.data.insert(END,str(a[i]))
    drawPic.data.insert(END,"\n")
    rows=np.array(load)
    rows=rows.tolist()

    for i in range(len(rows)):
        for j in range(len(rows[i])):
            if j!=0:
                drawPic.data.insert(END,"\t")
            tt=float(rows[i][j])
            drawPic.data.insert(END,"%.1f" % tt)
        drawPic.data.insert(END,"\n")
    drawPic.data.focus_force()
    drawPic.data.update()    
    drawPic.data.config(state=DISABLED)    
    
    
#获取训练集
def get_train_data(batch_size=60,time_step=20,train_begin=0,train_end=train_num):
    batch_index=[]
    data_train=data[train_begin:train_end]
    normalized_train_data=(data_train-np.mean(data_train,axis=0))/np.std(data_train,axis=0)  #标准化
    train_x,train_y=[],[]   #训练集 
    for i in range(len(normalized_train_data)-time_step):
       if i % batch_size==0:
           batch_index.append(i)
       x=normalized_train_data[i:i+time_step,:input_size]
       y=normalized_train_data[i:i+time_step,input_size,np.newaxis]
       train_x.append(x.tolist())
       train_y.append(y.tolist())
    batch_index.append((len(normalized_train_data)-time_step))
    return batch_index,train_x,train_y



#获取测试集
def get_test_data(time_step=20,test_begin=train_num):
    data_test=data[test_begin:]
    mean=np.mean(data_test,axis=0)
    std=np.std(data_test,axis=0)
    normalized_test_data=(data_test-mean)/std  #标准化
    size=(len(normalized_test_data)+time_step-1)//time_step  #有size个sample 
    test_x,test_y=[],[]  
    for i in range(size-1):
       x=normalized_test_data[i*time_step:(i+1)*time_step,:input_size]
       y=normalized_test_data[i*time_step:(i+1)*time_step,input_size]
       test_x.append(x.tolist())
       test_y.extend(y)
    test_x.append((normalized_test_data[(i+1)*time_step:,:input_size]).tolist())
    test_y.extend((normalized_test_data[(i+1)*time_step:,input_size]).tolist())
    return mean,std,test_x,test_y



#——————————————————定义神经网络变量——————————————————
#输入层、输出层权重、偏置

weights={
         'in':tf.Variable(tf.random_normal([input_size,rnn_unit])),
         'out':tf.Variable(tf.random_normal([rnn_unit,1]))
        }
biases={
        'in':tf.Variable(tf.constant(0.1,shape=[rnn_unit,])),
        'out':tf.Variable(tf.constant(0.1,shape=[1,]))
       }

#——————————————————定义神经网络变量——————————————————
def lstm(X):     
    batch_size=tf.shape(X)[0]
    time_step=tf.shape(X)[1]
    w_in=weights['in']
    b_in=biases['in']  
    input=tf.reshape(X,[-1,input_size])  #需要将tensor转成2维进行计算，计算后的结果作为隐藏层的输入
    input_rnn=tf.matmul(input,w_in)+b_in
    input_rnn=tf.reshape(input_rnn,[-1,time_step,rnn_unit])  #将tensor转成3维，作为lstm cell的输入
    cell=tf.nn.rnn_cell.BasicLSTMCell(rnn_unit)
    init_state=cell.zero_state(batch_size,dtype=tf.float32)
    output_rnn,final_states=tf.nn.dynamic_rnn(cell, input_rnn,initial_state=init_state, dtype=tf.float32)  #output_rnn是记录lstm每个输出节点的结果，final_states是最后一个cell的结果
    output=tf.reshape(output_rnn,[-1,rnn_unit]) #作为输出层的输入
    w_out=weights['out']
    b_out=biases['out']
    pred=tf.matmul(output,w_out)+b_out
    return pred,final_states



#——————————————————训练模型——————————————————
def train_lstm(batch_size=80,time_step=15,train_begin=train_num,train_end=len(data),num="0",info=None):
    global key
    X=tf.placeholder(tf.float32, shape=[None,time_step,input_size])
    Y=tf.placeholder(tf.float32, shape=[None,time_step,output_size])
    batch_index,train_x,train_y=get_train_data(batch_size,time_step,train_begin,train_end)
    with tf.variable_scope("sec_lstm"+num):
        pred,_=lstm(X)
    #损失函数
    loss=tf.reduce_mean(tf.square(tf.reshape(pred,[-1])-tf.reshape(Y, [-1])))
    train_op=tf.train.AdamOptimizer(lr).minimize(loss)
    saver=tf.train.Saver(tf.global_variables(),max_to_keep=15)
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        for i in range(iterator_num):
            for step in range(len(batch_index)-1):
                if key==1:
                    _,loss_=sess.run([train_op,loss],feed_dict={X:train_x[batch_index[step]:batch_index[step+1]],Y:train_y[batch_index[step]:batch_index[step+1]]})
                else:
                    picupdate(num)
                    drawPic.updata.grid(row=5,column=8)
                    drawPic.downdata.grid(row=7,column=8)
                    drawPic.set.grid(row=7,column=2)
                    return
            te="迭代次数："+str(i)+"  误差率："+str(loss_)+"\n"
            info.config(state=NORMAL)
            info.insert(END,te)
            info.focus_force()
            info.see(END)
            info.update()
            info.config(state=DISABLED)
            if i<50 and i % 5==0:
                saver.save(sess,'model_save1\\modle.ckpt')
                picupdate(num)
            elif i<100 and i % 10==0:
                saver.save(sess,'model_save1\\modle.ckpt')
                picupdate(num)
            elif i<500 and i % 50==0:
                saver.save(sess,'model_save1\\modle.ckpt')
                picupdate(num)               
            elif i<1000 and i % 100==0:
                saver.save(sess,'model_save1\\modle.ckpt')
                picupdate(num)  
            elif i % 200==0:
                saver.save(sess,'model_save1\\modle.ckpt')
                picupdate(num) 


#train_lstm()




#————————————————预测模型————————————————————
def prediction(time_step=1,num="0"):
    X=tf.placeholder(tf.float32, shape=[None,time_step,input_size])
    #Y=tf.placeholder(tf.float32, shape=[None,time_step,output_size])
    mean,std,test_x,test_y=get_test_data(time_step)
    with tf.variable_scope("sec_lstm"+num,reuse=True):
        pred,_=lstm(X)    
    saver=tf.train.Saver(tf.global_variables())
    with tf.Session() as sess:
        #参数恢复
        module_file = tf.train.latest_checkpoint('model_save1')
        saver.restore(sess, module_file) 
        test_predict=[]
        for step in range(len(test_x)):
          prob=sess.run(pred,feed_dict={X:[test_x[step]]})   
          predict=prob.reshape((-1))
          test_predict.extend(predict)
        test_y=np.array(test_y)*std[input_size]+mean[input_size]
        test_predict=np.array(test_predict)*std[input_size]+mean[input_size]
        acc=(1-np.average(np.abs(test_predict-test_y[:len(test_predict)])/test_y[:len(test_predict)]))*100  #偏差
        mse=np.average(pow(test_predict-test_y[:len(test_predict)],2))
        
        return test_y,test_predict,mse
#prediction() 
        
    
def downloadFile(filename):
    url = base_url + "/api/download/"
    res = requests.get(url + filename)
    return res.text
def getStockCode():
    url = base_url + "/api/stock_code"
    response = request.urlopen(url)
    data = response.read()
    data = data.decode("unicode_escape")
    # print(data)
    data = pd.read_json(data)
    # print(data)
    return data
def uploadFile(filepath):
    url = base_url + "/api/upload"
    files = {"file": open(filepath, "rb")}
    response = requests.post(url, files=files)
    return response
def drawPic():
    global key
    key=1
    drawPic.resulttext.set("")
    drawPic.f.clf()
    drawPic.canvas.show()
    
    drawPic.comboxlist.config(state=DISABLED)
    drawPic.updata.config(state=DISABLED)
    drawPic.downdata.config(state=DISABLED)
    drawPic.set.config(state=DISABLED)
       
    num=random.randint(1,10000)
    drawPic.info.delete(1.0,END)
    drawPic.info.update()
    train_lstm(num=str(num),info=drawPic.info)
    y1,y2,mse=prediction(num=str(num)) 
    
    '''
    temp = {
            "title":"result", 
            "series_name":"price", 
            "x_axis_title":"",
            "x_axis_range_start":0,
            "x_axis_range_end":len(y1)+100,
            "y_axis_title":"hightest price",
            "y_axis_start":0,
            "y_axis_end":23,
            "true_data":[str(y1[i]) for i in range(len(y1))],
            "predict_data":[str(y2[i]) for i in range(len(y2))]
            }
    
    filepath = os.path.join("d:\\", "result.txt")
    print(json.dumps(temp))
    with open(filepath, "w") as f:
        f.write(json.dumps(temp))
    '''
    
    drawPic.a=drawPic.f.add_subplot(221)
    drawPic.a.plot(list(range(len(y1))),y1,color='r')
    drawPic.a.set_title("True result")
    drawPic.a=drawPic.f.add_subplot(222)
    drawPic.a.plot(list(range(len(y2))),y2,color='b')
    drawPic.a.set_title("Predict result")
    drawPic.a=drawPic.f.add_subplot(212)
    drawPic.a.plot(list(range(len(y1))),y1,color='r')
    drawPic.a.plot(list(range(len(y2))),y2,color='b')
    drawPic.canvas.show()
    drawPic.resulttext.set("MSE:%.3f." % mse)
    
    drawPic.comboxlist.config(state=NORMAL)
    drawPic.updata.config(state=NORMAL)
    drawPic.downdata.config(state=NORMAL)
    drawPic.set.config(state=NORMAL)
    
def stop():
    global key
    key=0
def test():
    global iterator_num
    iterator_num=int(iterator.get())
    global rnn_unit
    rnn_unit=int(rnn_num.get())
    global lr
    lr=float(learning.get())
    global weights,biases
    weights={
         'in':tf.Variable(tf.random_normal([input_size,rnn_unit])),
         'out':tf.Variable(tf.random_normal([rnn_unit,1]))
        }
    biases={
        'in':tf.Variable(tf.constant(0.1,shape=[rnn_unit,])),
        'out':tf.Variable(tf.constant(0.1,shape=[1,]))
       }
    
    tkinter.messagebox.askokcancel('提示','设置成功！')
def showmodel():
    drawPic.model.config(state=NORMAL)
    drawPic.model.delete(1.0,END)
    drawPic.model.update()
    res=downloadFile("pa1.py")
    contents=res
    drawPic.model.insert(END,contents)
    drawPic.model.config(state=DISABLED)
def showdata():
    drawPic.data.config(state=NORMAL)
    drawPic.data.delete(1.0,END)
    drawPic.data.update()
    for i in range(len(title)):
        if i!=0:
            drawPic.data.insert(END,"\t")
        drawPic.data.insert(END,str(title[i]))
    drawPic.data.insert(END,"\n")
    
    for i in range(len(rows)):
        if i==0:
            continue
        for j in range(len(rows[i])-6):
            if j!=0:
                drawPic.data.insert(END,"\t")
            drawPic.data.insert(END,str(rows[i][j]))
        drawPic.data.insert(END,"\n")
    drawPic.data.focus_force()
    drawPic.data.update()
    drawPic.data.config(state=DISABLED)
def picupdate(num):
    drawPic.f.clf()
    y1,y2,mse=prediction(num=str(num)) 
    drawPic.a=drawPic.f.add_subplot(221)
    drawPic.a.plot(list(range(len(y1))),y1,color='r')
    drawPic.a.set_title("True result")
    drawPic.a=drawPic.f.add_subplot(222)
    drawPic.a.plot(list(range(len(y2))),y2,color='b')
    drawPic.a.set_title("Predict result")
    drawPic.a=drawPic.f.add_subplot(212)
    drawPic.a.plot(list(range(len(y1))),y1,color='r')
    drawPic.a.plot(list(range(len(y2))),y2,color='b')
    drawPic.canvas.show()
    drawPic.resulttext.set("MSE:%.3f." % mse)
def go(*args):   #处理事件，*args表示可变参数
    drawPic.data.delete(1.0,END)
    drawPic.data.update()
    tkinter.messagebox.askokcancel('提示','数据加载中...')
    path=drawPic.comboxlist.get()
    loaddata(path)
def uploadresult():
    temp=drawPic.resulttext.get()
    if temp=='':
        tkinter.messagebox.askokcancel('提示','请先运行模型！')
    else:
        filepath = os.path.join("d:\\", "result.txt")
        with open(filepath, "w") as f:
            f.write(drawPic.resulttext.get())
            response = uploadFile("d:\\result.txt")
        tkinter.messagebox.askokcancel('提示','上传成功！')
    
def downloadresult():
    temp=drawPic.resulttext.get()
    if temp=='':
        tkinter.messagebox.askokcancel('提示','请先运行模型！')
    else:
        path=askdirectory()
        filepath = os.path.join(path, "result.txt")
        with open(filepath, "w") as f:
            f.write(drawPic.resulttext.get())
        tkinter.messagebox.askokcancel('提示','保存成功！')
    
root = tkinter.Tk() 
root.title("股票预测结果")
root.resizable(False, False)    #固定窗口大小  
windowWidth = 1560              #获得当前窗口宽  
windowHeight = 950             #获得当前窗口高 
w_box = 100  
h_box = 100
screenWidth,screenHeight = root.maxsize()     #获得屏幕宽和高  
geometryParam = '%dx%d+%d+%d'%(windowWidth, windowHeight, (screenWidth-windowWidth)/2, (screenHeight - windowHeight)/2)  
root.geometry(geometryParam)    #设置窗口大小及偏移坐标  
root.wm_attributes('-topmost',1)#窗口置顶 

Label(root,text=' ').grid(row=0,column=0)
Label(root,text='\t\t模型源码信息',font = ("Arial, 20")).grid(row=0,column=1)
Label(root,text='\t股票数据信息',font = ("Arial, 20")).grid(row=0,column=7)

Label(root,text=' ').grid(row=1,column=0)
drawPic.model=ScrolledText(root,width=95,height=20)
drawPic.model.grid(row=1,column=1,columnspan=4)
drawPic.model.config(state=DISABLED)
showmodel()
Label(root,text='').grid(row=1,column=5)
drawPic.data=ScrolledText(root,width=95,height=20)
drawPic.data.grid(row=1,column=6,columnspan=4)
drawPic.data.config(state=DISABLED)
showdata()

Label(root,text='').grid(row=2,column=0)

Label(root,text=' ').grid(row=3,column=0)
Label(root,text='\t\t参数选择',font = ("Arial, 20")).grid(row=3,column=1)
Label(root,text='股票数据',font = ("Arial, 20")).grid(row=3,column=5)
Label(root,text='\t\t     功能选择',font = ("Arial, 20")).grid(row=3,column=7)

Label(root,text='').grid(row=4,column=0)

Label(root,text=' ').grid(row=5,column=0)
iterator_value=tkinter.StringVar()#窗体自带的文本，新建一个值
iterator=ttk.Combobox(root,textvariable=iterator_value) #初始化
iterator["values"]=("50","100","200","500","1000")
iterator.current(2)  
iterator.grid(row=5,column=1)
rnn_num_value=tkinter.StringVar()#窗体自带的文本，新建一个值
rnn_num=ttk.Combobox(root,textvariable=rnn_num_value) #初始化
rnn_num["values"]=("5","8","10","15","20")
rnn_num.current(2)  
rnn_num.grid(row=5,column=2)

stock=[]
stock1=getStockCode()
stock1=np.array(stock1)
stock1=stock1.tolist()
for i in range(len(stock1)):
    stock.append(stock1[i][0][0])


comvalue=tkinter.StringVar()#窗体自带的文本，新建一个值
drawPic.comboxlist=ttk.Combobox(root,textvariable=comvalue) #初始化
drawPic.comboxlist["values"]=tuple(stock)
drawPic.comboxlist.current(0)  #选择第一个
drawPic.comboxlist.bind("<<ComboboxSelected>>",go)  #绑定事件,(下拉列表框被选中时，绑定go()函数)
drawPic.comboxlist.grid(row=5,column=5)
Button(root,text='    运行    ',command=drawPic).grid(row=5,column=7)
drawPic.updata=Button(root,text='    上传结果  ',command=uploadresult)
drawPic.updata.grid(row=5,column=8)

Label(root,text='').grid(row=6,column=0)
Label(root,text='迭代次数').grid(row=6,column=1)
Label(root,text='神经元数量').grid(row=6,column=2)

Label(root,text=' ').grid(row=7,column=0)
learning_value=tkinter.StringVar()#窗体自带的文本，新建一个值
learning=ttk.Combobox(root,textvariable=learning_value) #初始化
learning["values"]=("0.0001","0.0003","0.0006","0.001","0.01")
learning.current(2)  
learning.grid(row=7,column=1)
drawPic.set=Button(root,text='                 应用                  ',command=test)
drawPic.set.grid(row=7,column=2)
Button(root,text='    停止    ',command=stop).grid(row=7,column=7)
drawPic.downdata=Button(root,text='    下载结果    ',command=downloadresult)
drawPic.downdata.grid(row=7,column=8)

Label(root,text='').grid(row=8,column=0)
Label(root,text='学习率').grid(row=8,column=1)

drawPic.resulttext=StringVar()
Label(root,textvariable=drawPic.resulttext,font = ("Arial, 15")).grid(row=9,column=5)

Label(root,text='').grid(row=10,column=0)

Label(root,text=' ').grid(row=11,column=0)
drawPic.info=ScrolledText(root,width=38,height=30)
drawPic.info.grid(row=11,column=1)
drawPic.info.config(state=DISABLED)
drawPic.f = Figure(figsize=(11,4), dpi=100) 
drawPic.canvas = FigureCanvasTkAgg(drawPic.f, master=root)
drawPic.canvas.show()
drawPic.canvas.get_tk_widget().grid(row=11, column=2,columnspan=9)  
root.mainloop()





