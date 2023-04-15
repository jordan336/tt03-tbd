module toy_cpu (input        clk,
                input        rst,
                input        op_valid,
                input  [2:0] opcode,
                input  [2:0] src_a,
                input  [2:0] src_b,
                input  [2:0] dest,
                input  [7:0] imm,
                output [7:0] out);
  wire reg_wr_en = op_valid & |opcode;
  wire [7:0] reg_wr_data = (opcode == 3'b111) ? imm : out;
  wire [7:0] reg_out0;
  wire [7:0] reg_out1;
  wire opcode_imm;
  wire [7:0] alu_b;

  assign opcode_imm = ((opcode === 3'b010) ||
                       (opcode === 3'b100) ||
                       (opcode === 3'b110));

  assign alu_b = opcode_imm ? imm : reg_out1;

  reg_file reg_file(.clk(clk),
                    .rst(rst),
                    .rd0_addr(src_a),
                    .rd1_addr(src_b),
                    .wr_addr(dest),
                    .wr_en(reg_wr_en),
                    .wr_data(reg_wr_data),
                    .out0(reg_out0),
                    .out1(reg_out1));

  alu alu(.opcode(opcode),
          .a(reg_out0),
          .b(alu_b),
          .out(out));
endmodule
