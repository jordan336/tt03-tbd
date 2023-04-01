`default_nettype none
`timescale 1ns/1ps

module tb (input [7:0] io_in,
           output [7:0] io_out);
  initial begin
    $dumpfile("tb.vcd");
    $dumpvars(0, tb);
    #1;
  end

  jordan336_toy_cpu toy(.io_in(io_in),
                        .io_out(io_out));
endmodule
