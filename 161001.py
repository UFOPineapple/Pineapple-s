# -*- coding: utf-8 -*-

import re
import os

global mark     #remaining rows
mark=0

global reason   #wrong reason
reason=" "

global myUrl    #record url
myUrl=[]

global judge_line
judge_line=""

global title_mark
title_mark=0

class StateMachine:

    def __init__(self):
        self.handlers = {}
        self.startState = None
        self.endStates = []

    def add_state(self, name, handler, end_state=0):
        name = name.upper()
        self.handlers[name] = handler
        if end_state:
            self.endStates.append(name)

    def set_start(self, name):
        self.startState = name.upper()

    def run(self, cargo):
        try:
            handler = self.handlers[self.startState]
        except:
            print "must call .set_start() before .run()"
        if not self.endStates:
            print "at least one state must be an end_state"

        line_numbers=len(cargo.split("\n"))

        while True:
            (newState, cargo) = handler(cargo)
            if newState.upper() in self.endStates:
                if newState=="error_state":
                    print "该段HTML不合规"
                    print "错误行：%d"%(line_numbers-mark)
                    print "错误原因："+reason
                elif newState=="end_state":
                    print "该段HTML合规"
                    print "\n".join(myUrl)
                break
            else:
                handler = self.handlers[newState.upper()]

def start_transitions(txt):
    global mark
    global reason
    global judge_line
    splitted_txt=re.split(r"\s+",txt.split("<",1)[1],1)
    if len(splitted_txt)>1:
        word=splitted_txt[0]
    else:
        word=txt
        txt=""
    if word=="!DOCTYPE":
        txt=splitted_txt[1].strip()
        newState="doctype_state"
    else:
        mark=len(txt.strip().split("\n"))
        judge_line = txt.split("\n", 1)[0]
        if judge_line!="":
            mark-=1
        reason="<!DOCTYPE HTML >"
        newState="error_state"
    return (newState,txt)

def doctype_transitions(txt):
    global mark
    global reason
    global judge_line
    splitted_txt=txt.split(">",1)
    if len(splitted_txt)>1:
        word=splitted_txt[0]
        word=word.strip()
    else:
        word=txt
        txt=""
    if word=="HTML":
        txt=splitted_txt[1].strip()
        newState="html_sate"
    else:
        mark =len(txt.strip().split("\n"))
        judge_line = txt.split("\n", 1)[0]
        if judge_line!="":
            mark-=1
        reason="<!DOCTYPE HTML >"
        newState="error_state"
    return (newState,txt)

def html_transitions(txt):
    global mark
    global reason
    global judge_line
    splitted_txt=txt.split("<",1)[1].split(">",1)
    if len(splitted_txt)>1:
        word=splitted_txt[0]
    else:
        word=txt
        txt=""
    if word=="HTML":
        txt=splitted_txt[1].strip()
        newState="html_start_state"
    else:
        mark = len(txt.strip().split("\n"))
        judge_line = txt.split("\n", 1)[0]
        if judge_line!="":
            mark-=1
        reason="<HTML>"
        newState="error_state"
    return (newState, txt)

def html_start_transitions(txt):
    global mark
    global reason
    global judge_line
    splitted_txt=txt.split("<",1)[1].split(">",1)
    if len(splitted_txt)>1:
        word=splitted_txt[0]
    else:
        word=txt
        txt=""
    if word=="HEAD":
        txt=splitted_txt[1].strip()
        newState="head_start_state"
    else:
        mark = len(txt.strip().split("\n"))
        judge_line = txt.split("\n", 1)[0]
        if judge_line!="":
            mark-=1
        reason="<HEAD>"
        newState="error_state"
    return (newState, txt)

def head_start_transitions(txt):
    global mark
    global reason
    global judge_line
    global title_mark
    splitted_txt=txt.split("<",1)[1].split(">",1)
    if len(splitted_txt)>1:
        word=splitted_txt[0]
    else:
        word=txt
        txt=""
    if word=="TITLE":
        txt=splitted_txt[1].strip()
        title_mark=len(txt.split("\n"))-1
        newState="title_start_state"
    else:
        mark = len(txt.strip().split("\n"))
        judge_line = txt.split("\n", 1)[0]
        if judge_line!="":
            mark-=1
        reason="<TITLE>"
        newState="error_state"
    return (newState, txt)

def title_start_transitions(txt):
    global mark
    global reason
    global judge_line
    global title_mark
    splitted_txt=txt.split("<",1)
    if len(splitted_txt)>1:
        str=splitted_txt[0]
    else:
        str=txt
        txt=""
    if len(str)>0:
        txt=splitted_txt[1].strip()
        newState="title_str_state"
    else:
        mark=title_mark
        reason="<STRING>"
        newState="error_state"
    return (newState, txt)

