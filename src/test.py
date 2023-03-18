import cocotb
from cocotb.triggers import Timer
import random

@cocotb.test()
async def test_tbd(dut):
    random_int = random.randint(0, 255)
    expected_int = ~random_int & 0xff

    dut._log.info("jordan336 start")

    dut.io_in.value = random_int
    await Timer(1, units="ns")

    dut._log.info("io_in: %s", dut.io_in.value)
    dut._log.info("io_out: %s", dut.io_out.value)

    assert int(dut.io_out.value) == expected_int

