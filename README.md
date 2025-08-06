# FaultRando
Tool for generating random bit or byte fault mutations of a binary

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
Creates 100 mutants each with 10 bit-flip mutations in the test folder for Basic.bin

For each mutant binary, the tool creates a JSON and PNG of the mutation locations

<img width="1010" height="740" alt="Screenshot 2025-08-06 193335" src="https://github.com/user-attachments/assets/c0a3ba25-06e8-4685-9a46-f6a85e96d811" />

<img width="565" height="667" alt="Screenshot 2025-08-06 193415" src="https://github.com/user-attachments/assets/4410979f-a6ac-4fbc-8859-5bbe9ae4e273" />

## Fault Models

original-binary = 01000101

byte-flip -> **10111010**

byte-set -> **11111111**

byte-reset -> **00000000**

bit-flip -> **1**1000101

bit-set -> **1**1000101

bit-reset -> **0**1000101
