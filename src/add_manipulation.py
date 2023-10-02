import socket
import ipaddress
import re

# Function returns true if IPv6 address is in the correct format.
def ipv6_val_check(ip):
    try:
        temp = ip
        socket.inet_pton(socket.AF_INET6, temp)
        return True
    except socket.error:
        return False

# Function returns true if MAC address is in the correct format.
def mac_val_check(dev_mac):
    if re.match("[0-9a-f]{2}([-])[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", dev_mac.lower()): # If the REGEX expression is matched (XX-XX-XX-XX-XX-XX) then it is valid
        return True
    return False

# Function returns the extended IPv6 address.
def extend_ip(ip):
    try:
        addr_str = ipaddress.ip_address(ip)
        new_add = addr_str.exploded # Extend address.
        return new_add
    except:
        return ""

# Function returns the compressed IPv6 address.
def compress_ip(ip):
    addr_str = ipaddress.ip_address(ip)
    new_add = addr_str.compressed # Compress address.
    return new_add

# Function returns solicited node multicast IPv6 address.
def get_sol_ip(ip):
    ex_ip = extend_ip(ip)
    sol_multi = "ff02::1:ff" + ex_ip[32:]
    return sol_multi

# Function returns the solicited node Ethernet address.
def get_sol_mac(sol_ip):
    ex_ip = extend_ip(sol_ip)
    sol_mac = "33-33-ff-" + ex_ip[32:34] + "-" + ex_ip[35:37] + "-" + ex_ip[37:]
    return sol_mac
