import esphome.codegen as cg
import esphome.config_validation as cv
from esphome import automation
from esphome.components import uart
from esphome.components import sensor
from esphome.const import CONF_ID, CONF_STATE, ICON_GAUGE

DEPENDENCIES = ['uart']

desky_ns = cg.esphome_ns.namespace('desky')

DeskySensor = desky_ns.class_('DeskySensor', cg.Component, sensor.Sensor, uart.UARTDevice)

CONFIG_SCHEMA = sensor.sensor_schema(icon=ICON_GAUGE).extend({
    cv.GenerateID(): cv.declare_id(DeskySensor),
}).extend(uart.UART_DEVICE_SCHEMA)

async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    await sensor.register_sensor(var, config)
    await uart.register_uart_device(var, config)

