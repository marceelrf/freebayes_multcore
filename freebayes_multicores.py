import subprocess
from multiprocessing import Pool, cpu_count
import time

def run_freebayes(command):
    """Runs a freebayes command."""
    subprocess.run(command, shell=True)

def prepare_commands(bed_file, ref, bam_list, output_base_name):
    """Reads the BED file and prepares freebayes commands."""
    commands = []
    with open(bed_file, 'r') as f:
        for idx, line in enumerate(f):
            columns = line.strip().split()
            chr, start, end = columns[0], columns[1], columns[2]
            region = f"{chr}:{start}-{end}"
            command = f"freebayes -f {ref} -L {bam_list} -r {region} > {output_base_name}_{idx + 1}.vcf"
            commands.append(command)
    return commands

if __name__ == '__main__':
    BED_FILE = 'your_bed_file.bed'
    REF = 'your_reference.fasta'
    BAM_LIST = 'your_bam_list.txt'
    OUTPUT_BASE_NAME = 'output'  # Change this to your desired base name
    NUM_CORES = 4  # Adjust this to the number of cores you want to use

    # Prepare the commands
    commands = prepare_commands(BED_FILE, REF, BAM_LIST, OUTPUT_BASE_NAME)
    
    # Start timing
    start_time = time.time()
    
    # Use a pool of workers to run the commands in parallel
    with Pool(NUM_CORES) as pool:
        pool.map(run_freebayes, commands)
        
    # End timing
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Total time taken: {elapsed_time:.2f} seconds")
