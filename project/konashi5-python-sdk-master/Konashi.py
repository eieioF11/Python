#!/usr/bin/env python3

from __future__ import annotations

import asyncio
import logging
from ctypes import *
from typing import *

from bleak import *


KONASHI_ADV_SERVICE_UUID = "064d0100-8251-49d9-b6f3-f7ba35e5d0a1"

KONASHI_UUID_CONFIG_CMD = "064d0201-8251-49d9-b6f3-f7ba35e5d0a1"
KONASHI_CFG_CMD_GPIO = 0x01
KONASHI_CFG_CMD_SOFTPWM = 0x02
KONASHI_CFG_CMD_HARDPWM = 0x03
KONASHI_CFG_CMD_ANALOG = 0x04
KONASHI_CFG_CMD_I2C = 0x05
KONASHI_CFG_CMD_UART = 0x06
KONASHI_CFG_CMD_SPI = 0x07
KONASHI_UUID_GPIO_CONFIG_GET = "064d0202-8251-49d9-b6f3-f7ba35e5d0a1"
KONASHI_UUID_SOFTPWM_CONFIG_GET = "064d0203-8251-49d9-b6f3-f7ba35e5d0a1"
KONASHI_UUID_HARDPWM_CONFIG_GET = "064d0204-8251-49d9-b6f3-f7ba35e5d0a1"
KONASHI_UUID_ANALOG_CONFIG_GET = "064d0205-8251-49d9-b6f3-f7ba35e5d0a1"
KONASHI_UUID_I2C_CONFIG_GET = "064d0206-8251-49d9-b6f3-f7ba35e5d0a1"
KONASHI_UUID_UART_CONFIG_GET = "064d0207-8251-49d9-b6f3-f7ba35e5d0a1"
KONASHI_UUID_SPI_CONFIG_GET = "064d0208-8251-49d9-b6f3-f7ba35e5d0a1"

KONASHI_UUID_CONTROL_CMD = "064d0301-8251-49d9-b6f3-f7ba35e5d0a1"
KONASHI_CTL_CMD_GPIO= 0x01
KONASHI_CTL_CMD_SOFTPWM = 0x02
KONASHI_CTL_CMD_HARDPWM = 0x03
KONASHI_CTL_CMD_ANALOG = 0x04
KONASHI_CTL_CMD_I2C_DATA = 0x05
KONASHI_CTL_CMD_UART_DATA = 0x06
KONASHI_CTL_CMD_SPI_DATA = 0x07
KONASHI_UUID_GPIO_OUTPUT_GET = "064d0302-8251-49d9-b6f3-f7ba35e5d0a1"
KONASHI_UUID_GPIO_INPUT = "064d0303-8251-49d9-b6f3-f7ba35e5d0a1"
KONASHI_UUID_SOFTPWM_OUTPUT_GET = "064d0304-8251-49d9-b6f3-f7ba35e5d0a1"
KONASHI_UUID_HARDPWM_OUTPUT_GET = "064d0305-8251-49d9-b6f3-f7ba35e5d0a1"
KONASHI_UUID_ANALOG_OUTPUT_GET = "064d0306-8251-49d9-b6f3-f7ba35e5d0a1"
KONASHI_UUID_ANALOG_INPUT = "064d0307-8251-49d9-b6f3-f7ba35e5d0a1"
KONASHI_UUID_I2C_DATA_IN = "064d0308-8251-49d9-b6f3-f7ba35e5d0a1"
KONASHI_UUID_UART_DATA_IN = "064d0309-8251-49d9-b6f3-f7ba35e5d0a1"
KONASHI_UUID_UART_DATA_SEND_DONE = "064d030a-8251-49d9-b6f3-f7ba35e5d0a1"
KONASHI_UUID_SPI_DATA_IN = "064d030b-8251-49d9-b6f3-f7ba35e5d0a1"


