import time
from topology import Topology, Device
import add_manipulation as am

# Prints out the options.
def help():
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("Enter 'AR' to run example demo.")
    print("Enter 'AE' to add a new router.")
    print("Enter 'AS' to add a new end device.")
    print("Enter 'RD' to remove a device.")

    print("Enter 'AC' to add a connection between 2 devices.")
    print("Enter 'RC' to remove a connection between 2 devices.")

    print("Enter 'AI' to add an IP address to an existing router.")
    print("Enter 'RI' to remove an existing IP address from a router.")

    print("Enter 'TT' to create a default test topology with two routers, three end devices, and a switch.")
    print("Enter 'SS' to start the simulation.")

    print("Enter 'PT' to print topology.")
    print("Enter 'PD' to print all info regarding a device.")

    print("Enter 'H' to repeat options.")
    print("Enter 'E' to end program.")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("Note: All IPv6 addresses have a Subnet mask of /64")
    print("\n")
    return

# Prints out the devices and their connections in the topology.
def print_topology(my_top):
    print("\n")
    print("PRINTING TOPOLOGY")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("Device: [Direct Connections]")
    for device in my_top.top:
        print(device.name + ": ", end='')
        if len(my_top.top[device]) != 0:
            for connection in my_top.top[device][:-1]:
                print(connection.name + ", ", end='')
            print(my_top.top[device][-1].name)
        else:
            print("No Connections")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print('\n')
    return

# Prints information regarding a single device.
def print_dev(dev):
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("Name: " + dev.name)
    print("Type: " + dev.dev_type)
    print("Global IP: [", end="")
    for x in range(len(dev.extended)-1):
        print("'" + am.compress_ip(dev.extended[x]) + "', ", end="")
    print("'" + am.compress_ip(dev.extended[len(dev.extended)-1]) + "']")
    print("Solicited-Node Multicast Address: ", end="")
    print(dev.sol_ip)
    print("MAC addresse: ", end="")
    print(dev.mac_add)
    print("Ethernet destination MAC address: ", end="")
    print(dev.sol_mac_add)
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("\n")
    return

# Function asks the user to enter device for print_dev() function.
def print_dev_ask(my_top):
    dev_name = input("Enter the name of the Device to print: ")
    dev = my_top.find_device(dev_name)
    if dev is None:
        print("This device is not in the topology.")
        return
    print_dev(dev)
    return

# Function returns a valid IPv6 address.
def ip_validity(my_top):
    dev_ip = ""
    while True: # Keep asking the user for an IPv6 address until a valid one is entered.
        dev_ip = input("Enter an IPv6 Global Unicast Address: ")
        if not am.ipv6_val_check(dev_ip): # Makes sure the entered IPv6 address is valid.
            print("Invalid IPv6 address.\n")
            continue
        if my_top.ip_exist(dev_ip): # Make sure that the IP was not already assigned to a different device.
            print("IPv6 Global Unicast Address was alreay assigned.\n")
            continue
        if (dev_ip[0] != '2') and (dev_ip[0] != '3'): # Make sure that the IPv6 address starts with a 2 or a 3 (Global Unicast Address).
            print("IPv6 Global Unicast Address must start with a 2 or a 3.\n")
            continue
        break
    return dev_ip

# Function returns a valid MAC address.
def mac_validity(my_top):
    dev_mac = ""
    while True: # Loops until a valid MAC address is input.
        dev_mac = input("Enter the device's MAC address (Hyphen-Hexadecimal notation): ")
        if not am.mac_val_check(dev_mac): # Makes sure that the MAC address is given in the correct format.
            print("Input is invalid.")
            continue
        if my_top.mac_exist(dev_mac): # Makes sure that the MAC address has not been assigned.
            print("The input MAC address was already assigned.")
            continue
        break
    return dev_mac

# Function creates a new device.
def create_dev(my_top, dev_ip, dev_mac, dev_name, dev_type):
    e_ip = am.extend_ip(dev_ip) # Get the extended IPv6 address.
    sol_ip = am.get_sol_ip(e_ip) # Get the solicited node multicast address.
    sol_mac = am.get_sol_mac(sol_ip) # Get the solicited node ethernet address.
    dev = Device(dev_name, dev_type, [e_ip], [sol_ip], [dev_mac], [sol_mac]) # Create the device.

    print("-----------------------------------------------------------------------------")
    print(dev_name + ": " + dev_ip + ", " + dev_mac)
    print("IPv6 Mapping: ")
    print("IPv6 Global Unicast Address -> Solicited-Node Multicast Address -> Ethernet Multicast Address")
    print(dev_ip + " -> " + sol_ip + " -> " + sol_mac)
    return dev

