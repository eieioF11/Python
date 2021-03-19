Repository for Konashi Python SDK.


## Requirements

- bleak (https://github.com/hbldh/bleak):
`pip3 install bleak`


## Files

- Konashi.py:
Interface to Konashi device.

- all.py, analog_out.py, gpio.py, i2c.py, pwm.py, spi.py, uart.py:
Test scripts using bluetooth directly (not SDK).

- uart_local.py:
Script for UART communication on PC.


## Test

In Konashi.py under `if __name__ == "__main__"`, replace the name in `Konashi(name="ksD4E5F6")` with the name of the device to connect to.

