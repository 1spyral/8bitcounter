# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, Timer

async def wait(dut, cycles=0, duration=0, unit="ns"):
    if cycles > 0:
        await ClockCycles(dut.clk, cycles)
    if duration > 0:
        await Timer(duration, unit=unit)

@cocotb.test()
async def test_project(dut):
    dut._log.info("Start")

    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 10, unit="us")
    cocotb.start_soon(clock.start())

    # Initial values
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0

    # Reset
    dut._log.info("Test reset")
    dut.rst_n.value = 0
    await wait(dut, 0, 1, "us")
    
    dut.rst_n.value = 1

    # Enable output
    dut.ui_in.value = 0b00000010  # LOAD=0, OE=1

    # Test counting
    dut._log.info("Test counting")

    await wait(dut, 1, 1)
    assert dut.uio_out.value == 1

    await wait(dut, 1, 1)
    assert dut.uio_out.value == 2

    await wait(dut, 1, 1)
    assert dut.uio_out.value == 3

    # Test synchronous load
    dut._log.info("Test synchronous load")

    dut.uio_in.value = 100
    dut.ui_in.value = 0b00000011  # LOAD=1, OE=1

    # LOAD takes priority over OE, so bus must be in input mode
    await wait(dut, 0, 1)
    assert dut.uio_oe.value == 0

    # Nothing should change until the next clock
    await wait(dut, 0, 1, "us")
    assert dut.uio_out.value == 3

    # Now 100 should be loaded
    await wait(dut, 1, 1)
    assert dut.uio_out.value == 100

    # Disable load, leave output enabled
    dut.ui_in.value = 0b00000010  # LOAD=0, OE=1

    await wait(dut, 1, 1)
    assert dut.uio_out.value == 101

    # Test overflow
    dut._log.info("Test overflow")

    dut.uio_in.value = 255
    dut.ui_in.value = 0b00000011  # LOAD=1, OE=1

    await wait(dut, 1, 1)
    assert dut.uio_out.value == 255

    dut.ui_in.value = 0b00000010  # LOAD=0, OE=1

    await wait(dut, 1, 1)
    assert dut.uio_out.value == 0

    # Test tri-state output
    dut._log.info("Test output enable")

    dut.ui_in.value = 0b00000000  # LOAD=0, OE=0

    await wait(dut, 0, 1, "us")
    assert dut.uio_oe.value == 0

    dut.ui_in.value = 0b00000010  # LOAD=0, OE=1
    await wait(dut, 0, 1, "us")

    assert dut.uio_oe.value == 0xFF

    # Test asynchronous reset
    dut._log.info("Test asynchronous reset")

    # Re-enable output and let the counter reach a non-zero value
    dut.ui_in.value = 0b00000010  # LOAD=0, OE=1

    await wait(dut, 3)
    assert dut.uio_out.value != 0

    # Assert reset asynchronously
    dut.rst_n.value = 0

    # Wait less than one full clock cycle
    await wait(dut, 0, 1, "us")

    # Counter should already be reset without waiting for a clock edge
    assert dut.uio_out.value == 0

    # Release reset
    dut.rst_n.value = 1
