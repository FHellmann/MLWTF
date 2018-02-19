# My Smart Home
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Smart home is a very intriguing topic in terms of facilitating everyday life in your own home. This project aims to consider the use of machine learning in home automation. The Smart Home will analyze the behavior of the residents and make suggestions on how the house could take on tasks independently in the future. User feedback can be used to accept or reject such routines.

## Features
The features listed here are planned so far:

- General
    - [x] [Web App](https://github.com/FHellmann/My-Smart-Home/blob/master/doc/features/general/WEB_APP.md)
    - [x] [Rest Api](https://github.com/FHellmann/My-Smart-Home/blob/master/doc/features/general/REST_API.md)
- Sensors
    - [x] [RX-Receiver](https://github.com/FHellmann/My-Smart-Home/blob/master/doc/features/general/RF.md)
    - [ ] Thermometer
    - [ ] Motion Detector
    - [ ] Camera
        - [ ] Object Detection
        - [ ] Face Recognition
- Actuators
    - [x] [TX-Sender](https://github.com/FHellmann/My-Smart-Home/blob/master/doc/features/general/RF.md)
    - [ ] Heater
    - [ ] Blinds
    - [ ] Light

## Architecture
My Smart Home was designed to passively analyze the behavior of the inhabitants to suggest rules for automation. Thanks to the decentralized solution, each room can act independently and propose rules accordingly. As a result, the area to be learned is kept as small as possible. A trans-spatial learning behavior is not provided for the time being and probably not required. If the learning behavior in a room can adapt to the inhabitant, this behavior should be transferable to n spaces.

### System Architecture

![Architecture](https://github.com/FHellmann/My-Smart-Home/blob/master/doc/images/My-Smart-Home_Network-Architecture.png)

The server has a transceiver for the frequencies 433 MHz. The server uses these frequencies to communicate with the sensors, actuators and other servers. Because the servers communicate with other components over these frequencies, the network is independent of Wi-Fi routers in the event of a power outage. Using an internal backup power supply, the servers can continue to communicate with other off-grid components.

### Software Architecture
*In work*

## Changelog
[See changelog](https://github.com/FHellmann/My-Smart-Home/blob/master/CHANGELOG.md)

## MIT License

Copyright (c) 2018 Fabio Hellmann

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.