def title_str_transitions(txt):
    global mark
    global reason
    global judge_line
    global title_mark
    splitted_txt=txt.split(">",1)
    if len(splitted_txt) > 1:
        word = splitted_txt[0]
    else:
        word = txt
        txt = ""
    if word=="/TITLE":
        txt=splitted_txt[1].strip()
        newState="title_end_state"
    else:
        mark=title_mark
        reason="</TITLE>"
        newState="error_state"
    return (newState,txt)

def title_end_transitions(txt):
    global mark
    global reason
    splitted_txt=txt.split("<",1)[1].split(">",1)
    if len(splitted_txt)>1:
        word=splitted_txt[0]
    else:
        word=txt
        txt=""
    if word=="/HEAD":
        txt=splitted_txt[1].strip()
        newState="head_end_state"
    else:
        mark = len(txt.strip().split("\n"))
        judge_line = txt.split("\n", 1)[0]
        if judge_line!="":
            mark-=1
        reason="</HEAD>"
        newState="error_state"
    return (newState,txt)

def head_end_transitions(txt):
    global mark
    global reason
    global judge_line
    splitted_txt=txt.split("<",1)[1].split(">",1)
    if len(splitted_txt)>1:
        word=splitted_txt[0]
    else:
        word=txt
        txt=""
    if word=="BODY":
        txt=splitted_txt[1].strip()
        newState="body_start_state"
    else:
        mark = len(txt.strip().split("\n"))
        judge_line = txt.split("\n", 1)[0]
        if judge_line!="":
            mark-=1
        reason="<BODY>"
        newState="error_state"
    return (newState,txt)

def body_start_transitions(txt):
    global mark
    global reason
    global judge_line
    splitted_txt=txt.split("<",1)[1].split(">",1)
    if len(splitted_txt)>1:
        word = splitted_txt[0]
    else:
        word=txt
        txt=""
    if word=="P":
        txt = splitted_txt[1].strip()
        newState="p_start_state"
    elif len(word)>5 and word.startswith("A "):
        newState = "a_start_state"
    elif word=="/BODY":
        txt = splitted_txt[1].strip()
        newState = "body_end_state"
    else:
        mark =len(txt.strip().split("\n"))
        judge_line = txt.split("\n", 1)[0]
        if judge_line!="":
            mark-=1
        reason="<A href=...> or <P> or </BODY>"
        newState="error_state"
    return (newState,txt)

def p_start_transitions(txt):
    global mark
    global reason
    global judge_line
    splitted_txt=txt.split("<",1)
    if len(splitted_txt)>1:
        str=splitted_txt[0]
    else:
        str=txt
        txt=""
    if len(str)>0:
        txt=splitted_txt[1].strip()
        newState="p_str_state"
    else:
        mark = len(txt.strip().split("\n"))
        judge_line = txt.split("\n", 1)[0]
        if judge_line!="":
            mark-=1
        reason="<STRING>"
        newState="error_state"
    return (newState, txt)

def p_str_transitions(txt):
    global mark
    global reason
    global judge_line
    splitted_txt=txt.split(">",1)
    if len(splitted_txt) > 1:
        word= splitted_txt[0]
    else:
        word = txt
        txt = ""
    if word=="/P":
        txt=splitted_txt[1].strip()
        newState="p_end_state"
    else:
        mark = len(txt.strip().split("\n"))
        judge_line = txt.split("\n", 1)[0]
        if judge_line!="":
            mark-=1
        reason="</P>"
        newState="error_state"
    return (newState,txt)

def p_end_transitions(txt):
    global mark
    global reason
    global judge_line
    splitted_txt = txt.split("<", 1)[1].split(">", 1)
    if len(splitted_txt) > 1:
        word = splitted_txt[0]
    else:
        word = txt
        txt = ""
    if word == "P":
        txt=splitted_txt[1].strip()
        newState = "p_start_state"
    elif len(word)>5 and word.startswith("A "):
        newState = "a_start_state"
    elif word == "/BODY":
        txt = splitted_txt[1].strip()
        newState = "body_end_state"
    else:
        mark = len(txt.strip().split("\n"))
        judge_line = txt.split("\n", 1)[0]
        if judge_line!="":
            mark-=1
        reason="<A href=...> or <P> or </BODY>"
        newState = "error_state"
    return (newState, txt)