KONASHI_GPIO_COUNT = 8
KONASHI_GPIO_WIRED_FCT_NOT_USED = 0
KONASHI_GPIO_WIRED_FCT_AND = 1
KONASHI_GPIO_WIRED_FCT_OR = 2
KONASHI_GPIO_DIRECTION_IN = 0
KONASHI_GPIO_DIRECTION_OUT = 1
class KonashiGpioPinConfig(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('function', c_uint8, 4),
        ('', c_uint8, 4),
        ('pull_down', c_uint8, 1),
        ('pull_up', c_uint8, 1),
        ('wired_fct', c_uint8, 2),
        ('direction', c_uint8, 1),
        ('send_on_change', c_uint8, 1),
        ('', c_uint8, 2)
    ]
    def __init__(self, direction: int=KONASHI_GPIO_DIRECTION_IN, send_on_change: bool=True, pull_down: bool=False, pull_up: bool=False, wired_fct: int=KONASHI_GPIO_WIRED_FCT_NOT_USED):
        """
        direction (int): the pin direction, one of KONASHI_GPIO_DIRECTION_IN or KONASHI_GPIO_DIRECTION_OUT
        send_on_change (bool): if true, a notification is sent on pin level change
        pull_down (bool): if true, activate the pull down resistor
        pull_up (bool): if true, activate the pull up resistor
        wired_function (int): use the pin in a wired function mode, one of KONASHI_GPIO_WIRED_FCT_NOT_USED, KONASHI_GPIO_WIRED_FCT_AND or KONASHI_GPIO_WIRED_FCT_OR
        """
        self.direction = direction
        self.send_on_change = send_on_change
        self.pull_down = pull_down
        self.pull_up = pull_up
        self.wired_fct = wired_fct
_KonashiGpioPinsConfig = KonashiGpioPinConfig*KONASHI_GPIO_COUNT

class KonashiSoftPwmPinConfig(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('control', c_uint8, 4),
        ('', c_uint8, 4),
        ('fixed_value', c_uint16)
    ]

KONASHI_HARDPWM_COUNT = 4
class KonashiHardPwmPinConfig(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('enabled', c_uint8, 1),
        ('', c_uint8, 7)
    ]
class KonashiHardPwmConfig(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('pin', KonashiHardPwmPinConfig*KONASHI_HARDPWM_COUNT),
        ('prescale', c_uint8, 4),
        ('clock', c_uint8, 4),
        ('period', c_uint16)
    ]

KONASHI_AIO_COUNT = 3
class KonashiAnalogPinConfig(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('direction', c_uint8, 1),
        ('send_on_change', c_uint8, 1),
        ('', c_uint8, 1),
        ('enabled', c_uint8, 1),
        ('', c_uint8, 4)
    ]
class KonashiAnalogConfig(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('pin', KonashiAnalogPinConfig*KONASHI_AIO_COUNT),
        ('adc_update_period', c_uint8),
        ('adc_voltage_reference', c_uint8, 4),
        ('', c_uint8, 4),
        ('vdac_voltage_reference', c_uint8, 4),
        ('', c_uint8, 4),
        ('idac_current_step', c_uint8, 4),
        ('', c_uint8, 4)
    ]

class KonashiI2cConfig(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('mode', c_uint8, 1),
        ('enabled', c_uint8, 1),
        ('', c_uint8, 6)
    ]

class KonashiUartConfig(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('stop_bits', c_uint8, 2),
        ('parity', c_uint8, 2),
        ('', c_uint8, 3),
        ('enabled', c_uint8, 1),
        ('baudrate', c_uint32)
    ]

class KonashiSpiConfig(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('mode', c_uint8, 2),
        ('', c_uint8, 1),
        ('endian', c_uint8, 1),
        ('', c_uint8, 3),
        ('enabled', c_uint8, 1),
        ('bitrate', c_uint32)
    ]


