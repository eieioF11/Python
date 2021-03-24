#!/usr/bin/env python3


import asyncio
import logging

from bleak import *


# KONASHI_ADDR = "58:8E:81:AB:1B:5D"
# KONASHI_ADDR = "58:8E:81:AB:1A:6B"
KONASHI_ADDR = "58:8E:81:AB:1A:C9"

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

def konashi_gpio_config_get_notify_hdl(sender, data):
    logging.debug("GPIO Config Get ({0}): {1}".format(sender, data))
    for i in range(8):
        func = "Disabled" if data[i*2]==0x00 else "GPIO" if data[i*2]==0x01 else "PWM" if data[i*2]==0x02 else "I2C" if data[i*2]==0x03 else "SPI" if data[i*2]==0x04 else "unknown"
        direction = "O" if (data[i*2+1]&0x10)==0x10 else "I"
        wired = "AND" if (data[i*2+1]&0x0C)==0x04 else "OR" if (data[i*2+1]&0x0C)==0x08 else "Off"
        logging.info("GPIO{}: {} ({}, PU:{}, PD:{}, Wired:{}, Ntfy:{})".format(i, func, direction, (data[i*2+1]&0x02)==0x02, (data[i*2+1]&0x01)==0x01, wired, (data[i*2+1]&0x20)==0x20))

def konashi_softpwm_config_get_notify_hdl(sender, data):
    logging.debug("SoftPWM Config Get ({0}): {1}".format(sender, data))
    for i in range(4):
        t = "Disabled" if data[i*3]==0x00 else "Duty" if data[i*3]==0x01 else "Period" if data[i*3]==0x02 else "unknown"
        c = "{}: {}{}".format("Period" if t=="Duty" else "Duty", data[i*3+1]+(data[i*3+2]<<8), "ms" if t=="Duty" else "%") if t=="Duty" or t=="Period" else ""
        logging.info("SoftPWM{}: {} ({})".format(i, t, c))

def konashi_hardpwm_config_get_notify_hdl(sender, data):
    logging.debug("HardPWM Config Get ({0}): {1}".format(sender, data))
    for i in range(4):
        logging.info("HardPWM{}: {}".format(i, "Enabled" if data[i] else "Disabled"))
    logging.info("HardPWM config: CLK:{}, PRESC:{}, Period:{}".format("20kHz" if (data[4]&0xF0)==0x10 else "38.4MHz", 2**(data[4]&0x0F), data[5]+(data[6]<<8)))

def konashi_analog_config_get_notify_hdl(sender, data):
    logging.debug("Analog Config Get ({0}): {1}".format(sender, data))
    for i in range(3):
        direction = "O" if (data[i]&0x01)==0x01 else "I"
        logging.info("AN{}: {} ({}, Ntfy:{})".format(i, "Enabled" if data[i]&0x08 else "Disabled", direction, (data[i]&0x02)==0x02))
    adc_update = "{}ms".format(100*(data[3]+1))
    adc_ref_str = {0:"Disabled", 1:"1V25", 2:"2V5", 3:"VDD"}
    adc_ref = adc_ref_str[data[4]] if data[4] in adc_ref_str else "unknown"
    vdac_ref_str = {0:"Disabled", 1:"1V25Ln", 2:"2V5Ln", 3:"1V25", 4:"2V5", 5:"Avdd"}
    vdac_ref = vdac_ref_str[data[5]] if data[5] in vdac_ref_str else "unknown"
    idac_step_str = {0:"Disabled", 1:"0.05~1.6uA", 2:"1.6~4.7uA", 3:"0.5~16uA", 4:"2~64uA"}
    idac_step = idac_step_str[data[6]] if data[6] in idac_step_str else "unknown"
    logging.info("Analog config: ADC update period:{}, ADC ref:{}, VDAC ref:{}, IDAC step:{}".format(adc_update, adc_ref, vdac_ref, idac_step))

def konashi_i2c_config_get_notify_hdl(sender, data):
    logging.debug("I2C Config Get ({0}): {1}".format(sender, data))
    logging.info("I2C config: {} ({})".format("Enabled" if data[0]&0x02 else "Disabled", "Standard 100kb/s" if (data[0]&0x01)==0x00 else "Fast 400kb/s"))

