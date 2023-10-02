from collections import defaultdict
from add_manipulation import extend_ip

# Device class.
class Device:
    def __init__(self, name="", d_type="", e_ip=[], s_ip=[], mac=[], sol_mac=[]):
        self.name = name # Name of the device.
        self.dev_type = d_type # Device type.

        self.extended = e_ip # List of extended IPv6 addesses belonging to the Device.
        self.sol_ip = s_ip # List of extended Solicited Node Multicast IPv6 addresses belonging to the Device.

        self.mac_add = mac # List of MAC addresses belonging to the device.
        self.sol_mac_add = sol_mac # List of Ethernet Multicast Addresses belonging to the device.

    def __str__(self):
        return self.name

    def __eq__(self, other): # Used to define what it means for devices to be equal.
        return hasattr(other, "name") and self.name == other.name

    def __hash__(self): # Makes it so that a device can be used as a key in a dictionary.
        return hash(self.name)

    # Method returns True if the devices have an interface in the same subnet.
    def same_sub(self, other):
        if(self.dev_type.lower() == "switch") or (other.dev_type.lower() == "switch"):
            return True
        for ip in self.extended:
            net = ip[:20]
            for sec_ip in other.extended: # Compare net to the IPv6 addresses of the input device.
                if net in sec_ip:
                    return True
        return False
    
    # Method returns True if the device has an interface in the same subnet as the entered IPv6 address.
    def same_sub_ip(self, ip):
        if self.dev_type.lower() == "switch": # Switch does not have IP address in this program so return True.
            return True
        net = ip[:20] 
        for sec_ip in self.extended: # Compare net to the IPv6 addresses of the input device.
            if net in sec_ip:
                return True
        return False

    # Method returns the index of the IPv6 address in its list of IPv6 addresses.
    def ip_ind(self, ip_add):
        for index, ip in enumerate(self.extended):
            if ip == ip_add:
                return index            
        return None

class Topology:
    def __init__(self):
        self.top = defaultdict(list)

    # Method adds a device to the topology.
    def add_device(self, dev1):
        self.top[dev1] = []

    # Method creates a connection between two devices.
    def add_connection(self, dev1, dev2):
        self.top[dev1].append(dev2)
        self.top[dev2].append(dev1)

    # Method removes a connection between two devices.
    def remove_connection(self, dev1, dev2):
        self.top[dev1].remove(dev2)
        self.top[dev2].remove(dev1)
    
    # Method returns a device in the topology corresponding to the given name of the device.
    def find_device(self, dev_name):
        for dev in self.top:
            if dev_name == dev.name:
                return dev
        return None

    # Method returns a device in the topology corresponding to a given the IPv6 address of the device.
    def find_device_ip(self, ip):
        for dev in self.top:
            if ip in dev.extended:
                return dev
        return None
    
    # Method returns True if a device has the input IPv6 address.
    def ip_exist(self, dev_ip):
        ext_ip = extend_ip(dev_ip)
        for key in self.top:
            if ext_ip in key.extended:
                return True
        return False
    
    # Method returns True if a device has the input MAC address.
    def mac_exist(self, dev_mac):
        for key in self.top:
            if (dev_mac in key.mac_add) or (dev_mac in key.sol_mac_add):
                return True
        return False

    # Method returns True if a conenction between the two devices exists.
    def check_connection(self, dev1, dev2):
        if (dev1 in self.top[dev2]) or (dev2 in self.top[dev1]):
            return True
        return False
    
    # Method returns True if the name entered belongs to a device in the Topology.
    def name_validity(self, dev_name):
        dev = self.find_device(dev_name)
        if dev is None:
            return True
        return False
        