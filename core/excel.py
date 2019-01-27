# -*- coding: utf-8 -*-

import hashlib
import xlrd
import pandas as pd
import sqlite3
import os


class ExcelToSQLite:

    @staticmethod
    def excel_to_sqlite():
        conn = sqlite3.connect('/opt/chinamobileportscan/db/ports.db')

        # 目前文件的MD5值，避免编码问题使用二进制的形式打开文件
        now_all_ip_md5 = hashlib.md5(open('/opt/chinamobileportscan/docs/allip.xlsx', 'rb').read()).hexdigest()
        now_record_port = hashlib.md5(open('/opt/chinamobileportscan/docs/bb.xlsx', 'rb').read()).hexdigest()
        
        # 处理所有IP列表
        with open('/opt/chinamobileportscan/docs/allip_md5.txt', 'r+') as f:
            before_all_ip_md5 = f.readline()
            if now_all_ip_md5 == before_all_ip_md5:
                f.close()
            else:
                # 更新文件MD5值
                # f.truncate()
                f.write(now_all_ip_md5)
                f.close()

                # IP重写到数据库
                df = pd.read_excel('/opt/chinamobileportscan/docs/allip.xlsx')
                sheet = df[['起始地址','当前负责三级部门','具体业务信息','负责人']]
                sheet = sheet.rename(columns={'起始地址': '公网IP地址'})
                sheet.to_sql('allips', conn, schema=None, if_exists='replace', index=False, index_label=None, chunksize=None)
                #conn.close()

                # 扫描全量公网地址重新写入到文件
                if os.path.exists('/opt/chinamobileportscan/conf/ips.txt'):
                    os.remove('/opt/chinamobileportscan/conf/ips.txt')
                    all_ip = sheet[['公网IP地址']]
                    all_ip.to_csv('/opt/chinamobileportscan/conf/ips.txt', sep='\t', index=False, header=False)
                else:
                    all_ip = sheet[['公网IP地址']]
                    all_ip.to_csv('/opt/chinamobileportscan/conf/ips.txt', sep='\t', index=False, header=False)

        # 处理已备案端口信息
        
        with open('/opt/chinamobileportscan/docs/recordport_md5.txt', 'r+') as f:
            before_record_port = f.readline()
            if now_record_port == before_record_port:
                f.close()
            else:
                # 更新文件MD5值
                # f.truncate()
                f.write(now_record_port)
                f.close()
                
                # 备案信息重写到数据库
                df = pd.read_excel('/opt/chinamobileportscan/docs/bb.xlsx')
                sheet = df[['公网IP地址', '端口']]
                sheet.to_sql('recordports', conn, schema=None, if_exists='replace', index=False, index_label=None, chunksize=None)
                # conn.close()
