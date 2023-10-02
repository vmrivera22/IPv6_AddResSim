# IPv6_AddResSim
IPv6 Address Resolution Simulation

Overview:
    This program is terminal-based simulation of IPv6 address resolution using user built or a prebuilt topology.

Functionality:
    NOTE: All IPv6 addresses have a subnet mask of /64 (in this program).

    This program allows the user to create their own topology using routers, switches, and end-devices. Connections between devices can be added if the devices have interfaces in the same subnet and can be removed if the connection already exists. Additional IPv6 addresses can be added (or removed) to routers allowing routers to be in multiple different subnets. Switches, on the other hand, do not have IPv6 addresses (in this simulation) and thus can form a connection with any device.

    The Address resolution simulation must be done between two devices in the same subnet. Both broadcast Neighbor Solicitation packets and direct Neighbor Advertisment packets are simulated.

    Information regarding a device can be printed as well as the topology to view the devices connections. Additionally all options available can be repeated by inputing the 'H' option.

    OPTIONS:
    'AR': Add a new router
    'AR': Add a new end device
    'AS': Add a new switch
    'RD': Remove a device
    'AC': Add a connection
    'RC': Remove a connection
    'AI': Add a new IPv6 address to an existing device
    'RI': Remove an IPv6 address from an existing device
    'TT': Create the pre-built test topology
    'SS': Start the Simulation
    'PT': Print the Topology
    'PD': Print all info regarding a device
    'H': Repeat options
    'E': End the program

Pre-Built Topology:
    The prebuilt topology consists of 6 devices: 2 routers (R1, R2, R3), 3 end devices (E1, E2), and a switch (S1).
    The topology is connected as follows:
        device: [connections]
        R2: [R1, S1]
        R1: [R2, E1]
        E1: [R1]
        S1: [R2, E2, E3]
        E2: [S1]
        E3: [S1]