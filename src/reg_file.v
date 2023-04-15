module reg_file (input        clk,
                 input        rst,
                 input  [2:0] rd0_addr,
                 input  [2:0] rd1_addr,
                 input  [2:0] wr_addr,
                 input        wr_en,
                 input  [7:0] wr_data,
                 output [7:0] out0,
                 output [7:0] out1);
  reg [7:0] regs[8];

  always @(posedge clk, posedge rst) begin
    if (rst === 1) begin
      regs[0] <= '0;
      regs[1] <= '0;
      regs[2] <= '0;
      regs[3] <= '0;
      regs[4] <= '0;
      regs[5] <= '0;
      regs[6] <= '0;
      regs[7] <= '0;
    end else begin
      if (wr_en === 1) begin
        regs[wr_addr] <= wr_data;
      end
    end
  end

  assign out0 = regs[rd0_addr];
  assign out1 = regs[rd1_addr];

endmodule

