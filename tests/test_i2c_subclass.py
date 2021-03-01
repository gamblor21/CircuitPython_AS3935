# SPDX-FileCopyrightText: Copyright (c) 2021 Martin Stephens
#
# SPDX-License-Identifier: MIT

# Many Pylnt conventions are broken for the sake of test readability
# Others fail because Pylint doesn't understand Pytest.
# Therefore skip this file.
# pylint: skip-file

import pytest
from CircuitPython_AS3935 import biffobear_as3935 as as3935


@pytest.mark.parametrize(
    "i2c, i2cbus, address, int_pin",
    [("i2c1", "i2cbus1", "address1", "int_pin1")],
)
def test_as3935_AS3935_I2C_instantiated_with_correct_args(
    mocker, i2c, i2cbus, address, int_pin
):
    assert issubclass(as3935.AS3935_I2C, as3935.AS3935)
    mock_i2cdevice = mocker.patch.object(
        as3935.i2c_dev, "I2CDevice", return_value=i2cbus
    )
    mock_as3935_init = mocker.patch.object(as3935.AS3935, "__init__", return_value=None)
    as3935.AS3935_I2C(i2c, address, interrupt_pin=int_pin)
    # Confirm that I2CDevice called with correct values
    mock_i2cdevice.assert_called_once_with(i2c, address)
    mocker.resetall()
    # Confirm I2CDevice is called with the correct default address
    test_as3935_i2c = as3935.AS3935_I2C(i2c, interrupt_pin=int_pin)
    default_i2c_address = 0x03
    mock_i2cdevice.assert_called_once_with(i2c, 0x03)
    # Confirm that the I2CDevice is assighed to self._bus
    assert test_as3935_i2c._bus == i2cbus
    # Check that AS3935 instantiated with correct args
    mock_as3935_init.assert_called_once_with(interrupt_pin=int_pin)


@pytest.mark.parametrize("addr, data_byte", [(0x04, 0xff), (0x0e, 0x44)])
def test_write_byte_out_calls_i2c_dev_write_with_correct_kwargs(mocker, addr, data_byte):
    # Confirm that the correct _write_byte_out is being called
    assert as3935.AS3935_I2C._write_byte_out.__qualname__ == "AS3935_I2C._write_byte_out"
    mock_as3935_init = mocker.patch.object(as3935.AS3935, "__init__", return_value=None)
    mock_i2cdevice = mocker.patch.object(as3935.i2c_dev, "I2CDevice", autospec=True, return_value=mocker.MagicMock())
    # mock_as3935_init = mocker.patch.object(as3935.AS3935, "__init__", return_value=None)

    test_register = as3935._Register(addr, 0x55, 0x00)
    test_as3935_i2c = as3935.AS3935_I2C("i2c", interrupt_pin="int_pin")
    test_as3935_i2c._write_byte_out(test_register, data_byte)
    test_as3935_i2c._bus.writeto.assert_called_once_with(addr, bytearray([data_byte, 0x00]), end=1)


@pytest.mark.parametrize("addr, data_byte", [(0x04, 0xff), (0x0e, 0x44)])
def test_read_byte_in_calls_i2c_dev_write_then_readinto_with_correct_args(mocker, addr, data_byte):
    # Confirm that the correct _read_byte_in is being called
    assert as3935.AS3935_I2C._read_byte_in.__qualname__ == "AS3935_I2C._read_byte_in"
    mock_as3935_init = mocker.patch.object(as3935.AS3935, "__init__", return_value=None)
    mock_i2cdevice = mocker.patch.object(as3935.i2c_dev, "I2CDevice", autospec=True, return_value=mocker.MagicMock())
    mock_i2cdevice
    test_register = as3935._Register(addr, 0x55, 0x00)
    test_as3935_i2c = as3935.AS3935_I2C("A", interrupt_pin="int_pin")
    as3935._BUFFER[0] = data_byte
    assert test_as3935_i2c._read_byte_in(test_register) == data_byte
    test_as3935_i2c._bus.write_then_readinto.assert_called_once_with(addr, as3935._BUFFER, as3935._BUFFER, out_end=1, in_end=1)
