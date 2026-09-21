<!---

This file is used to generate your project datasheet. Please fill in the information below and delete any unused
sections.

You can also include images in this folder and reference them in the markdown. Each image must be less than
512 kb in size, and the combined size of all images must be less than 1 MB.
-->

## How it works

This project implements an 8-bit programmable binary counter with an asynchronous reset, synchronous load, and tri-state outputs.

On each rising edge of the clock, the counter increments by one. Since the counter is 8 bits wide, it counts from 0 to 255 and wraps back to 0 after reaching 255.

The `LOAD` input allows a custom 8-bit value from `DATA[7:0]` to be loaded into the counter. Loading is synchronous, so the new value is stored on the next rising edge of the clock when `LOAD` is high. When `LOAD` is low, normal counting continues.

The active-low reset (`rst_n`) is asynchronous. Pulling `rst_n` low immediately resets the counter to 0 without waiting for a clock edge.

The `OE` (output enable) input controls the tri-state output. When `OE` is high, `COUNT[7:0]` outputs the current counter value. When `OE` is low, the outputs are placed in the high-impedance (`Z`) state.

### Pin usage

- `DATA[7:0]` — 8-bit value used for synchronous loading
- `LOAD` — load `DATA[7:0]` on the next rising clock edge
- `OE` — enable the counter outputs
- `COUNT[7:0]` — current 8-bit counter value
- `clk` — counter clock
- `rst_n` — active-low asynchronous reset

## How to test

The included cocotb testbench verifies:

- asynchronous reset behavior
- normal binary counting
- synchronous loading
- overflow from 255 back to 0
- tri-state output behavior

Run the test suite from the `test/` directory:

```
cd test
make -B
```

A successful run should report that all cocotb tests passed.
