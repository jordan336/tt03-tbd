module instr_fetch (input            clk,
                    input            rst,
                    input      [5:0] in,
                    output reg       op_valid,
                    output reg [2:0] opcode,
                    output reg [2:0] src_a,
                    output reg [2:0] src_b,
                    output reg [2:0] dest,
                    output reg [7:0] imm);
  assign src_a = in[2:0];

  always @(posedge clk) begin
    opcode <= in[5:3];
  end
endmodule
