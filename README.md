# My Smart Home
Smart home is a very intriguing topic in terms of facilitating everyday life in your own home. This project aims to consider the use of machine learning in home automation. The Smart Home will analyze the behavior of the residents and make suggestions on how the house could take on tasks independently in the future. User feedback can be used to accept or reject such routines.

## Features
The features listed here are planned so far:

- [ ] Sensors
    - [ ] Thermometer
    - [ ] Motion Detector
    - [ ] Camera (Object Detection & Face Recognition)
- [ ] Actuators
    - [ ] Heater
    - [ ] Blinds
    - [ ] Light

## Architecture
My Smart Home was designed to passively analyze the behavior of the inhabitants to suggest rules for automation. Thanks to the decentralized solution, each room can act independently and propose rules accordingly. As a result, the area to be learned is kept as small as possible. A trans-spatial learning behavior is not provided for the time being and probably not required. If the learning behavior in a room can adapt to the inhabitant, this behavior should be transferable to n spaces.

![Architecture](https://github.com/FHellmann/My-Smart-Home/blob/master/doc/images/My-Smart-Home_Network-Architecture.png)

The server has a transceiver for the frequencies 433 and 868 MHz. The server uses these frequencies to communicate with the sensors, actuators and other servers. Because the servers communicate with other components over these frequencies, the network is independent of Wi-Fi routers in the event of a power outage. Using an internal backup power supply, the servers can continue to communicate with other off-grid components.
