import subprocess
from multiprocessing import Pool, cpu_count
import time

def run_command(command):
    """Runs a shell command."""
    subprocess.run(command, shell=True)

def prepare_commands(bed_file, ref, bam_list, output_base_name, chunk_size, overlap_size):
    """Reads the BED file and prepares freebayes commands."""
    commands = []
    with open(bed_file, 'r') as f:
        lines = f.readlines()
    
    step_size = chunk_size - overlap_size
    
    for i in range(0, len(lines), step_size):
        chunk_lines = lines[i:i + chunk_size]
        regions = [f"{line.strip().split()[0]}:{line.strip().split()[1]}-{line.strip().split()[2]}" for line in chunk_lines]
        region_str = ' '.join([f"-r {region}" for region in regions])
        output_file = f"{output_base_name}_{i // step_size + 1}.vcf"
        freebayes_command = f"freebayes -f {ref} -L {bam_list} {region_str} > {output_file}"
        bgzip_command = f"bgzip {output_file}"
        tabix_command = f"tabix -p vcf {output_file}.gz"
        commands.append((freebayes_command, bgzip_command, tabix_command))
    
    return commands

def run_freebayes_with_bgzip_and_tabix(commands, total, current):
    """Runs freebayes command, compresses with bgzip, and indexes with tabix, showing progress."""
    freebayes_command, bgzip_command, tabix_command = commands
    run_command(freebayes_command)
    run_command(bgzip_command)
    run_command(tabix_command)
    print(f"Progress: {current}/{total} chunks completed")

if __name__ == '__main__':
    BED_FILE = 'your_bed_file.bed'
    REF = 'your_reference.fasta'
    BAM_LIST = 'your_bam_list.txt'
    OUTPUT_BASE_NAME = 'output'  # Change this to your desired base name
    NUM_CORES = 4  # Adjust this to the number of cores you want to use
    CHUNK_SIZE = 1000  # Adjust this to the size of pieces you want each thread to process
    OVERLAP_SIZE = 50  # Adjust this to the overlap size you want between chunks

    # Prepare the commands
    commands = prepare_commands(BED_FILE, REF, BAM_LIST, OUTPUT_BASE_NAME, CHUNK_SIZE, OVERLAP_SIZE)
    total_chunks = len(commands)
    
    # Start timing
    start_time = time.time()
    
    # Use a pool of workers to run the commands in parallel with progress
    with Pool(NUM_CORES) as pool:
        for i, _ in enumerate(pool.imap_unordered(run_freebayes_with_bgzip_and_tabix, commands), 1):
            print(f"Progress: {i}/{total_chunks} chunks completed")
    
    # End timing
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Total time taken: {elapsed_time:.2f} seconds")
    
    # Run the final bcftools concat command
    print(f"Concatenating {total_chunks} files into {NUM_CORES} threads")
    concat_command = f"bcftools concat --threads {NUM_CORES} -a --rm-dups all -o {OUTPUT_BASE_NAME}.vcf.gz *.vcf.gz"
    run_command(concat_command)