def konashi_uart_config_get_notify_hdl(sender, data):
    logging.debug("UART Config Get ({0}): {1}".format(sender, data))
    parity = "Odd" if (data[0]&0x0C)==0x08 else "Even" if (data[0]&0x0C)==0x04 else "None"
    stopbits = "2" if (data[0]&0x03)==0x03 else "1.5" if (data[0]&0x03)==0x02 else "0.5" if (data[0]&0x03)==0x00 else "1"
    logging.info("UART config: {} (Parity:{}, Stop bits:{}, Baudrate:{})".format("Enabled" if data[0]&0x80 else "Disabled", parity, stopbits, data[1]+(data[2]<<8)+(data[3]<<16)+(data[4]<<24)))

def konashi_spi_config_get_notify_hdl(sender, data):
    logging.debug("SPI Config Get ({0}): {1}".format(sender, data))
    endian = "MSB first" if (data[0]&0x08)==0x08 else "LSB first"
    logging.info("SPI config: {} (Mode:{}, Endian:{}, Baudrate:{})".format("Enabled" if data[0]&0x80 else "Disabled", data[0]&0x07, endian, data[1]+(data[2]<<8)+(data[3]<<16)+(data[4]<<24)))


def konashi_gpio_output_get_notify_hdl(sender, data):
    logging.debug("GPIO Output Get ({0}): {1}".format(sender, data))
    for i in range(8):
        if data[i]&0x10:
            logging.info("GPIO{} (out): {}".format(i, "On" if data[i]&0x01 else "Off"))

def konashi_gpio_input_notify_hdl(sender, data):
    logging.debug("GPIO Input ({0}): {1}".format(sender, data))
    for i in range(8):
        if data[i]&0x10:
            logging.info("GPIO{} (in): {}".format(i, "On" if data[i]&0x01 else "Off"))

def konashi_softpwm_output_get_notify_hdl(sender, data):
    logging.debug("SoftPWM Output Get ({0}): {1}".format(sender, data))
    for i in range(4):
        c = data[i*4]+(data[i*4+1]<<8)
        t = "{}ms".format(data[i*4+2]+(data[i*4+3]<<8))
        logging.info("SoftPWM{}: {} ({})".format(i, c, t))

def konashi_hardpwm_output_get_notify_hdl(sender, data):
    logging.debug("HardPWM Output Get ({0}): {1}".format(sender, data))
    for i in range(4):
        c = data[i*4]+(data[i*4+1]<<8)
        t = "{}ms".format(data[i*4+2]+(data[i*4+3]<<8))
        logging.info("HardPWM{}: {} ({})".format(i, c, t))

def konashi_analog_output_get_notify_hdl(sender, data):
    logging.debug("Analog Output Get ({0}): {1}".format(sender, data))
    for i in range(3):
        if data[i*5]&0x01:
            c = data[i*5+1]+(data[i*5+2]<<8)
            t = "{}ms".format(data[i*5+3]+(data[i*5+4]<<8))
            logging.info("AN{} (out): {} ({})".format(i, c, t))

def konashi_analog_input_notify_hdl(sender, data):
    logging.debug("Analog Input ({0}): {1}".format(sender, data))
    for i in range(3):
        if data[i*3]&0x01:
            c = data[i*3+1]+(data[i*3+2]<<8)
            logging.info("AN{} (in): {}".format(i, c))

def konashi_i2c_data_in_notify_hdl(sender, data):
    logging.debug("I2C Data In ({0}): {1}".format(sender, data))
    in_data = ""
    for i in range(len(data)-2):
        in_data += " {:02x}".format(data[2+i])
    logging.info("I2C addr 0x{:02x} (res: 0x{:02x}), In:{}".format(data[1], data[0], in_data))

def konashi_uart_data_in_notify_hdl(sender, data):
    logging.debug("UART Data In ({0}): {1}".format(sender, data))
    in_data = ""
    for i in range(len(data)):
        in_data += " {:02x}".format(data[i])
    logging.info("UART in:{}".format(in_data))

def konashi_uart_data_send_done_notify_hdl(sender, data):
    logging.debug("UART Data Send Done ({0}): {1}".format(sender, data))
    logging.info("UART Data Send Done: {:02x}".format(data[0]))

