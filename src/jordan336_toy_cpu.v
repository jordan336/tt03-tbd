module jordan336_toy_cpu (input [7:0] io_in,
                          output [7:0] io_out);
  assign io_out = ~io_in;
endmodule