def a_start_transitions(txt):
    global mark
    global reason
    global myUrl
    global judge_line
    splitted_txt=txt.split("<",1)[1].split(">",1)
    if len(splitted_txt) > 1:
        str = splitted_txt[0]
    else:
        str = txt
        txt = ""
    if str.startswith("A "):
        splitted_str=re.split(r"\s+",str.strip(),1)
        tag_a=splitted_str[0]
        myHref=splitted_str[1]
        if "=" in myHref:
            splitted_href=myHref.split("=",1)
            tag_href,url=splitted_href
            if url.startswith("\"") and url.endswith("\""):
                url = url.split("\"", 1)[1].split("\"", 1)[0]
                if tag_a=="A" and tag_href=="href" and len(url)>0:
                    myUrl.append(url)
                    txt=splitted_txt[1].strip()
                    newState="a_secend_state"
                else:
                    mark=len(txt.strip().split("\n"))
                    judge_line = txt.split("\n", 1)[0]
                    if judge_line != "":
                        mark -= 1
                    reason="<A href=...>"
                    newState="error_state"
            else:
                mark=len(txt.strip().split("\n"))
                judge_line = txt.split("\n", 1)[0]
                if judge_line != "":
                    mark -= 1
                reason = "<A href=...>"
                newState = "error_state"
        else:
            mark=len(txt.strip().split("\n"))
            judge_line = txt.split("\n", 1)[0]
            if judge_line != "":
                mark -= 1
            reason = "<A href=...>"
            newState = "error_state"
    else:
        mark=len(txt.strip().split("\n"))
        judge_line = txt.split("\n", 1)[0]
        if judge_line!="":
            mark-=1
        reason = "<A href=...>"
        newState = "error_state"
    return (newState, txt)

def a_second_transitions(txt):
    global mark
    global reason
    global judge_line
    splitted_txt=txt.split("<",1)
    if len(splitted_txt)>1:
        str=splitted_txt[0]
    else:
        str=txt
        txt=""
    if len(str)>0:
        txt = splitted_txt[1].strip()
        newState="a_str_state"
    else:
        mark = len(txt.strip().split("\n"))
        judge_line = txt.split("\n", 1)[0]
        if judge_line!="":
            mark-=1
        reason="<STRING>"
        newState="error_state"
    return (newState,txt)

def a_str_transitions(txt):
    global mark
    global reason
    global judge_line
    splitted_txt=txt.split(">",1)
    if len(splitted_txt) > 1:
        word = splitted_txt[0]
    else:
        word = txt
        txt = ""
    if word=="/A":
        txt=splitted_txt[1].strip()
        newState="a_end_state"
    else:
        mark = len(txt.strip().split("\n"))
        judge_line = txt.split("\n", 1)[0]
        if judge_line!="":
            mark-=1
        reason="</A>"
        newState="error_state"
    return (newState,txt)

def a_end_transitions(txt):
    global mark
    global reason
    global judge_line
    splitted_txt = txt.split("<", 1)[1].split(">", 1)
    if len(splitted_txt) > 1:
        word = splitted_txt[0]
    else:
        word = txt
        txt = ""
    if len(word)>5 and word.startswith("A "):
        newState="a_start_state"
    elif word=="P":
        txt=splitted_txt[1].strip()
        newState="p_start_state"
    elif word=="/BODY":
        txt=splitted_txt[1].strip()
        newState="body_end_state"
    else:
        mark = len(txt.strip().split("\n"))
        judge_line = txt.split("\n", 1)[0]
        if judge_line!="":
            mark-=1
        reason="<A href=...> or <P> or </BODY>"
        newState="error_state"
    return (newState,txt)

def body_end_transitions(txt):
    global mark
    global reason
    global judge_line
    if txt=="</HTML>":
        txt=""
        newState="end_state"
    else:
        mark = len(txt.strip().split("\n"))
        judge_line = txt.split("\n", 1)[0]
        if judge_line!="":
            mark-=1
        reason="</HTML>"
        newState="error_state"
    return (newState,txt)

m=StateMachine()

#添加各状态
m.set_start("Start")
m.add_state("Start",start_transitions)
m.add_state("doctype_state",doctype_transitions)
m.add_state("html_sate",html_transitions)
m.add_state("html_start_state",html_start_transitions)
m.add_state("head_start_state",head_start_transitions)
m.add_state("title_start_state",title_start_transitions)
m.add_state("title_str_state",title_str_transitions)
m.add_state("title_end_state",title_end_transitions)
m.add_state("head_end_state",head_end_transitions)
m.add_state("body_start_state",body_start_transitions)
m.add_state("p_start_state",p_start_transitions)
m.add_state("p_str_state",p_str_transitions)
m.add_state("p_end_state",p_end_transitions)
m.add_state("a_start_state",a_start_transitions)
m.add_state("a_secend_state",a_second_transitions)
m.add_state("a_str_state",a_str_transitions)
m.add_state("a_end_state",a_end_transitions)
m.add_state("body_end_state",body_end_transitions)
m.add_state("end_state",None,end_state=1)
m.add_state("error_state",None,end_state=1)

#获取文件夹下各文件
dir="C:\\Pineapple's\\TestFile\\"
for root,dirs,files in os.walk(dir):
    for file in files:
        f_path=os.path.join(root,file)
        f=open(f_path,"r")

        myList=[]
        myHtml=""
        myUrl=[]
        line=f.readline()

        #判断HTML是否合规
        while line!="":
            line=line.strip("\n")
            myList.append(line)
            line=f.readline()
        else:
            print f_path
            myHtml = ("\n").join(myList)
            m.run(myHtml)
            print

        f.close()
"# Pineapple-s" 
