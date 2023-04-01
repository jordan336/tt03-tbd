import cocotb
from cocotb.triggers import Timer
import random

@cocotb.test()
async def test_nop(dut):
    dut._log.info("Test NOP")

    dut.io_in.value = 0
    await Timer(1, units="ns")

    dut._log.info("io_in: %s", dut.io_in.value)
    dut._log.info("io_out: %s", dut.io_out.value)

    assert int(dut.io_out.value) == 1

