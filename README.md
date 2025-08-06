# FaultRando
Tool for generating random bit or byte mutations of a binary

## Setup

Tested on Python 3.8 for Debian/Ubuntu.

```bash
pip install -Ur requirements.txt
```

## Usage

```bash
python rando.py 
```
positional arguments:
- binary_path:      Path to binary
- fault_model:      byte-flip, byte-set, byte-reset, bit-flip, bit-set, bit-reset
- mutation_count:   Number of mutations per sample
- sample_size:      Number of mutation samples
- out_path:         Path to output folder
  
## Example

```bash
python rando.py ./Basic.bin bit-flip 10 100 ./test
```
creates 100 mutants each with 10 bit flip mutations in the test folder for Basic.bin
