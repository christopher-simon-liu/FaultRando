import mmap
import os
import argparse
import logging
import sys
import random
import json
import math
import numpy as np
from PIL import Image
import matplotlib as mpl
from matplotlib import pyplot
from tqdm import tqdm

# Logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')

stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.INFO)
stdout_handler.setFormatter(formatter)

file_handler = logging.FileHandler('logs.log')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stdout_handler)

# Fault Models
# byte array is a list of ints
# (0 to 255) = (0x00 to 0xFF)
def fault_byte_set(byte_hex):
    return 0xFF

def fault_byte_reset(byte_hex):
    return 0x00

def fault_byte_flip(byte_hex):
    return byte_hex ^ 0xFF

def fault_bit_flip(byte_hex, bit_position):
    binary_string = bin(byte_hex)[2:].zfill(8)
    binary_list = list(binary_string)
    temp = binary_list[bit_position]
    binary_list[bit_position] = str(int(temp) ^ 1)
    binary_string = "".join(binary_list)
    return int(binary_string, 2)

def fault_bit_set(byte_hex, bit_position):
    binary_string = bin(byte_hex)[2:].zfill(8)
    binary_list = list(binary_string)
    binary_list[bit_position] = 1
    binary_string = "".join(binary_list)
    return int(binary_string, 2)

def fault_bit_reset(byte_hex, bit_position):
    binary_string = bin(byte_hex)[2:].zfill(8)
    binary_list = list(binary_string)
    binary_list[bit_position] = 0
    binary_string = "".join(binary_list)
    return int(binary_string, 2)

def main():  
    ## entry point of this program
    ## Parsing the arguments
    parser = argparse.ArgumentParser(description="Tool Options")
    parser.add_argument("binary_path", default="./Basic.bin", type=str, help="Path to binary")
    parser.add_argument("fault_model", default="byte-flip", type=str, help="byte-flip, byte-set, byte-reset, bit-flip, bit-set, bit-reset")
    parser.add_argument("mutation_count", default=1, type=int, help="Number of mutations per sample")
    parser.add_argument("sample_size", default=1, type=int, help="Number of mutation samples")
    parser.add_argument("out_path", default="./test", type=str, help="Path to output folder")

    args = parser.parse_args()
    binary_path = args.binary_path
    fault_model = args.fault_model
    mutation_count = args.mutation_count
    sample_size = args.sample_size
    out_path = args.out_path

    logger.info(f"Fault Rando: {binary_path}")

    file_name = os.path.basename(binary_path)
    base_name, file_extension = os.path.splitext(file_name)

    byte_array=[]
    size = 0    
    try:
        with open(binary_path, "r+b") as f:
            mm = mmap.mmap(f.fileno(), 0)
            byte_array = bytearray(mm)
            size = len(byte_array)
            logger.info(f"{size} bytes in binary")
            f.close()
    except FileNotFoundError:
        logger.error(f"Error: The file '{binary_path}' was not found.")

    if mutation_count < 1:
        logger.error("Mutation Count needs to be more than 1")
        raise ValueError("Mutation Count")

    if sample_size < 1:
        logger.error("Sample Size needs to be more than 1")
        raise ValueError("Sample Size")

    pbar = tqdm(total=sample_size)

    for i in range(sample_size):
        j = 0
        indexes_to_mutate = list()
        bit_positions_to_mutate = list()
        for c in range(mutation_count):
            # Random byte indexes
            index = random.randrange(0, size)
            indexes_to_mutate.append(index)
        
            # Random bit indexes
            if "bit" in fault_model:
                bit_position = random.randrange(0, 8)
                bit_positions_to_mutate.append(bit_position)
            else:
                bit_positions_to_mutate.append(0)
       
        # Rewriting Binary
        binary_to_mutate = byte_array.copy()

        for x in range(mutation_count):
            index = indexes_to_mutate[x]
            bit_position = bit_positions_to_mutate[x]

            original_byte = binary_to_mutate[index] 
            mutant_byte_hex = 0

            if fault_model == "byte-flip":
                mutant_byte_hex = fault_byte_flip(original_byte)
            elif fault_model == "byte-set":
                mutant_byte_hex = fault_byte_set(original_byte)
            elif fault_model == "byte-reset":
                mutant_byte_hex = fault_byte_reset(original_byte)
            elif fault_model == "bit-flip":
                mutant_byte_hex = fault_bit_flip(original_byte, bit_position)
            elif fault_model == "bit-set":
                mutant_byte_hex = fault_bit_set(original_byte, bit_position)
            elif fault_model == "bit-reset":
                mutant_byte_hex = fault_bit_reset(original_byte, bit_position)
            else:
                logger.error("Invalid Fault Model")
                raise ValueError("Fault Model")

            binary_to_mutate[int(index)] = mutant_byte_hex
        
        
        out_file_path = os.path.join(out_path, f"{base_name}{i}{file_extension}")
        with open(out_file_path, 'wb') as o:
            o.write(binary_to_mutate)
            o.close()  
        logger.info(f"{out_file_path} created")

        meta_data = {
            "fault_model": fault_model,
            "byte_indexes": indexes_to_mutate,
            "bit_positions": bit_positions_to_mutate
        }
        out_meta_path = os.path.join(out_path, f"{base_name}{i}.json")
        with open(out_meta_path, "w") as m:
            m.write(json.dumps(meta_data, indent=1))
            m.close()
        logger.info(f"{out_meta_path} created")


        visual_array = [0] * size
        # Calculate the square root
        sqrt_result = math.sqrt(size)
        # Round the square root up to the nearest integer
        rounded_up_result = math.ceil(sqrt_result)
        # big square
        rowlength = rounded_up_result
        collength = rounded_up_result
        fill = rowlength * collength - size
        visual_array.extend([2]*fill)

        for n in indexes_to_mutate:
            visual_array[n] = 1
    
        arr = np.array(visual_array)
        matrix = arr.reshape(rowlength, collength)
        # Colors

        WHITISH = "#FAFAFA"
        CHARCOAL = "#36454F"
        RED = "#FF0000"

        fig = pyplot.figure(f"{base_name}{i}")

        cmap = mpl.colors.ListedColormap([WHITISH, RED, CHARCOAL])
        bounds=[0,1,2,3]
        norm = mpl.colors.BoundaryNorm(bounds, cmap.N)

        # tell imshow about color map so that only set colors are used
        img = pyplot.imshow(matrix, interpolation='nearest', cmap=cmap, norm=norm)
    
        # make a color bar
        pyplot.colorbar(img, cmap=cmap, norm=norm, boundaries=bounds, ticks=[0,1,2,3])

        out_graphic_path = os.path.join(out_path, f"{base_name}{i}.png")
        fig.savefig(out_graphic_path)
        logger.info(f"{out_graphic_path} saved")
        pyplot.close()

        pbar.update(1)
    pbar.close()


if __name__ == "__main__":
    main()