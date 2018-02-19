# Rest Api
The rest api is used by the web app to request data and start actions. It's also used for the [decentralized architecture](https://github.com/FHellmann/My-Smart-Home/blob/master/README.md#Architecture) to communicate with other stations.

The api contains interfaces for the sensors and actuators. The rest api can be accessed through the same ip and port as the web app.

## Sensors
* http://0.0.0.0:5005/api/sensors/
    * *Method*: GET
    * *Description*: Does nothing.
    * *Return (sample)*:
    ```json
    {"success" : true}
    ```
    
* http://0.0.0.0:5005/api/sensors/rx/signals/search
    * *Method*: POST
    * *Description*: Activates the rx module to receive rf signals for at least 15 seconds. It will deactivate automatically after the time is left.
    * *Return (sample)*:
    ```json
    {"success" : true}
    ```
    
* http://0.0.0.0:5005/api/sensors/rx/signals
    * *Method*: GET
    * *Description*: Get the found signals.
    * *Return (sample)*:
    ```json
    ```

## Actuators
* http://0.0.0.0:5005/api/actuators/
    * *Method*: GET
    * *Description*: Does nothing.
    * *Return (sample)*:
    ```json
    {"success" : true}
    ```
    
* http://0.0.0.0:5005/api/actuators/tx/signal/send
    * *Method*: POST
    * *Description*: Send a signal.
    * *Return (sample)*:
    ```json
    {"success" : true}
    ```