def konashi_spi_data_in_notify_hdl(sender, data):
    logging.debug("SPI Data In ({0}): {1}".format(sender, data))
    in_data = ""
    for i in range(len(data)):
        in_data += " {:02x}".format(data[i])
    logging.info("SPI in:{}".format(in_data))


def konashi_builtin_temperature_notify_hdl(sender, data):
    logging.debug("Builtin Temperature ({0}): {1}".format(sender, data))
    logging.info("Temperature: {}℃".format((data[0]+(data[1]<<8))/100))

def konashi_builtin_humidity_notify_hdl(sender, data):
    logging.debug("Builtin Humidity ({0}): {1}".format(sender, data))
    logging.info("Humidity: {}%".format((data[0]+(data[1]<<8))/100))

def konashi_builtin_pressure_notify_hdl(sender, data):
    logging.debug("Builtin Pressure ({0}): {1}".format(sender, data))
    logging.info("Pressure: {}hPa".format((data[0]+(data[1]<<8)+(data[2]<<16)+(data[3]<<24))/1000))

def konashi_builtin_presence_notify_hdl(sender, data):
    logging.debug("Builtin Presence ({0}): {1}".format(sender, data))
    logging.info("Presence: {}".format("Detected" if data[0]&0x01 else ("Not detected")))


