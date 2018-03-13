# Database

The database is realized with the no-sql
[TinyDB](http://tinydb.readthedocs.io/en/latest/index.html).

## Radio Frequency
The radio frequency data is store in an own "table" called _rf_table_.
The sub-items are arranged in a pseudo list.
Each item is numbered/indexed. The index item contains two main items.
One is the signal with the nested protocol itself and the other one is
an attribute which states if the signal was received or sent.
```json
{
  "rf_table": {
    "1": {
      "signal": {
        "protocol": {
          "one_high": 3,
          "zero_low": 3,
          "sync_low": 31,
          "sync_high": 1,
          "one_low": 1,
          "zero_high": 1,
          "pulse_length": 350
        },
        "code": 65536,
        "time": 1520976794.53731,
        "bit_length": 31,
        "pulse_length": 230
      },
      "received": true
    },
    "2": {
      "signal": {
        "protocol": {
          "one_high": 3,
          "zero_low": 3,
          "sync_low": 6,
          "sync_high": 1,
          "one_low": 1,
          "zero_high": 1,
          "pulse_length": 380
        },
        "code": 1,
        "time": 1520976801.474649,
        "bit_length": 17,
        "pulse_length": 1217
      },
      "received": true
    }
  }
}
```
