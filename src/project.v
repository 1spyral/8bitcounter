/*
 * Copyright (c) 2026 Luke Zhan
 * SPDX-License-Identifier: Apache-2.0
 */

`default_nettype none

module tt_um_1spyral (
    input  wire [7:0] ui_in,    // Dedicated inputs
    output wire [7:0] uo_out,   // Dedicated outputs
    input  wire [7:0] uio_in,   // IOs: Input path
    output wire [7:0] uio_out,  // IOs: Output path
    output wire [7:0] uio_oe,   // IOs: Enable path (active high: 0=input, 1=output)
    input  wire       ena,      // always 1 when the design is powered, so you can ignore it
    input  wire       clk,      // clock
    input  wire       rst_n     // reset_n - low to reset
);

  // All output pins must be assigned. If not used, assign to 0.
  assign uio_out = 0;
  assign uio_oe  = 0;

  reg [7:0] count;

  always @(posedge clk or negedge rst_n) begin
    if (!rst_n)
      count <= '0;
    else if (uio_in[0])
      count <= ui_in;
    else
      count <= count + 1;
  end

  assign uo_out = uio_in[1] ? count : 8'bz;

  // List all unused inputs to prevent warnings
  wire _unused = &{ena, uio_in[7:2], 1'b0};

endmodule
