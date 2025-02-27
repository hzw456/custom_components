import esphome.codegen as cg
import esphome.config_validation as cv
from esphome import pins, automation
from esphome.components import key_provider
from esphome.const import CONF_ID, CONF_KEY, CONF_ON_TAG, CONF_TRIGGER_ID

AUTO_LOAD = [ "key_provider" ]

MULTI_CONF = True

wiegand_ns = cg.esphome_ns.namespace('wiegand')

Wiegand = wiegand_ns.class_('Wiegand', key_provider.KeyProvider, cg.Component)
WiegandTagTrigger = wiegand_ns.class_(
    "WiegandTagTrigger", automation.Trigger.template(cg.std_string)
)
WiegandKeyTrigger = wiegand_ns.class_(
    "WiegandKeyTrigger", automation.Trigger.template(cg.uint8)
)

CONF_D0 = "d0"
CONF_D1 = "d1"
CONF_ON_KEY = "on_key"

CONFIG_SCHEMA = cv.Schema(
    {
        cv.GenerateID(): cv.declare_id(Wiegand),
        cv.Required(CONF_D0): pins.internal_gpio_input_pin_schema,
        cv.Required(CONF_D1): pins.internal_gpio_input_pin_schema,
        cv.Optional(CONF_ON_TAG): automation.validate_automation(
            {
                cv.GenerateID(CONF_TRIGGER_ID): cv.declare_id(WiegandTagTrigger),
            }
        ),
        cv.Optional(CONF_ON_KEY): automation.validate_automation(
            {
                cv.GenerateID(CONF_TRIGGER_ID): cv.declare_id(WiegandKeyTrigger),
            }
        ),
    }
)


async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    pin = await cg.gpio_pin_expression(config[CONF_D0])
    cg.add(var.set_d0_pin(pin))
    pin = await cg.gpio_pin_expression(config[CONF_D1])
    cg.add(var.set_d1_pin(pin))

    for conf in config.get(CONF_ON_TAG, []):
        trigger = cg.new_Pvariable(conf[CONF_TRIGGER_ID])
        cg.add(var.register_tag_trigger(trigger))
        await automation.build_automation(trigger, [(cg.std_string, "x")], conf)

    for conf in config.get(CONF_ON_KEY, []):
        trigger = cg.new_Pvariable(conf[CONF_TRIGGER_ID])
        cg.add(var.register_key_trigger(trigger))
        await automation.build_automation(trigger, [(cg.uint8, "x")], conf)

