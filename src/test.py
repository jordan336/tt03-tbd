import cocotb
from cocotb.triggers import Timer
import random

@cocotb.test()
async def test_nop(dut):
    dut.io_in.value = 0x0
    await Timer(1, units="ns")
    assert int(dut.io_out.value) == 1

@cocotb.test()
async def test_add(dut):
    dut.io_in.value = 0x20
    await Timer(1, units="ns")
    assert int(dut.io_out.value) == 2

@cocotb.test()
async def test_addi(dut):
    dut.io_in.value = 0x40
    await Timer(1, units="ns")
    assert int(dut.io_out.value) == 4

@cocotb.test()
async def test_and(dut):
    dut.io_in.value = 0x60
    await Timer(1, units="ns")
    assert int(dut.io_out.value) == 8

@cocotb.test()
async def test_andi(dut):
    dut.io_in.value = 0x80
    await Timer(1, units="ns")
    assert int(dut.io_out.value) == 16

@cocotb.test()
async def test_or(dut):
    dut.io_in.value = 0xa0
    await Timer(1, units="ns")
    assert int(dut.io_out.value) == 32

@cocotb.test()
async def test_ori(dut):
    dut.io_in.value = 0xc0
    await Timer(1, units="ns")
    assert int(dut.io_out.value) == 64

@cocotb.test()
async def test_store(dut):
    dut.io_in.value = 0xe0
    await Timer(1, units="ns")
    assert int(dut.io_out.value) == 128

