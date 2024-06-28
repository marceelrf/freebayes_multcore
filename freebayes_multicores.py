import subprocess
from multiprocessing import Pool, cpu_count

def run_freebayes(command):
    """Runs a freebayes command."""
    subprocess.run(command, shell=True)

def prepare_commands(bed_file, ref, bam_list):
    """Reads the BED file and prepares freebayes commands."""
    commands = []
    with open(bed_file, 'r') as f:
        for idx, line in enumerate(f):
            columns = line.strip().split()
            chr, start, end = columns[0], columns[1], columns[2]
            region = f"{chr}:{start}-{end}"
            command = f"freebayes -f {ref} -L {bam_list} -r {region} > out{idx + 1}.vcf"
            commands.append(command)
    return commands

if __name__ == '__main__':
    BED_FILE = 'your_bed_file.bed'
    REF = 'your_reference.fasta'
    BAM_LIST = 'your_bam_list.txt'
    NUM_CORES = 4  # Adjust this to the number of cores you want to use

    # Prepare the commands
    commands = prepare_commands(BED_FILE, REF, BAM_LIST)

    # Use a pool of workers to run the commands in parallel
    with Pool(NUM_CORES) as pool:
        pool.map(run_freebayes, commands)
