import cocotb
from cocotb.triggers import FallingEdge, Timer
from cocotb.clock import Clock
from cocotb.binary import BinaryValue, BinaryRepresentation
import random

CLK_FREQ_HZ = 10000
CLK_PERIOD_SEC = (1 / CLK_FREQ_HZ)
CLK_PERIOD_US = CLK_PERIOD_SEC * 1000000

def start_clk(dut):
    cocotb.start_soon(Clock(dut.clk, CLK_PERIOD_US, "us").start())

def split_imm(imm):
    imm_75 = (imm & 0xe0) >> 5
    imm_43 = (imm & 0x18) >> 3
    imm_20 = imm & 0x7
    return imm_75, imm_43, imm_20

async def exit_reset(dut):
    dut.rst.value = 1;
    await FallingEdge(dut.clk)
    dut.rst.value = 0;

async def exit_start_state(dut):
    dut.instr.value = 0x3f
    await FallingEdge(dut.clk)

async def do_preamble(dut):
    start_clk(dut)
    await exit_reset(dut)
    await exit_start_state(dut)

async def drive_instr(dut, bits35, bits02):
    instr_val = BinaryValue(n_bits=6, bigEndian=False, binaryRepresentation=BinaryRepresentation.UNSIGNED)
    instr_val.binstr = '{:03b}{:03b}'.format(bits35, bits02)
    dut.instr.value = instr_val
    await FallingEdge(dut.clk)
    instr_val.binstr = 'zzzzzz'
    dut.instr.value = instr_val

async def execute_disp(dut, src):
    await drive_instr(dut, 0, src)

async def execute_add(dut, dest, src_a, src_b):
    await drive_instr(dut, 1, src_a)
    await drive_instr(dut, dest, src_b)

async def execute_add_i(dut, dest, src, imm):
    imm_75 = (imm & 0xe0) >> 5
    imm_43 = (imm & 0x18) >> 3
    imm_20 = imm & 0x7
    await drive_instr(dut, 2, src)
    await drive_instr(dut, dest, imm_75)
    await drive_instr(dut, imm_43, imm_20)

async def execute_and(dut, dest, src_a, src_b):
    await drive_instr(dut, 3, src_a)
    await drive_instr(dut, dest, src_b)

async def execute_and_i(dut, dest, src, imm):
    imm_75, imm_43, imm_20 = split_imm(imm)
    await drive_instr(dut, 4, src)
    await drive_instr(dut, dest, imm_75)
    await drive_instr(dut, imm_43, imm_20)

async def execute_or(dut, dest, src_a, src_b):
    await drive_instr(dut, 5, src_a)
    await drive_instr(dut, dest, src_b)

async def execute_or_i(dut, dest, src, imm):
    imm_75, imm_43, imm_20 = split_imm(imm)
    await drive_instr(dut, 6, src)
    await drive_instr(dut, dest, imm_75)
    await drive_instr(dut, imm_43, imm_20)

async def execute_store(dut, dest, imm):
    imm_75, imm_43, imm_20 = split_imm(imm)
    await drive_instr(dut, 7, 0)
    await drive_instr(dut, dest, imm_75)
    await drive_instr(dut, imm_43, imm_20)

def check_fetch(dut, opcode=None, opcode_valid=1, dest=None, src_a=None, src_b=None, imm=None):
    if opcode is not None:
        assert int(dut.toy.fetch.opcode) == opcode
    assert int(dut.toy.fetch.op_valid) == opcode_valid
    if dest is not None:
        assert int(dut.toy.fetch.dest) == dest
    if src_a is not None:
        assert int(dut.toy.fetch.src_a) == src_a
    if src_b is not None:
        assert int(dut.toy.fetch.src_b) == src_b
    if imm is not None:
        assert int(dut.toy.fetch.imm) == imm

async def check_out(dut, out_val):
    await FallingEdge(dut.clk)
    assert int(dut.io_out) == out_val

@cocotb.test()
async def fetch_disp(dut):
    src = random.randint(0, 7)
    await do_preamble(dut)
    await execute_disp(dut, src)
    check_fetch(dut, 0, src_a=src)

@cocotb.test()
async def fetch_add(dut):
    dest = random.randint(0, 7)
    src_a = random.randint(0, 7)
    src_b = random.randint(0, 7)
    await do_preamble(dut)
    await execute_add(dut, dest, src_a, src_b)
    check_fetch(dut, 1, dest=dest, src_a=src_a, src_b=src_b)

@cocotb.test()
async def fetch_add_i(dut):
    dest = random.randint(0, 7)
    src = random.randint(0, 7)
    imm = random.randint(0, 255)
    await do_preamble(dut)
    await execute_add_i(dut, dest, src, imm)
    check_fetch(dut, 2, dest=dest, src_a=src, imm=imm)

@cocotb.test()
async def fetch_and(dut):
    dest = random.randint(0, 7)
    src_a = random.randint(0, 7)
    src_b = random.randint(0, 7)
    await do_preamble(dut)
    await execute_and(dut, dest, src_a, src_b)
    check_fetch(dut, 3, dest=dest, src_a=src_a, src_b=src_b)