async def run():
    async with BleakClient(KONASHI_ADDR) as konashi:
        x = await konashi.is_connected()
        logging.info("Connected to konashi: {0}".format(x))

        await konashi.start_notify(KONASHI_UUID_GPIO_CONFIG_GET, konashi_gpio_config_get_notify_hdl)
        await konashi.start_notify(KONASHI_UUID_SOFTPWM_CONFIG_GET, konashi_softpwm_config_get_notify_hdl)
        await konashi.start_notify(KONASHI_UUID_HARDPWM_CONFIG_GET, konashi_hardpwm_config_get_notify_hdl)
        await konashi.start_notify(KONASHI_UUID_ANALOG_CONFIG_GET, konashi_analog_config_get_notify_hdl)
        await konashi.start_notify(KONASHI_UUID_I2C_CONFIG_GET, konashi_i2c_config_get_notify_hdl)
        await konashi.start_notify(KONASHI_UUID_UART_CONFIG_GET, konashi_uart_config_get_notify_hdl)
        await konashi.start_notify(KONASHI_UUID_SPI_CONFIG_GET, konashi_spi_config_get_notify_hdl)

        await konashi.start_notify(KONASHI_UUID_GPIO_OUTPUT_GET, konashi_gpio_output_get_notify_hdl)
        await konashi.start_notify(KONASHI_UUID_GPIO_INPUT, konashi_gpio_input_notify_hdl)
        await konashi.start_notify(KONASHI_UUID_SOFTPWM_OUTPUT_GET, konashi_softpwm_output_get_notify_hdl)
        await konashi.start_notify(KONASHI_UUID_HARDPWM_OUTPUT_GET, konashi_hardpwm_output_get_notify_hdl)
        await konashi.start_notify(KONASHI_UUID_ANALOG_OUTPUT_GET, konashi_analog_output_get_notify_hdl)
        await konashi.start_notify(KONASHI_UUID_ANALOG_INPUT, konashi_analog_input_notify_hdl)
        await konashi.start_notify(KONASHI_UUID_I2C_DATA_IN, konashi_i2c_data_in_notify_hdl)
        await konashi.start_notify(KONASHI_UUID_UART_DATA_IN, konashi_uart_data_in_notify_hdl)
        await konashi.start_notify(KONASHI_UUID_UART_DATA_SEND_DONE, konashi_uart_data_send_done_notify_hdl)
        await konashi.start_notify(KONASHI_UUID_SPI_DATA_IN, konashi_spi_data_in_notify_hdl)

        await konashi.start_notify("00002a6e-0000-1000-8000-00805f9b34fb", konashi_builtin_temperature_notify_hdl)
        await konashi.start_notify("00002a6f-0000-1000-8000-00805f9b34fb", konashi_builtin_humidity_notify_hdl)
        await konashi.start_notify("00002a6d-0000-1000-8000-00805f9b34fb", konashi_builtin_pressure_notify_hdl)
        await konashi.start_notify("00002ae2-0000-1000-8000-00805f9b34fb", konashi_builtin_presence_notify_hdl)

        logging.debug("Command: GPIO config")
        await konashi.write_gatt_char(KONASHI_UUID_CONFIG_CMD, bytearray([KONASHI_CFG_CMD_GPIO, 0x01,0x10, 0x11,0x10, 0x21,0x10, 0x31,0x10, 0x41,0x10, 0x51,0x10, 0x61,0x10, 0x71,0x10]))
        logging.debug("Command: SoftPWM config")
        await konashi.write_gatt_char(KONASHI_UUID_CONFIG_CMD, bytearray([KONASHI_CFG_CMD_SOFTPWM, 0x00,0x00,0x00, 0x10,0x00,0x00, 0x20,0x00,0x00, 0x30,0x00,0x00]))
        logging.debug("Command: HardPWM config")
        await konashi.write_gatt_char(KONASHI_UUID_CONFIG_CMD, bytearray([KONASHI_CFG_CMD_HARDPWM, 0x00, 0x10, 0x20, 0x30, 0xFF,0x00,0x00,0x00]))
        logging.debug("Command: Analog config")
        await konashi.write_gatt_char(KONASHI_UUID_CONFIG_CMD, bytearray([KONASHI_CFG_CMD_ANALOG, 0x00, 0x10, 0x20, 0xF0,0xFF, 0xE0, 0xD0, 0xC0]))
        logging.debug("Command: I2C config")
        await konashi.write_gatt_char(KONASHI_UUID_CONFIG_CMD, bytearray([KONASHI_CFG_CMD_I2C, 0x00]))
        logging.debug("Command: UART config")
        await konashi.write_gatt_char(KONASHI_UUID_CONFIG_CMD, bytearray([KONASHI_CFG_CMD_UART, 0x00, 0x00,0x00,0x00,0x00]))
        logging.debug("Command: SPI config")
        await konashi.write_gatt_char(KONASHI_UUID_CONFIG_CMD, bytearray([KONASHI_CFG_CMD_SPI, 0x00, 0x00,0x00,0x00,0x00]))

        logging.debug("Command: GPIO control")
        await konashi.write_gatt_char(KONASHI_UUID_CONTROL_CMD, bytearray([KONASHI_CTL_CMD_GPIO, 0x00, 0x10, 0x20, 0x30, 0x40, 0x50, 0x60, 0x70]))
        logging.debug("Command: SoftPWM control")
        await konashi.write_gatt_char(KONASHI_UUID_CONTROL_CMD, bytearray([KONASHI_CTL_CMD_SOFTPWM, 0x00,0x00,0x00,0x00,0x00, 0x01,0x00,0x00,0x00,0x00, 0x02,0x00,0x00,0x00,0x00, 0x03,0x00,0x00]))
        logging.debug("Command: HardPWM control")
        await konashi.write_gatt_char(KONASHI_UUID_CONTROL_CMD, bytearray([KONASHI_CTL_CMD_HARDPWM, 0x00,0x00,0x00, 0x01,0x00,0x00, 0x02,0x00,0x00, 0x03,0x00,0x00]))
        logging.debug("Command: Analog control")
        await konashi.write_gatt_char(KONASHI_UUID_CONTROL_CMD, bytearray([KONASHI_CTL_CMD_ANALOG, 0x00,0x00,0x00, 0x01,0x00,0x00, 0x02,0x00,0x00]))
        logging.debug("Command: I2C control")
        await konashi.write_gatt_char(KONASHI_UUID_CONTROL_CMD, bytearray([KONASHI_CTL_CMD_I2C_DATA, 0x02, 0x08, 0x55, 0x00]))
        logging.debug("Command: UART control")
        await konashi.write_gatt_char(KONASHI_UUID_CONTROL_CMD, bytearray([KONASHI_CTL_CMD_UART_DATA, 0x00]))
        logging.debug("Command: SPI control")
        await konashi.write_gatt_char(KONASHI_UUID_CONTROL_CMD, bytearray([KONASHI_CTL_CMD_SPI_DATA, 0x00]))

        while await konashi.is_connected():
            await asyncio.sleep(1)


bl = logging.getLogger("bleak")
bl.setLevel(logging.WARNING)

logging.basicConfig(level=logging.DEBUG)

loop = asyncio.get_event_loop()
loop.run_until_complete(run())
