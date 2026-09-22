<!---

This file is used to generate your project datasheet. Please fill in the information below and delete any unused
sections.

You can also include images in this folder and reference them in the markdown. Each image must be less than
512 kb in size, and the combined size of all images must be less than 1 MB.
-->

## How it works

This project implements an 8-bit programmable binary counter with asynchronous reset, synchronous load, and tri-state outputs.

On each rising edge of the clock, the counter increments by one, wrapping from 255 back to 0.

The `uio[7:0]` pins are shared between loading and output. When `LOAD` is high, they act as inputs and their 8-bit value is loaded into the counter on the next rising clock edge.

When `LOAD` is low and `OE` is high, `uio[7:0]` outputs the current counter value. When `OE` is low, the pins are placed in the high-impedance (`Z`) state.

The active-low `rst_n` asynchronously resets the counter to 0.

### Pin usage

- `LOAD` — enable synchronous loading
- `OE` — enable counter output
- `uio[7:0]` — 8-bit load input / counter output
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