@cocotb.test()
async def fetch_and_i(dut):
    dest = random.randint(0, 7)
    src = random.randint(0, 7)
    imm = random.randint(0, 255)
    await do_preamble(dut)
    await execute_and_i(dut, dest, src, imm)
    check_fetch(dut, 4, dest=dest, src_a=src, imm=imm)

@cocotb.test()
async def fetch_or(dut):
    dest = random.randint(0, 7)
    src_a = random.randint(0, 7)
    src_b = random.randint(0, 7)
    await do_preamble(dut)
    await execute_or(dut, dest, src_a, src_b)
    check_fetch(dut, 5, dest=dest, src_a=src_a, src_b=src_b)

@cocotb.test()
async def fetch_or_i(dut):
    dest = random.randint(0, 7)
    src = random.randint(0, 7)
    imm = random.randint(0, 255)
    await do_preamble(dut)
    await execute_or_i(dut, dest, src, imm)
    check_fetch(dut, 6, dest=dest, src_a=src, imm=imm)

@cocotb.test()
async def fetch_store(dut):
    dest = random.randint(0, 7)
    imm = random.randint(0, 255)
    await do_preamble(dut)
    await execute_store(dut, dest, imm)
    check_fetch(dut, 7, dest=dest, imm=imm)

@cocotb.test()
async def fetch_intermediate_check(dut):
    start_clk(dut)
    await exit_reset(dut)
    check_fetch(dut, opcode_valid=0)
    await exit_start_state(dut)
    check_fetch(dut, opcode_valid=0)
    await drive_instr(dut, 4, 0)
    check_fetch(dut, opcode_valid=0)
    await drive_instr(dut, 1, 2)
    check_fetch(dut, opcode_valid=0)
    await drive_instr(dut, 3, 4)
    check_fetch(dut, opcode=4, opcode_valid=1)

@cocotb.test()
async def fetch_b2b_add_and(dut):
    dest = random.randint(0, 7)
    src_a = random.randint(0, 7)
    src_b = random.randint(0, 7)
    await do_preamble(dut)
    # Execute add
    await execute_add(dut, dest, src_a, src_b)
    check_fetch(dut, 1, dest=dest, src_a=src_a, src_b=src_b)
    # Check op is not valid
    await FallingEdge(dut.clk)
    check_fetch(dut, opcode_valid=0)
    # Execute and
    dest = random.randint(0, 7)
    src_a = random.randint(0, 7)
    src_b = random.randint(0, 7)
    await execute_and(dut, dest, src_a, src_b)
    check_fetch(dut, 3, dest=dest, src_a=src_a, src_b=src_b)

@cocotb.test()
async def disp(dut):
    reg = random.randint(0, 7)
    imm = random.randint(0, 255)
    await do_preamble(dut)
    await execute_disp(dut, reg)
    await check_out(dut, 0)
    await execute_store(dut, reg, imm)
    await execute_disp(dut, reg)
    await check_out(dut, imm)

@cocotb.test()
async def add(dut):
    dest = random.randint(0, 7)
    src_a = random.randint(0, 7)
    src_b = random.randint(0, 7)
    imm_a = random.randint(0, 255)
    imm_b = random.randint(0, 255)
    expected_val = (imm_a + imm_b) & 0xff
    if (src_a == src_b):
        expected_val = (imm_b + imm_b) & 0xff
    await do_preamble(dut)
    await execute_store(dut, src_a, imm_a)
    await execute_store(dut, src_b, imm_b)
    await execute_add(dut, dest, src_a, src_b)
    await check_out(dut, expected_val)

@cocotb.test(skip=True)
async def add_i(dut):
    cocotb.start_soon(Clock(dut.clk, CLK_PERIOD_US, "us").start())
    dut.instr.value = 0x10
    await Timer(CLK_PERIOD_US, units="us")
    assert int(dut.io_out.value) == 4

@cocotb.test(skip=True)
async def _and(dut):
    cocotb.start_soon(Clock(dut.clk, CLK_PERIOD_US, "us").start())
    dut.instr.value = 0x18
    await Timer(CLK_PERIOD_US, units="us")
    assert int(dut.io_out.value) == 8

@cocotb.test(skip=True)
async def and_i(dut):
    cocotb.start_soon(Clock(dut.clk, CLK_PERIOD_US, "us").start())
    dut.instr.value = 0x20
    await Timer(CLK_PERIOD_US, units="us")
    assert int(dut.io_out.value) == 16

@cocotb.test(skip=True)
async def _or(dut):
    cocotb.start_soon(Clock(dut.clk, CLK_PERIOD_US, "us").start())
    dut.instr.value = 0x28
    await Timer(CLK_PERIOD_US, units="us")
    assert int(dut.io_out.value) == 32

@cocotb.test(skip=True)
async def or_i(dut):
    cocotb.start_soon(Clock(dut.clk, CLK_PERIOD_US, "us").start())
    dut.instr.value = 0x30
    await Timer(CLK_PERIOD_US, units="us")
    assert int(dut.io_out.value) == 64

@cocotb.test(skip=True)
async def store(dut):
    cocotb.start_soon(Clock(dut.clk, CLK_PERIOD_US, "us").start())
    dut.instr.value = 0x38
    await Timer(CLK_PERIOD_US, units="us")
    assert int(dut.io_out.value) == 128

