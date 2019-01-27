# -*- coding: utf-8 -*-

import subprocess
import datetime
import pandas as pd
import xml.etree.cElementTree as ET
import sqlite3

class NmapScan:

    @staticmethod
    def nmap_scan():
        ip_file = '/opt/chinamobileportscan/conf/ips.txt'
        with open('/opt/chinamobileportscan/conf/ports.txt', 'r') as f:
            scan_ports = f.readline()
            f.close
        
        date = datetime.date.today().strftime('%Y%m%d')
        scan_result = '/opt/chinamobileportscan/output/'+date+'_scan_result.xml'

        # 扫描参数
        scan_args = 'nmap -p {ports} -iL {ip_file} --open -n -oX {save_file} -vv'.format(ports=scan_ports, ip_file=ip_file, save_file=scan_result)

        # 等待扫描结束
        subprocess.call(scan_args, stdin=None, stdout=None, stderr=None, shell=True)


    # 读取xml的扫描文件，将端口信息写入到数据库
    @staticmethod
    def xml_to_sqlite():
        xml_file = '/opt/chinamobileportscan/output/'+datetime.date.today().strftime('%Y%m%d')+'_scan_result.xml'
        tree = ET.parse(xml_file)
        root = tree.getroot()
        hosts = root.findall('host')
        host_data = []

        for host in hosts:
            addr_info = []
            date = datetime.date.today().strftime('%Y%m%d')

            # Ignore hosts that are not 'up'
            if not host.findall('status')[0].attrib['state'] == 'up':
                continue
            
            # Get IP address and host info. If no hostname, then ''
            ip_address = host.findall('address')[0].attrib['addr']
            host_name_element = host.findall('hostnames')
            try:
                host_name = host_name_element[0].findall('hostname')[0].attrib['name']
            except IndexError:
                host_name = ''

            try:
                port_element = host.findall('ports')
                ports = port_element[0].findall('port')
                for port in ports:
                    port_data = []
                    
                    # Ignore ports that are not 'open'
                    if not port.findall('state')[0].attrib['state'] == 'open':
                        continue
                    
                    proto = port.attrib['protocol']
                    port_id = port.attrib['portid']
                    service = port.findall('service')[0].attrib['name']
                    port_data.extend((date, ip_address, proto, port_id, service))
                    
                    # Add the port data to the host data
                    host_data.append(port_data)

            # If no port information, just create a list of host information
            except IndexError:
                addr_info.extend((ip_address, host_name))
                host_data.append(addr_info)
        

            conn = sqlite3.connect('/opt/chinamobileportscan/db/ports.db')
            df = pd.DataFrame(host_data)
            df.columns = ['日期','公网IP地址', '协议', '端口', '服务']
            df.to_sql('scanports', conn, schema=None, if_exists='append', index=False, index_label=None, chunksize=None)
            conn.close()
