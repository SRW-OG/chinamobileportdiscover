# -*- coding: utf-8 -*-

import hashlib
import xlrd
import pandas as pd
import sqlite3
import os

def excel_to_sqlite():
    conn = sqlite3.connect('D:\\DevLab\\china_mobile_port_scan\\app\\db\\ports.db')

    # 目前文件的MD5值
    now_all_ip_md5 = hashlib.md5(open('D:\\DevLab\\china_mobile_port_scan\\app\\docs\\allip.xlsx', 'rb').read()).hexdigest()
    now_record_port_md5 = hashlib.md5(open('D:\\DevLab\\china_mobile_port_scan\\app\\docs\\bb.xlsx', 'rb').read()).hexdigest()
    


    # 处理所有IP列表
    with open('D:\\DevLab\\china_mobile_port_scan\\app\\docs\\allip_md5.txt', 'r+') as f:
        before_all_ip_md5 = f.readline()

        print('1:' + now_all_ip_md5)
        print('2:' + before_all_ip_md5)
        
        if now_all_ip_md5 == before_all_ip_md5:
            print("IP文件无变化")
            f.close()
        else:
            # 更新文件MD5值
            f.truncate()
            f.write(now_all_ip_md5)
            f.close()

            # IP重写到数据库
            df = pd.read_excel('D:\\DevLab\\china_mobile_port_scan\\app\\docs\\allip.xlsx')
            sheet = df[['起始地址','当前负责三级部门','具体业务信息','负责人']]
            sheet = sheet.rename(columns={'起始地址': '公网IP地址'})
            sheet.to_sql('allips', conn, schema=None, if_exists='replace', index=True, index_label=None, chunksize=None)
            #conn.close()

            # 扫描全量公网地址重新写入到文件
            if os.path.exists('D:\\DevLab\\china_mobile_port_scan\\app\\conf\\ips.txt'):
                os.remove('D:\\DevLab\\china_mobile_port_scan\\app\\conf\\ips.txt')
                all_ip = sheet[['公网IP地址']]
                all_ip.to_csv('D:\\DevLab\\china_mobile_port_scan\\app\\conf\\ips.txt', sep='\t', index=False, header=False)
            else:
                all_ip = sheet[['公网IP地址']]
                all_ip.to_csv('D:\\DevLab\\china_mobile_port_scan\\app\\conf\\ips.txt', sep='\t', index=False, header=False)

    # 处理已备案端口信息
    
    with open('D:\\DevLab\\china_mobile_port_scan\\app\\docs\\recordport_md5.txt', 'r+') as f:
        before_record_port_md5 = f.readline()

        print('3:' + now_record_port_md5)
        print('4:' + before_record_port_md5)

        if now_record_port_md5 == before_record_port_md5:
            print("备案文件无变化")
            f.close()
        else:
            # 更新文件MD5值
            f.truncate()
            f.write(now_record_port_md5)
            f.close()
            
            # 备案信息重写到数据库
            df = pd.read_excel('D:\\DevLab\\china_mobile_port_scan\\app\\docs\\bb.xlsx')
            sheet = df[['公网IP地址', '端口']]
            sheet.to_sql('recordports', conn, schema=None, if_exists='replace', index=True, index_label=None, chunksize=None)
            conn.close()

if __name__ == "__main__":
    excel_to_sqlite()
    print('end')