# Function requests user info to create a new device.
def add_device(my_top, dev_type):
    dev_name = input("Enter the name of the device: ")
    if not my_top.name_validity(dev_name):
        print("This device already exits.")
        return
    
    if dev_type == "switch":
        dev = Device(dev_name, dev_type)
        my_top.add_device(dev)
        print("Switch was created.")
        return dev

    dev_ip = ip_validity(my_top)
    dev_mac = mac_validity(my_top)

    dev = create_dev(my_top, dev_ip, dev_mac, dev_name, dev_type)
    my_top.add_device(dev)
    return

# Function removes a device from topology.
def remove_device(my_top):
    dev_name = input("Enter the name of the device to remove: ")
    dev = my_top.find_device(dev_name)
    if dev is None: # Device does not exist.
        print("Device does not exist in the topology.")
        return
    for connection in my_top.top[dev]: # Remove connections to the device.
        my_top.top[connection].remove(dev)
    my_top.top.pop(dev) # Remove the device.
    print(dev.name + " was removed from the topology.")
    return

# Function adds an IP address to a device.
def req_ip(dev, new_ip, new_mac):
    e_ip = am.extend_ip(new_ip) # Extend the IPv6 address.
    sol_ip = am.get_sol_ip(e_ip) # Get solicited node multicast address.
    sol_mac = am.get_sol_mac(sol_ip) # Get the solicited node Etherent address.
    
    # Add the addresses to their corresponing list.
    dev.extended.append(e_ip) 
    dev.sol_ip.append(sol_ip)
    dev.mac_add.append(new_mac)
    dev.sol_mac_add.append(sol_mac)
    return sol_ip, sol_mac

# Funciton gets user input to add an IPv6 address to a router.
def add_ip(my_top):
    dev_name = input("Enter the name of the router you want to add an IP address to: ")
    dev = my_top.find_device(dev_name)
    if dev is None: # Make sure the device exists in the topology.
        print("Device does not exist in the topology.")
        return
    if dev.dev_type.lower() != "router": # Make sure the device is a router.
        print("Device input is not a router.")
        return
    new_ip = ip_validity(my_top) # Get a valid IPv6 address.
    new_mac = mac_validity(my_top) # Get a valid MAC address.

    sol_ip, sol_mac = req_ip(dev, new_ip, new_mac)
    print("IP Mapping:")
    print("IPv6 Global Unicast Address -> Solicited-Node Multicast Address -> Ethernet Multicast Address")
    print(new_ip + " -> " + sol_ip + " -> " + sol_mac)
    print_dev(dev)
    return

# Function removes an exisiting IPv6 address from a router.
def remove_ip(my_top):
    # Enter the IP and device from which the IP should be removed.
    dev_name = input("Enter the name of the router you want to remove an IP address from: ")
    dev = my_top.find_device(dev_name)
    if dev is None:
        print("Device does not exist in the topology.")
        return
    if dev.dev_type.lower() != "router":
        print("Device input is not a router.")
        return
    rm_ip = am.extend_ip(input("Enter the IP address you want to remove: "))
    if rm_ip not in dev.extended:
        print("Input IPv6 address does not belong with the input device.")
        return
    
    # Remove the addresses from their corresponding list.
    rm_ind = dev.extended.index(rm_ip)
    dev.extended.pop(rm_ind)
    dev.sol_ip.pop(rm_ind)
    dev.mac_add.pop(rm_ind)
    dev.sol_mac_add.pop(rm_ind)

    for connection in my_top.top[dev]: # Remove connections to device if it is no longer in the same IP subnet.
        if not dev.same_sub(connection):
            my_top.remove_connection(dev, connection)

    print("IPv6 address was removed.")
    print_dev(dev)
    return

# Function creates a connection between two different devices in the same subnet.
def add_connection(my_top):
    # Enter the name of the devices to connect.
    t_dev1 = input("Enter the name of the first device: ")
    dev1 = my_top.find_device(t_dev1)
    if dev1 is None:
        print("Device is not in the network.")
        return
    t_dev2 = input("Enter the name of the second device: ")
    dev2 = my_top.find_device(t_dev2)
    if dev2 is None:
        print("Device is not in the network.")
        return
    if dev1 == dev2:
        print("Cannot connect a device to itself.")
        return
    if my_top.check_connection(dev1, dev2):
        print("Connection already exists.")
        return
    
    # Make sure the devices are in the same subnet.
    if not dev1.same_sub(dev2):
        print("Devices have no IP addresses in the same subnet.")
    else:
        my_top.add_connection(dev1, dev2)
        print("Connection between " + dev1.name + " and " + dev2.name + " was created.")
    return

