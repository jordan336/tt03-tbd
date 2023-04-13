module alu (input      [2:0] opcode,
            input      [7:0] a,
            input      [7:0] b,
            output reg [7:0] out);
  always @(*) begin
    case (opcode)
      3'b000: out = a;
      3'b001,
      3'b010: out = a + b;
      3'b011,
      3'b100: out = a & b;
      3'b101,
      3'b110: out = a | b;
      3'b111: out = a;
    endcase
  end
endmodule
