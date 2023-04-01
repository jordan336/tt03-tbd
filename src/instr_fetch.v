module instr_fetch (input        clk,
                    input        rst,
                    input  [5:0] in,
                    output       op_valid,
                    output [2:0] opcode,
                    output [2:0] src_a,
                    output [2:0] src_b,
                    output [2:0] dest,
                    output [7:0] imm);
  assign opcode = in[5:3];
  assign src_a = in[2:0];
endmodule
