# -*- coding: utf-8 -*-

from core.excel import *
from core.scan import *
from core.compare import *
from core.alert import *

def main():
    # 1.更新基准信息
    ExcelToSQLite.excel_to_sqlite()
    print("更新IP地址和备案信息完成")

    # 2.执行扫描任务，扫描结束后将结果保存到数据库
    print("开始扫描")
    NmapScan.nmap_scan()
    print("扫描结束")

    # 3.导入扫描结果到数据库
    NmapScan.xml_to_sqlite()
    print("完成扫描结果导入")

    # 4.比较端口变更
    Compare.compare_port()
    print("完成端口对比")

    # 5.发送告警邮件
    SendMail.send_mail()
    print("已发送告警邮件")

# if __name__ == "__main__":
#     main()