KONASHI_GPIO_LEVEL_LOW = 0
KONASHI_GPIO_LEVEL_HIGH = 1
KONASHI_GPIO_LEVEL_TOGGLE = 2
class KonashiGpioPinControl(LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('level', c_uint8, 1),
        ('', c_uint8, 3),
        ('valid', c_uint8, 1),
        ('', c_uint8, 3)
    ]
_KonashiGpioPinsControl = KonashiGpioPinControl*KONASHI_GPIO_COUNT


class NotFoundError(Exception):
    pass

class InvalidDeviceError(Exception):
    pass


class Konashi:
    def __init__(self, name: str) -> None:
        self._name = name
        self._ble_dev = None
        self._ble_client = None
        self._gpio_config = _KonashiGpioPinsConfig()
        self._gpio_output = _KonashiGpioPinsControl()
        self._gpio_input = _KonashiGpioPinsControl()
        self._gpio_input_cb = None

    def __str__(self):
        return f'Konashi {self._name} ({"Unknown" if self._ble_dev is None else self._ble_dev.address})'

    def __repr__(self):
        return f'Konashi(name="{self._name}")'

    def __eq__(self, other):
        if self._ble_dev is not None and other._ble_dev is not None:
            return self._ble_dev.address == other._ble_dev.address
        return self._name == other._name

    def __ne__(self, other):
        return not self.__eq__(other)
        

    @staticmethod
    async def find(name: str, timeout: float) -> Konashi:
        if not timeout > 0.0:
            raise ValueError("Timeout should be longer than 0 seconds")
        _konashi = None
        _invalid = False
        _scan_task = None
        _scanner = BleakScanner()
        def _scan_cb(dev: BLEDevice, adv: AdvertisementData):
            nonlocal _konashi
            nonlocal _invalid
            if dev.name == name:
                if KONASHI_ADV_SERVICE_UUID in adv.service_uuids:
                    _konashi = Konashi(name)
                    _konashi._ble_dev = dev
                else:
                    _invalid = True
                _scanner.register_detection_callback(None)
                if _scan_task:
                    _scan_task.cancel()
        _scanner.register_detection_callback(_scan_cb)
        _timedout = False
        async def _scan_coro(t: float) -> None:
            nonlocal _timedout
            try:
                await _scanner.start()
                if timeout > 0:
                    await asyncio.sleep(t)
                else:
                    while True:
                        await asyncio.sleep(100)
                _timedout = True
            except asyncio.CancelledError:
                _timedout = False
            finally:
                await _scanner.stop()
        _scan_task = asyncio.create_task(_scan_coro(timeout))
        await _scan_task
        if _timedout:
            raise NotFoundError(f'Could not find {name}')
        elif _invalid:
            raise InvalidDeviceError(f'{name} is not a Konashi device')
        else:
            return _konashi

    @staticmethod
    async def search(timeout: float) -> List[Konashi]:
        if not timeout > 0.0:
            raise ValueError("Timeout should be longer than 0 seconds")
        _konashi = []
        def _scan_cb(dev: BLEDevice, adv: AdvertisementData):
            nonlocal _konashi
            if KONASHI_ADV_SERVICE_UUID in adv.service_uuids:
                k = Konashi(dev.name)
                k._ble_dev = dev
                if k not in _konashi:
                    _konashi.append(k)
        _scanner = BleakScanner()
        _scanner.register_detection_callback(_scan_cb)
        await _scanner.start()
        await asyncio.sleep(timeout)
        _scanner.register_detection_callback(None)
        await _scanner.stop()
        return _konashi

    async def connect(self, timeout: float) -> None:
        if not timeout > 0.0:
            raise ValueError("Timeout should be longer than 0 seconds")
        if self._ble_dev is None:
            try:
                k = await self.find(self._name, timeout)
                self._ble_dev = k._ble_dev
            except NotFoundError:
                raise
            except InvalidDeviceError:
                raise
        if self._ble_client is None:
            self._ble_client = BleakClient(self._ble_dev.address)
        _con = await self._ble_client.connect(timeout=timeout)
        if _con:
            buf = await self._ble_client.read_gatt_char(KONASHI_UUID_GPIO_CONFIG_GET)
            self._gpio_config = _KonashiGpioPinsConfig.from_buffer_copy(buf)
            await self._ble_client.start_notify(KONASHI_UUID_GPIO_CONFIG_GET, self._ntf_cb_gpio_config_get)
            await self._ble_client.start_notify(KONASHI_UUID_SOFTPWM_CONFIG_GET, self._ntf_cb_softpwm_config_get)
            await self._ble_client.start_notify(KONASHI_UUID_HARDPWM_CONFIG_GET, self._ntf_cb_hardpwm_config_get)
            await self._ble_client.start_notify(KONASHI_UUID_ANALOG_CONFIG_GET, self._ntf_cb_analog_config_get)
            await self._ble_client.start_notify(KONASHI_UUID_I2C_CONFIG_GET, self._ntf_cb_i2c_config_get)
            await self._ble_client.start_notify(KONASHI_UUID_UART_CONFIG_GET, self._ntf_cb_uart_config_get)
            await self._ble_client.start_notify(KONASHI_UUID_SPI_CONFIG_GET, self._ntf_cb_spi_config_get)

            buf = await self._ble_client.read_gatt_char(KONASHI_UUID_GPIO_CONFIG_GET)
            self._gpio_output = _KonashiGpioPinsControl.from_buffer_copy(buf)
            await self._ble_client.start_notify(KONASHI_UUID_GPIO_OUTPUT_GET, self._ntf_cb_gpio_output_get)
            buf = await self._ble_client.read_gatt_char(KONASHI_UUID_GPIO_CONFIG_GET)
            self._gpio_input = _KonashiGpioPinsControl.from_buffer_copy(buf)
            await self._ble_client.start_notify(KONASHI_UUID_GPIO_INPUT, self._ntf_cb_gpio_input)
            await self._ble_client.start_notify(KONASHI_UUID_SOFTPWM_OUTPUT_GET, self._ntf_cb_softpwm_output_get)
            await self._ble_client.start_notify(KONASHI_UUID_HARDPWM_OUTPUT_GET, self._ntf_cb_hardpwm_output_get)
            await self._ble_client.start_notify(KONASHI_UUID_ANALOG_OUTPUT_GET, self._ntf_cb_analog_output_get)
            await self._ble_client.start_notify(KONASHI_UUID_ANALOG_INPUT, self._ntf_cb_analog_input)
            await self._ble_client.start_notify(KONASHI_UUID_I2C_DATA_IN, self._ntf_cb_i2c_data_in)
            await self._ble_client.start_notify(KONASHI_UUID_UART_DATA_IN, self._ntf_cb_uart_data_in)
            await self._ble_client.start_notify(KONASHI_UUID_UART_DATA_SEND_DONE, self._ntf_cb_uart_data_send_done)
            await self._ble_client.start_notify(KONASHI_UUID_SPI_DATA_IN, self._ntf_cb_spi_data_in)

    async def disconnect(self) -> None:
        if self._ble_client is not None:
            await self._ble_client.disconnect()
            self._ble_client = None


    def _ntf_cb_gpio_config_get(self, sender, data):
        self._gpio_config = _KonashiGpioPinsConfig.from_buffer_copy(data)
    def _ntf_cb_softpwm_config_get(self, sender, data):
        pass
    def _ntf_cb_hardpwm_config_get(self, sender, data):
        pass
    def _ntf_cb_analog_config_get(self, sender, data):
        pass
    def _ntf_cb_i2c_config_get(self, sender, data):
        pass
    def _ntf_cb_uart_config_get(self, sender, data):
        pass
    def _ntf_cb_spi_config_get(self, sender, data):
        pass

    def _ntf_cb_gpio_output_get(self, sender, data):
        self._gpio_output = _KonashiGpioPinsControl.from_buffer_copy(data)
    def _ntf_cb_gpio_input(self, sender, data):
        for i in range(KONASHI_GPIO_COUNT):
            if data[i]&0x10:
                val = data[i]&0x01
                if self._gpio_input[i].level != val:
                    if self._gpio_input_cb is not None:
                        self._gpio_input_cb(i, val)
        self._gpio_input = _KonashiGpioPinsControl.from_buffer_copy(data)
    def _ntf_cb_softpwm_output_get(self, sender, data):
        pass
    def _ntf_cb_hardpwm_output_get(self, sender, data):
        pass
    def _ntf_cb_analog_output_get(self, sender, data):
        pass
    def _ntf_cb_analog_input(self, sender, data):
        pass
    def _ntf_cb_i2c_data_in(self, sender, data):
        pass
    def _ntf_cb_uart_data_in(self, sender, data):
        pass
    def _ntf_cb_uart_data_send_done(self, sender, data):
        pass
    def _ntf_cb_spi_data_in(self, sender, data):
        pass


    async def gpioConfigSet(self, configs: Sequence(Tuple[int, bool, KonashiGpioPinConfig])) -> None:
        """
        Specify a list of configurations in the format (pin_bitmask, enable, config) with:
          pin_bitmask (int): a bitmask of the pins to apply this configuration to
          enable (bool): enable or disable the specified pins
          config (KonashiGpioPinConfig): the configuration for the specified pins
        """
        b = bytearray([KONASHI_CFG_CMD_GPIO])
        for config in configs:
            for i in range(KONASHI_GPIO_COUNT):
                if (config[0]&(1<<i)) > 0:
                    b.extend(bytearray([(i<<4)|(0x1 if config[1] else 0x0), bytes(config[2])[1]]))
        await self._ble_client.write_gatt_char(KONASHI_UUID_CONFIG_CMD, b)

    def gpioSetInputCallback(self, notify_callback: Callable[[int, int], None]) -> None:
        """
        The callback is called with parameters:
          pin (int)
          value (int)
        """
        self._gpio_input_cb = notify_callback

    async def gpioControl(self, controls: Sequence(Tuple[int, int])) -> None:
        """
        Specify a list of controls in the format (pin, level) with:
          pin (int): a bitmask of the pins to apply this control to
          level (int): the control for the specified pins
        """
        b = bytearray([KONASHI_CTL_CMD_GPIO])
        for control in controls:
            for i in range(KONASHI_GPIO_COUNT):
                if (control[0]&(1<<i)) > 0:
                    b.extend(bytearray([(i<<4)|(control[1])]))
        await self._ble_client.write_gatt_char(KONASHI_UUID_CONTROL_CMD, b)


if __name__ == "__main__":
    async def main():
        k = Konashi(name="ksAB1A08")
        await k.connect(5)
        print("Connected")
        await asyncio.sleep(3)
        def pin_change_cb(pin, val):
            print("Pin {}: {}".format(pin, val))
        k.gpioSetInputCallback(pin_change_cb)
        await k.gpioConfigSet([(0x01,True,KonashiGpioPinConfig(KONASHI_GPIO_DIRECTION_IN,send_on_change=True)), (0x1E,True,KonashiGpioPinConfig(KONASHI_GPIO_DIRECTION_OUT,send_on_change=False))])
        await asyncio.sleep(1)
        await k.gpioControl([(0x14,KONASHI_GPIO_LEVEL_LOW), (0x0A,KONASHI_GPIO_LEVEL_HIGH)])
        for i in range(10):
            await asyncio.sleep(1)
            await k.gpioControl([(0x1E,KONASHI_GPIO_LEVEL_TOGGLE)])
        await asyncio.sleep(2)
        await k.disconnect()
        print("Disconnected")
        await asyncio.sleep(2)

    logging.basicConfig(level=logging.INFO)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
