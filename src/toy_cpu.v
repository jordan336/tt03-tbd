module toy_cpu (input        clk,
                input        rst,
                input        op_valid,
                input  [2:0] opcode,
                input  [2:0] src_a,
                input  [2:0] src_b,
                input  [2:0] dest,
                input  [7:0] imm,
                output [7:0] out);
  wire wr_en;
  wire [7:0] wr_data;
  wire [7:0] src_a_data;
  wire [7:0] src_b_data;
  wire [7:0] alu_b;

  decode decode(.op_valid(op_valid),
                .opcode(opcode),
                .imm(imm),
                .src_b_data(src_b_data),
                .alu_out(out),
                .wr_en(wr_en),
                .wr_data(wr_data),
                .alu_operand(alu_b));

  reg_file reg_file(.clk(clk),
                    .rst(rst),
                    .rd0_addr(src_a),
                    .rd1_addr(src_b),
                    .wr_addr(dest),
                    .wr_en(wr_en),
                    .wr_data(wr_data),
                    .out0(src_a_data),
                    .out1(src_b_data));

  alu alu(.opcode(opcode),
          .a(src_a_data),
          .b(alu_b),
          .out(out));
endmodule
