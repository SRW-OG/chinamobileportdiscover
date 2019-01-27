# -*- coding: utf-8 -*-

import datetime
import yagmail
import sqlite3

def send_mail():
    conn = sqlite3.connect('D:\\DevLab\\china_mobile_port_scan\\app\\db\\ports.db')
    cur = conn.cursor()

    # 邮件配置
    yag = yagmail.SMTP(user='seed_hkz@163.com',password='xxxxx',host='smtp.163.com', port='465')

    date = datetime.date.today().strftime('%Y%m%d')

    # 邮件标题
    subject = '每日端口变更情况监控{DATE}'.format(DATE=date)
    # 收件人
    to = ['seed_hkz@163.com']


    # 获取当天数据库的端口变更数据，转成列表
    # sql = 'SELECT "公网IP地址","端口","服务","当前负责三级部门","具体业务信息","负责人","备案" FROM alertports WHERE "日期"={DATE}'.format(DATE=date)

    # count = cur.execute(sql)
    # results = cur.fetchall()
    # port_list = list(results)

    html_table_head = """
    <p>今日端口变更表：</p>
    <style>table,table tr th, table tr td {{border:1px solid #0094ff;}}
    table {{  min-height: 25px; line-height: 25px; text-align: center; border-collapse: collapse; padding:2px;}}</style>
    <table border="1" cellspacing="0">
        <tr>
            <th>公网IP地址</th>
            <th>端口</th>
            <th>服务</th>
            <th>当前负责三级部门</th>
            <th>具体业务信息</th>
            <th>负责人</th>
            <th>备案</th>
        </tr>
    </table>
    """

    # for port_info in port_list:
    #     html_table_body += """
    #     <tr>
    #         <th>{IP}</th>
    #         <th>{PORT}</th>
    #         <th>{SERVICE}</th>
    #         <th>{DEPARTMENT}</th>
    #         <th>{BUSINESS}</th>
    #         <th>{CHARGE}</th>
    #         <th>{REPORT}</th>
    #     </tr>
    #     """.format(IP=port_info[0], PORT=port_info[1], SERVICE=port_info[2], DEPARTMENT=port_info[3], BUSINESS=port_info[4], CHARGE=port_info[5], REPORT=port_info[6])

    mail_head = "您好，今日检测端口变更情况如下："
    mail_html = html_table_head # + html_table_body

    # 发邮件
    yag.send(to = to, subject = subject, contents = [mail_head, mail_html])

if __name__ == "__main__":
    send_mail()
    print("发送成功")