![](../../workflows/gds/badge.svg) ![](../../workflows/docs/badge.svg)

# Toy CPU

Toy CPU is an 8 bit toy CPU for the Tiny Tapeout project.

# I/O Interface

|#|Input         |Output     |
|-|--------------|-----------|
|0|clk           |data_out[0]|
|1|rst           |data_out[1]|
|2|instruction[0]|data_out[2]|
|3|instruction[1]|data_out[3]|
|4|instruction[2]|data_out[4]|
|5|instruction[3]|data_out[5]|
|6|instruction[4]|data_out[5]|
|7|instruction[5]|data_out[6]|

# ISA

|Opcode|Mnemonic|Name           |Description                         |
|------|--------|---------------|------------------------------------|
|000   |DISP    |Display        |data_out = reg[src_a]               |
|001   |ADD     |Add            |reg[dest] = reg[src_a] + reg[src_b] |
|010   |ADD_I   |Add (immediate)|reg[dest] = reg[src_a] + imm        |
|011   |AND     |And            |reg[dest] = reg[src_a] & reg[src_b] |
|100   |AND_I   |And (immediate)|reg[dest] = reg[src_a] & imm        |
|101   |OR      |Or             |reg[dest] = reg[src_a] \| reg[src_b]|
|110   |OR_I    |Or (immediate) |reg[dest] = reg[src_a] \| imm       |
|111   |STRE    |Store          |reg[dest] = imm                     |

## Instruction format

Instructions are passed using the upper 6 bits of the inputs. Depending on the opcode, the full instruction with opcode and all arguments is passed using one, two, or three 6 bit instruction words.

|Word|Input [7:5] |Input [4:2]           |Input [1]|Input [0]|
|----|------------|----------------------|---------|---------|
|0   |opcode[2:0] |src_a[2:0]            |rst      |clk      |
|1   |dest[2:0]   |src_b[2:0] or imm[7:5]|rst      |clk      |
|2   |{X,imm[4:3]}|imm[2:0]              |rst      |clk      |

|Opcode|Mnemonic|Number of Instruction Words|
|------|--------|---------------------------|
|000   |DISP    |1                          |
|001   |ADD     |2                          |
|010   |ADD_I   |3                          |
|011   |AND     |2                          |
|100   |AND_I   |3                          |
|101   |OR      |2                          |
|110   |OR_I    |3                          |
|111   |STRE    |3                          |

## Start input

After exiting reset, the Toy CPU looks for a start input to begin processing the instruction stream. The start input is all 1s in the 6 bit instruction word (0x3F). After sampling the start sequence, the CPU will interpret the next 6 bit instruction word as the first word in the instruction stream.

# What is Tiny Tapeout?

TinyTapeout is an educational project that aims to make it easier and cheaper than ever to get your digital designs manufactured on a real chip!

Go to https://tinytapeout.com for instructions!