# Function removes an existing connection between two devices.
def remove_connection(my_top):
    t_dev1 = input("Enter the name of the first device: ")
    dev1 = my_top.find_device(t_dev1)
    if dev1 is None:
        print("Device is not in the network.")
        return
    t_dev2 = input("Enter the name of the second device: ")
    dev2 = my_top.find_device(t_dev2)
    if dev2 is None:
        print("Device is not in the network.")
        return
    if not my_top.check_connection(dev1, dev2):
        print("Connection between the devices does not exist.")
        return
    else:
        my_top.remove_connection(dev1, dev2)
        print("Connection between " + dev1.name + " and " + dev2.name + " was removed.")
    return

# Function to get user input (starting device and IPv6 address).
def start_sim(my_top):
    # Get user input regarding the device to send the NS request and the IPv6 destination.
    dev1_n = input("Enter the name of the device making the Neighbor Solicitation (NS) request: ") # Device that will send NS.
    dev1 = my_top.find_device(dev1_n)
    if dev1 is None:
        print("-> The device is not in the Topology.")
        return
    dev2_add = input("Enter the IPv6 Global Unicast address of the device reciving the NS request (making the NA): ") # Device that will respond to NS.

    ip_add = am.extend_ip(dev2_add)
    if ip_add == "":
        print("-> None of the Devices in the topology have the input IPv6 Global Unicast address.")
        return

    # Make sure the devices are in the same subnet.
    if not dev1.same_sub_ip(ip_add):
        print("-> The input address must be in the same subnet as the input device in order for the address to be resolved.")
        return

    dev2 = my_top.find_device_ip(ip_add)
    true_path = []
    true_path = request(my_top, dev1, dev2, true_path, ip_add) # Start the simulation.
    return

# Function iterate through the topology.
def request(my_top, dev1, dev2, true_path, ip_add):
    visited = []
    queue = []
    visited.append(dev1)
    queue.append([dev1])
    add_ind = dev2.ip_ind(ip_add)

    print("----------------------------NEIGHBOR SOLICITATION----------------------------")
    print(dev1.name + " is sending broadcast.")
    print("#############################################################################")
    print("Packet for " + dev2.name + ": ")
    print("[DA: Multicast][DA: Solicited-Node Multicast][ICMPv6 NS - Target IPv6 Address]")
    print("[" + dev2.sol_mac_add[add_ind] + "] [" + dev2.sol_ip[add_ind] + "] [" + am.compress_ip(dev2.extended[add_ind]) + "]")
    print("#############################################################################")
    print("\n")

    # Iterate through devices using a BFS approach.
    found = False
    while queue:
        path = queue.pop(0)
        curr_dev = path[-1] # Get the latest device in the path that was pushed.

        if curr_dev != dev1: # Device sending the NS does not process the NS packet.
            print_req(curr_dev, dev2, add_ind)
            if ((curr_dev.dev_type == "router") or (curr_dev.dev_type == "end")) and (curr_dev != dev2):
                continue
        if curr_dev == dev2: # If the current device matches the device we are looking for then make it send a NA packet following true_path.
            true_path = path.copy()
            response(my_top, true_path, add_ind)
            found = True
            continue

        for device in my_top.top[curr_dev]:
            if (device not in visited) and (device.same_sub_ip(ip_add) is True): # Makes sure that the NS is only brodcast to devices in the same subnet.
                new_path = path.copy()
                new_path.append(device) # Create a new path with the addition of the newly visited device.
                queue.append(new_path)
                visited.append(device) # Mark the current device as visited so we don't visit it again - prevents loops.
    if found == False:
        print("Address Resolution failed.")
        print("The IPv6 address trying to be resolved was in a different subnet than the device sending the NS packet.")
    print("-----------------------------------------------------------------------------")
    return true_path

