# -*- coding: utf-8 -*-

import subprocess
import datetime
import pandas as pd
import xml.etree.cElementTree as ET
import sqlite3

def nmap_scan():
    ip_file = 'D:\\DevLab\\china_mobile_port_scan\\app\\conf\\ips.txt'
    with open('D:\\DevLab\\china_mobile_port_scan\\app\\conf\\ports.txt', 'r') as f:
        scan_ports = f.readline()
        f.close
    
    date = datetime.date.today().strftime('%Y%m%d')
    scan_result = 'D:\\DevLab\\china_mobile_port_scan\\app\\output\\'+date+'_scan_result.xml'

    # 扫描参数
    scan_args = 'nmap -p {ports} -iL {ip_file} --open -sV -oX {save_file}'.format(ports=scan_ports, ip_file=ip_file, save_file=scan_result)

    #subprocess.Popen(scan_args, bufsize=-1, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    subprocess.call(scan_args, stdin=None, stdout=None, stderr=None, shell=False)


# 读取xml的扫描文件，将端口信息写入到数据库

def read_XML():
    xml_file = 'D:\\DevLab\\china_mobile_port_scan\\app\\output\\'+datetime.date.today().strftime('%Y%m%d')+'_scan_result.xml'
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
        
        # If we only want the IP addresses from the scan, stop here
        # if args.ip_addresses:
        #     addr_info.extend((ip_address, host_name))
        #     host_data.append(addr_info)
        #     continue
        
        # Get the OS information if available, else ''
        # try:
        #     os_element = host.findall('os')
        #     # os_name = os_element[0].findall('osmatch')[0].attrib['name']
        # except IndexError:
        #     os_name = ''
        
        # Get information on ports and services
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
                # try:
                #     product = port.findall('service')[0].attrib['product']
                # except (IndexError, KeyError):
                #     product = ''      
                # try:
                #     servicefp = port.findall('service')[0].attrib['servicefp']
                # except (IndexError, KeyError):
                #     servicefp = ''
                # try:
                #     script_id = port.findall('script')[0].attrib['id']
                # except (IndexError, KeyError):
                #     script_id = ''
                # try:
                #     script_output = port.findall('script')[0].attrib['output']
                # except (IndexError, KeyError):
                #     script_output = ''

                # Create a list of the port data
                # port_data.extend((ip_address, host_name, os_name, proto, port_id, service, product, servicefp, script_id, script_output))
                port_data.extend((date, ip_address, proto, port_id, service))
                
                # Add the port data to the host data
                host_data.append(port_data)

        # If no port information, just create a list of host information
        except IndexError:
            addr_info.extend((ip_address, host_name))
            host_data.append(addr_info)
    

        conn = sqlite3.connect('D:\\DevLab\\china_mobile_port_scan\\app\\db\\ports.db')
        df = pd.DataFrame(host_data)
        df.columns = ['日期','公网IP地址', '协议', '端口', '服务']
        df.to_sql('scanports', conn, schema=None, if_exists='append', index=True, index_label=None, chunksize=None)
        conn.close()

if __name__ == "__main__":
    nmap_scan()
    print('执行完扫描')
    read_XML()