# Architecture
My Smart Home was designed to passively analyze the behavior of the inhabitants to suggest rules for automation. Thanks to the decentralized solution, each room can act independently and propose rules accordingly. As a result, the area to be learned is kept as small as possible. A trans-spatial learning behavior is not provided for the time being and probably not required. If the learning behavior in a room can adapt to the inhabitant, this behavior should be transferable to n spaces.

## System Architecture

![Architecture](https://github.com/FHellmann/My-Smart-Home/blob/master/doc/images/My-Smart-Home_Network-Architecture.png)

The server has a transceiver for the frequencies 433 MHz. The server uses these frequencies to communicate with the sensors, actuators and other servers. Because the servers communicate with other components over these frequencies, the network is independent of Wi-Fi routers in the event of a power outage. Using an internal backup power supply, the servers can continue to communicate with other off-grid components.

## Software Architecture