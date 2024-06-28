# FreeBayes Parallel Runner

This script allows you to run FreeBayes in parallel, using multiple cores to process each line of a BED file. Each region specified in the BED file is processed in a separate core, and you can specify the number of cores to use as well as the base name for the output files.

## Prerequisites

- Python 3
- FreeBayes
- A BED file specifying the regions to analyze
- An indexed reference genome file
- A list of BAM files names/paths (One per line)

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/freebayes-parallel-runner.git
    cd freebayes-parallel-runner
    ```

2. Ensure FreeBayes is installed and available in your PATH:
    ```bash
    sudo apt-get install freebayes
    ```

## Usage

1. Prepare your BED file, reference genome file, and BAM list file.

2. Modify the script to specify the paths to your files and the number of cores to use:
    ```python
    BED_FILE = 'path/to/your_bed_file.bed'
    REF = 'path/to/your_reference.fasta'
    BAM_LIST = 'path/to/your_bam_list.txt'
    OUTPUT_BASE_NAME = 'output'  # Change this to your desired base name
    NUM_CORES = 4  # Adjust this to the number of cores you want to use
    ```

3. Run the script:
    ```bash
    python freebayes_parallel_runner.py
    ```

## Example

```python
import subprocess
import time
from multiprocessing import Pool, cpu_count

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
    print(f"Total time taken: {elapsed_time:.2f} seconds")```

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contributing

1. Fork the repository
2 . Create your feature branch (git checkout -b feature/fooBar)
3. Commit your changes (git commit -am 'Add some fooBar')
4. Push to the branch (git push origin feature/fooBar)
5. Create a new Pull Request

## Acknowledgements

- FreeBayes
- Python
- multiprocessing module

## Contact

For any questions or suggestions, please open an issue or contact me at [marcel.ferreira@unesp.br].