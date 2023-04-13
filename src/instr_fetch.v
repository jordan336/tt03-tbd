module instr_fetch (input            clk,
                    input            rst,
                    input      [5:0] in,
                    output reg       op_valid,
                    output reg [2:0] opcode,
                    output reg [2:0] src_a,
                    output reg [2:0] src_b,
                    output reg [2:0] dest,
                    output reg [7:0] imm);

  localparam STATE_START = 2'b00;
  localparam STATE_ONE   = 2'b01;
  localparam STATE_TWO   = 2'b10;
  localparam STATE_THREE = 2'b11;

  reg [1:0] state, new_state;
  reg load_opcode;
  reg load_src_a;
  reg load_src_b;
  reg load_dest;
  reg load_imm_upper;
  reg load_imm_lower;
  reg op_valid_next;

  always @(*) begin
    new_state = state;
    load_opcode = 0;
    load_src_a = 0;
    load_src_b = 0;
    load_dest = 0;
    load_imm_upper = 0;
    load_imm_lower = 0;
    op_valid_next = 0;

    case (state)
      STATE_START: begin
        if (in === '1) begin
          new_state = STATE_ONE;
        end
      end
      STATE_ONE: begin
        load_opcode = 1;
        load_src_a = 1;
        if (!$isunknown(in[5:3])) begin
          if (in[5:3] === 3'b000) begin
            new_state = STATE_ONE;
            op_valid_next = 1;
          end else begin
            new_state = STATE_TWO;
          end
        end
      end
      STATE_TWO: begin
        load_dest = 1;
        if ((opcode === 3'b010) ||
            (opcode === 3'b100) ||
            (opcode === 3'b110) ||
            (opcode === 3'b111)) begin
          load_imm_upper = 1;
          new_state = STATE_THREE;
        end else begin
          load_src_b = 1;
          op_valid_next = 1;
          new_state = STATE_ONE;
        end
      end
      STATE_THREE: begin
        load_imm_lower = 1;
        op_valid_next = 1;
        new_state = STATE_ONE;
      end
    endcase
  end

  always @(posedge clk, posedge rst) begin
    if (rst == 1'b1) begin
      state <= STATE_START;
    end else begin
      state <= new_state;
    end
  end

  always @(posedge clk) begin
    if (load_opcode) begin
      opcode <= in[5:3];
    end
  end

  always @(posedge clk) begin
    if (load_src_a) begin
      src_a <= in[2:0];
    end
  end

  always @(posedge clk) begin
    if (load_src_b) begin
      src_b <= in[2:0];
    end
  end

  always @(posedge clk) begin
    if (load_dest) begin
      dest <= in[5:3];
    end
  end

  always @(posedge clk) begin
    if (load_imm_lower) begin
      imm[4:0] <= in[4:0];
    end
    if (load_imm_upper) begin
      imm[7:5] <= in[2:0];
    end
  end

  always @(posedge clk) begin
    op_valid <= op_valid_next;
  end
endmodule
