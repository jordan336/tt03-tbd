import cocotb
from cocotb.triggers import Timer
from cocotb.clock import Clock
import random

CLK_FREQ_HZ = 10000
CLK_PERIOD_SEC = (1 / CLK_FREQ_HZ)
CLK_PERIOD_US = CLK_PERIOD_SEC * 1000000

@cocotb.test()
async def test_nop(dut):
    cocotb.start_soon(Clock(dut.clk, CLK_PERIOD_US, "us").start())
    dut.instr.value = 0
    await Timer(CLK_PERIOD_US, units="us")
    assert int(dut.io_out.value) == 1

@cocotb.test()
async def test_add(dut):
    cocotb.start_soon(Clock(dut.clk, CLK_PERIOD_US, "us").start())
    dut.instr.value = 0x08
    await Timer(CLK_PERIOD_US, units="us")
    assert int(dut.io_out.value) == 2

@cocotb.test()
async def test_addi(dut):
    cocotb.start_soon(Clock(dut.clk, CLK_PERIOD_US, "us").start())
    dut.instr.value = 0x10
    await Timer(CLK_PERIOD_US, units="us")
    assert int(dut.io_out.value) == 4

@cocotb.test()
async def test_and(dut):
    cocotb.start_soon(Clock(dut.clk, CLK_PERIOD_US, "us").start())
    dut.instr.value = 0x18
    await Timer(CLK_PERIOD_US, units="us")
    assert int(dut.io_out.value) == 8

@cocotb.test()
async def test_andi(dut):
    cocotb.start_soon(Clock(dut.clk, CLK_PERIOD_US, "us").start())
    dut.instr.value = 0x20
    await Timer(CLK_PERIOD_US, units="us")
    assert int(dut.io_out.value) == 16

@cocotb.test()
async def test_or(dut):
    cocotb.start_soon(Clock(dut.clk, CLK_PERIOD_US, "us").start())
    dut.instr.value = 0x28
    await Timer(CLK_PERIOD_US, units="us")
    assert int(dut.io_out.value) == 32

@cocotb.test()
async def test_ori(dut):
    cocotb.start_soon(Clock(dut.clk, CLK_PERIOD_US, "us").start())
    dut.instr.value = 0x30
    await Timer(CLK_PERIOD_US, units="us")
    assert int(dut.io_out.value) == 64

@cocotb.test()
async def test_store(dut):
    cocotb.start_soon(Clock(dut.clk, CLK_PERIOD_US, "us").start())
    dut.instr.value = 0x38
    await Timer(CLK_PERIOD_US, units="us")
    assert int(dut.io_out.value) == 128