# Function simulates the acceptance of NS packet.
def print_req(curr_dev, dev2, add_ind):
    print("*****************************************************************************")
    print("'" + curr_dev.name + "' recived neighbor solicitation packet.")
    if curr_dev.dev_type == "switch": # If the device is a switch then flood the packet.
        print(curr_dev.name + " (BROADCASTING): the switch is broadcasting the packet.")
    elif dev2.sol_mac_add[add_ind] in curr_dev.sol_mac_add: # If solicited node MAC address matches then pass the NS packet up.
        print("Passing Packet Up:")
        print("NIC Card->", end="")
        if dev2.sol_ip[add_ind] in curr_dev.sol_ip: # If the solicited node IPv6 multicast address matches then pass the NS packet up.
            print("IPv6 Process->", end="")
            if dev2.extended[add_ind] in curr_dev.extended: # If the IPv6 address matches the packets destinnation IPv6 address then the packet is accepted.
                print("ICMPv6 Process")
                print("\n")
                print(curr_dev.name + " (ACCEPTED): Ethernet multicast, IPv6 solicited-node multicast/global unicast match.")
                print("\n")
            else:
                print("\n")
                print(curr_dev.name + " (DROPPED): IPv6 global unicast address did NOT match.") 
        else:
            print("\n")
            print(curr_dev.name + " (DROPPED): IPv6 solicited-node multicast address did NOT match.")
    else:
        print(curr_dev.name + " (DROPPED): Ethernet multicast address did NOT match.")
    print("*****************************************************************************\n")
    return

# Function simulates NA packet response.
def response(my_top, true_path, ip_ind):
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!-NEIGHBOR ADVERTISMENT-!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    dev_to = true_path[0]
    dev_from = true_path[-1]
    print("Neighbor Advertisment is being sent from '" + dev_from.name + "' to '" + dev_to.name + "'.")
    for device in reversed(true_path[1:]): # NA packet is sent directly back to the device that sent the NS packet.
        print(device.name + "->", end='')
    print(true_path[0].name)
    print(true_path[0].name + " recived neighbor advertisment " + dev_from.name)
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    return

# Function creates a test simulation topology.
def test_top(my_top):
    # Create 2 routers, 2 end devices, and a switch.
    dev1 = create_dev(my_top, "2001:1::1", "12-21-12-12-12-12", "R1", "router")
    dev2 = create_dev(my_top, "2001:1::2", "43-43-43-43-43-43", "E1", "end")
    dev3 = Device("S1", "switch")
    dev4 = create_dev(my_top, "2001:2::21", "43-43-53-45-34-43", "R2", "router")
    dev5 = create_dev(my_top, "2001:2::3", "44-53-63-73-43-43", "E2", "end")
    dev6 = create_dev(my_top, "2001:2::6", "99-99-53-43-23-43", "E3", "end")

    my_top.add_device(dev1)
    my_top.add_device(dev2)
    my_top.add_device(dev3)
    my_top.add_device(dev4)
    my_top.add_device(dev5)
    my_top.add_device(dev6)

    req_ip(dev4, "2001:3::21", "43-54-65-67-65-12")
    req_ip(dev1, "2001:3::8", "13-14-61-61-15-12")

    # Connect R1 to R2 and E1, R2 to S1, and E2/E3 to S1.
    my_top.add_connection(dev1, dev2)
    my_top.add_connection(dev1, dev4)
    my_top.add_connection(dev4, dev3)
    my_top.add_connection(dev3, dev5)
    my_top.add_connection(dev3, dev6)

    print_topology(my_top)
    return

def main():
    n_top = Topology()
    res = "S"
    help() # Print out the options.
    while res != "E": # Exit the program with 'E'.
        print("\n")
        res = input("Enter option: ")
        res = res.upper()
        match res:
            case 'AR': # Add a router.
                add_device(n_top, "router")
            case 'AE': # Add a end device.
                add_device(n_top, "end")
            case 'AS': # Add a switch.
                add_device(n_top, "switch")
            case 'RD': # Remove a device.
                remove_device(n_top)
            case 'AC': # Add a connection.
                add_connection(n_top)
            case 'RC': # Remove a connection.
                remove_connection(n_top)
            case 'AI': # Add an IPv6 address to an existing router.
                add_ip(n_top)
            case 'RI': # Remove an IPv6 address from a router.
                remove_ip(n_top)
            case 'TT': # Create a default test topology.
                test_top(n_top)
            case 'SS': # Start the simulation.
                start_sim(n_top)
            case 'PT': # Print the devices and their connections.
                print_topology(n_top)
            case 'PD': # Print information regarding a device.
                print_dev_ask(n_top)
            case 'H': # Repeat the options.
                help()
    return

if __name__ == "__main__":
    main()
