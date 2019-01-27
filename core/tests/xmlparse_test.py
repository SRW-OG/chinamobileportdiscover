import xml.etree.cElementTree as ET
import time

# xml_file = time.strftime("%Y%m%d", time.localtime(time.time()))+'_scan_result.xml'
tree = ET.parse('test.xml')
root = tree.getroot()
hosts = root.findall('host')
host_data = []

for host in hosts:
    addr_info = []
    date = time.strftime("%Y-%m-%d", time.localtime(time.time()))

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
    try:
        os_element = host.findall('os')
        os_name = os_element[0].findall('osmatch')[0].attrib['name']
    except IndexError:
        os_name = ''
    
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
            try:
                product = port.findall('service')[0].attrib['product']
            except (IndexError, KeyError):
                product = ''      
            try:
                servicefp = port.findall('service')[0].attrib['servicefp']
            except (IndexError, KeyError):
                servicefp = ''
            try:
                script_id = port.findall('script')[0].attrib['id']
            except (IndexError, KeyError):
                script_id = ''
            try:
                script_output = port.findall('script')[0].attrib['output']
            except (IndexError, KeyError):
                script_output = ''

            # Create a list of the port data
            # port_data.extend((ip_address, host_name, os_name, proto, port_id, service, product, servicefp, script_id, script_output))
            port_data.extend((date, ip_address, proto, port_id, service))
            
            # Add the port data to the host data
            host_data.append(port_data)

    # If no port information, just create a list of host information
    except IndexError:
        addr_info.extend((ip_address, host_name))
        host_data.append(addr_info)

print(host_data)