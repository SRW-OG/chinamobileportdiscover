# -*- coding: utf-8 -*-

import datetime
import yagmail
import sqlite3

class SendMail:
    
    @staticmethod
    def send_mail():
        conn = sqlite3.connect('/opt/chinamobileportscan/db/ports.db')
        cur = conn.cursor()

        # 邮件配置
        yag = yagmail.SMTP(user='xxx@163.com', password='xxxx', host='smtp.163.com', port='465')

        date = datetime.date.today().strftime('%Y%m%d')

        # 邮件标题
        subject = '每日端口变更情况监控{DATE}'.format(DATE=date)
        # 收件人
        to = ['xxx@163.com']

        mail_head = "您好，今日检测端口变更情况如下："


        # 获取当天数据库的端口变更数据，转成列表
        sql = 'SELECT "端口状态","公网IP地址","端口","服务","当前负责三级部门","具体业务信息","负责人","备案" FROM alertports WHERE "日期"="{DATE}"'.format(DATE=date)

        cur.execute(sql)
        results = cur.fetchall()
        port_list = list(results)

        # 如果端口情况没有变化，查询结果为空，直接发送端口未变更
        if port_list:
            html_table_body = ''
            for port_info in port_list:
                html_table_body +=  """<tr><th>{STATUS}</th><th>{IP}</th><th>{PORT}</th><th>{SERVICE}</th><th>{DEPARTMENT}</th><th>{BUSINESS}</th><th>{CHARGE}</th><th>{REPORT}</th></tr>""".format(STATUS=port_info[0], IP=port_info[1], PORT=port_info[2], SERVICE=port_info[3], DEPARTMENT=port_info[4], BUSINESS=port_info[5], CHARGE=port_info[6], REPORT=port_info[7])

            mail_html = """</style><table border="1" cellspacing="0"><tr><th>端口状态</th><th>公网IP地址</th><th>端口</th><th>服务</th><th>当前负责三级部门</th><th>具体业务信息</th><th>负责人</th><th>备案</th></tr>{TABLE}</table>""".format(TABLE=html_table_body)

            # 发邮件
            yag.send(to = to, subject = subject, contents = [mail_head, mail_html])

        else:
            yag.send(to = to, subject = subject, contents = [mail_head, '同昨天相比，未发现新开启或关闭端口。'])
