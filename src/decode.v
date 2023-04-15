module decode(input        op_valid,
              input [2:0]  opcode,
              input [7:0]  imm,
              input [7:0]  src_b_data,
              input [7:0]  alu_out,
              output       wr_en,
              output [7:0] wr_data,
              output [7:0] alu_operand);
  wire opcode_disp;
  wire opcode_store;
  wire opcode_imm;

  assign opcode_disp  = (opcode == 3'b000);
  assign opcode_store = (opcode == 3'b111);
  assign opcode_imm   = ((opcode === 3'b010) ||
                         (opcode === 3'b100) ||
                         (opcode === 3'b110));

  assign wr_en = op_valid & !opcode_disp;
  assign wr_data = opcode_store ? imm : alu_out;
  assign alu_operand = opcode_imm ? imm : src_b_data;
endmodule
