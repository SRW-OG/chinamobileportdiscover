# -*- coding: utf-8 -*-

import sqlite3
import pandas as pd
import datetime

class Compare:
    
    @staticmethod
    def compare_port():
        conn = sqlite3.connect('/opt/chinamobileportscan/db/ports.db')
        cur = conn.cursor()
        all_ip = pd.read_sql_query('SELECT * FROM allips', conn)

        today = datetime.date.today().strftime('%Y%m%d')
        yesterday = (datetime.date.today() - datetime.timedelta(days=1)).strftime('%Y%m%d')

        sql1 = 'SELECT "公网IP地址","端口" FROM scanports WHERE "日期"="{date}"'.format(date=today)
        sql2 = 'SELECT "公网IP地址","端口" FROM scanports WHERE "日期"="{date}"'.format(date=yesterday)

        df1 = pd.read_sql_query(sql1, conn)
        df2 = pd.read_sql_query(sql2, conn)

        # 取合集去重获得新开启或关闭的端口信息
        today_new_port = df1.append(df2).append(df2).drop_duplicates(keep=False).reset_index(drop=True)
        today_close_port = df2.append(df1).append(df1).drop_duplicates(keep=False).reset_index(drop=True)

        # print(today_new_port)
        # print(today_close_port)

        list1_temp = []
        list2_temp = []

        # 判断是否有新开启端口变更的情况
        if today_new_port.empty:  # 未发现有新开的端口
            print("未发现新开端口")
        else: # 如果有新开端口
            # 判断端口是否已备案
            for ip_port in range(len(today_new_port.index)):
                sql1_temp = 'SELECT count(*) FROM recordports WHERE "公网IP地址"="{IP}" AND "端口"="{PORT}"'.format(IP=today_new_port.iloc[ip_port][0], PORT=today_new_port.iloc[ip_port][1])

                if (cur.execute(sql1_temp) == 0):
                    # print(cur.execute(sql1_temp))
                    list1_temp.append("否")
                else:
                    # print(cur.execute(sql1_temp))
                    list1_temp.append("是")
    
            pd1_temp = pd.DataFrame(list1_temp)
            pd1_temp.columns = ['备案']

            # 横向合并新开端口表
            new_df1 = pd.concat([today_new_port ,pd1_temp], axis=1)

            new_df1["端口状态"]="开启"
            new_df1["日期"]=today
            # print(new_df1)
            # print(all_ip)

            # 合并IP部门等信息
            new_open_df = pd.merge(new_df1, all_ip, on='公网IP地址', how='left')
            # 存到数据库
            new_open_df.to_sql('alertports', conn, schema=None, if_exists='append', index=False, index_label=None, chunksize=None)
            
        # 判断是否有新关闭端口的情况
        if today_close_port.empty:
            print("未发现有新关闭端口")
        else:
            for ip_port in range(len(today_close_port.index)):
                sql2_temp = 'SELECT count(*) FROM recordports WHERE "公网IP地址"="{IP}" AND "端口"="{PORT}"'.format(IP=today_close_port.iloc[ip_port][0], PORT=today_close_port.iloc[ip_port][1])
                # print(sql2_temp)

                if (cur.execute(sql2_temp) ==0 ): # 如果从查询结果中找不到记录，则未备案
                    list2_temp.append('否')
                else:
                    list2_temp.append('是')
            
            pd2_temp = pd.DataFrame(list2_temp)
            pd2_temp.columns = ['备案']

            # 横向合并新开端口表
            new_df2 = pd.concat([today_new_port ,pd2_temp], axis=1)

            new_df2["端口状态"]="开启"
            new_df2["日期"]=today
            # print(new_df1)
            # print(all_ip)

            # 合并IP部门等信息
            new_close_df = pd.merge(new_df1, all_ip, on='公网IP地址', how='left')
            # 存到数据库
            new_close_df.to_sql('alertports', conn, schema=None, if_exists='append', index=False, index_label=None, chunksize=None)

        conn.close()
