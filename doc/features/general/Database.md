# Database

The database is realized with the no-sql
[TinyDB](http://tinydb.readthedocs.io/en/latest/index.html). To get an abstract data structure in the database, the most abstract data is used to save. This data is an event. 

## Events
The [event](https://github.com/FHellmann/My-Smart-Home/blob/master/app/database/models.py) has an event type, which is the source of the data, a data source type which says if the data belongs to a sensor or actuator, a timestamp and the data which depends on the event source.
```json
{
  "events": {
    "1": {
      "event_type": "radio_frequency",
      "data_source_type ": "sensor",
      "timestamp": 934759027,
      "data": {}
    }
}
```
