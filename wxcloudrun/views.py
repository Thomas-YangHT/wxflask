from datetime import datetime
from flask import render_template, request
from run import app
from wxcloudrun.dao import delete_counterbyid, query_counterbyid, insert_counter, update_counterbyid
from wxcloudrun.model import Counters
from wxcloudrun.response import make_succ_empty_response, make_succ_response, make_err_response
import json
import time
from flask import Response


@app.route('/')
def index():
    """
    :return: 返回index页面
    """
    return render_template('index.html')


@app.route('/api/msg', methods=['POST'])
def responseMsg():
    """
    :return: 文本消息
    """
    # 获取请求体参数
    params = request.get_json()

    # 检查action参数
    if 'action' in params:
        # 按照不同的action的值，进行不同的操作
        action = params['action']
        # 执行自增操作
        if action == 'CheckContainerPath':
            return make_succ_response("success")
    else:
        if request.headers.get("x-wx-source"):
            help = "请输入要查询的命令:\n===================\n如: ls ---返回用法链接\n"
            help += "001-<a href='https://mubu.com/doc/3xyI7zD_Yo'>CmdCheetSheet</a>\n"
            help += "002-<a href='https://mubu.com/doc/3y4NwBXCxo'>简述shell流程控制</a>\n"
            help += "003-<a href='https://mubu.com/doc/2-KsPtqeKo'>国内安装源总结</a>\n"
            help += "004-<a href='https://mubu.com/doc/2d8bwNidNo'>简述网络排障</a>\n"
            help += "005-<a href='https://mubu.com/doc/2wPYi23fso'>简述运维操作工具</a>\n"
            help += "006-<a href='https://mubu.com/doc/3Q14_dh4Go'>markdown文档工具</a>\n"
            help += "007-<a href='https://mubu.com/doc/3FM8gqgzro'>简述web应用性能优化</a>\n"
            help += "008-<a href='https://mubu.com/doc/3DOZgQxGwo'>简述微信公众号开发</a>\n"
            help += "009-<a href='https://mubu.com/doc/3uK_TGfrXo'>解决故障[更新中]</a>\n"
            help += "010-<a href='https://mubu.com/doc/4pNs1XBo_f9'>安全扫描</a>\n"
            help += "011-<a href='https://mubu.com/doc/3Bxi3I9DCo'>Raspberry pi4使用记录</a>\n"
            help += "012-<a href='https://mubu.com/doc/1XiLnBztCo'>K8S启动盘使用帮助</a>\n"
            # help += "\n待完成waiting:\n"
            # help += "013-<a href=''>试用pandas分析数据</a>\n"
            # help += "014-<a href=''>性能优化</a>\n"
            # help += "015-<a href=''>Python实例</a>\n"
            # help += "016-<a href=''>日志收集系统</a>\n"
            # help += "017-<a href=''>来自编个监控系统</a>\n"
            # help += "018-<a href=''>从win10到centos7</a>\n"
            help += "\nCloudMan 每天5分钟系列:\n"
            help += "<a href='https://mp.weixin.qq.com/s/7o8QxGydMTUe4Q7Tz46Diw'>[Docker教程]</a>\n"
            help += "<a href='https://mp.weixin.qq.com/s/RK6DDc8AUBklsUS7rssW2w'>[Kubernetes教程]</a>\n"
            help += "<a href='https://mp.weixin.qq.com/s/QtdMkt9giEEnvFTQzO9u7g'>[OpenStack教程]</a>\n"
            help += "\n其它:\n"
            help += "001-<a href='https://mubu.com/doc/3u65WbvQsp'>SimpleComputerWords</a>\n"
            help += "002-<a href='https://mubu.com/doc/3mtscGgyIo'>简述测试概念与工具</a>\n"
            help += "003-<a href='https://mubu.com/doc/LYdGMKtto'>IT架构图</a>\n"
            help += "004-<a href='https://mp.weixin.qq.com/mp/homepage?__biz=Mzg4MjAyMDgzMQ==&hid=1&sn=ce7139573c267c56ae45f026c4242045'>LinuxMan往期目录</a>\n"

            print(help)
            if params["MsgType"] == "text":
                keyword = params["Content"]
                if keyword == "help":
                    content = help
                else:
                    content = "参考:\n1:<a href='https://jaywcjlove.gitee.io/linux-command/c/" + \
                        keyword + ".html'>" + keyword + "</a>\n"
                    content += "2:<a href='https://www.linuxcool.com/" + \
                        keyword + "'>" + keyword + "</a>\n"
                    content += "3:<a href='https://man.linuxde.net/" + \
                        keyword + "'>" + keyword + "</a>"
                retParams = {
                    "ToUserName": params["FromUserName"],
                    "FromUserName": params["ToUserName"],
                    "CreateTime": int(time.time()),
                    "MsgType": "text",
                    "Content": content
                }
                return Response(json.dumps(retParams,ensure_ascii=False), mimetype='application/json')
            else:
                return make_succ_response(json.dumps(params))
        else:
            return make_err_response('缺少action或非法消息')


@app.route('/api/count', methods=['POST'])
def count():
    """
    :return:计数结果/清除结果
    """

    # 获取请求体参数
    params = request.get_json()

    # 检查action参数
    if 'action' not in params:
        return make_err_response('缺少action参数')

    # 按照不同的action的值，进行不同的操作
    action = params['action']

    # 执行自增操作
    if action == 'inc':
        counter = query_counterbyid(1)
        if counter is None:
            counter = Counters()
            counter.id = 1
            counter.count = 1
            counter.created_at = datetime.now()
            counter.updated_at = datetime.now()
            insert_counter(counter)
        else:
            counter.id = 1
            counter.count += 1
            counter.updated_at = datetime.now()
            update_counterbyid(counter)
        return make_succ_response(counter.count)

    # 执行清0操作
    elif action == 'clear':
        delete_counterbyid(1)
        return make_succ_empty_response()

    # action参数错误
    else:
        return make_err_response('action参数错误')


@app.route('/api/count', methods=['GET'])
def get_count():
    """
    :return: 计数的值
    """
    counter = Counters.query.filter(Counters.id == 1).first()
    return make_succ_response(0) if counter is None else make_succ_response(counter.count)
