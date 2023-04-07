`default_nettype none
`timescale 1ns/1ps

module tb (input clk,
           input rst,
           input [5:0] instr,
           output [7:0] io_out);
  initial begin
    $dumpfile("tb.vcd");
    $dumpvars(0, tb);
    #1;
  end

  jordan336_toy_cpu toy(.io_in({instr, rst, clk}),
                        .io_out(io_out));
endmodule
