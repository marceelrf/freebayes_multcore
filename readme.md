# Freebayes Multicores Runner

This script allows you to run Freebayes in parallel, using multiple cores to process each line of a BED file. Each region specified in the BED file is processed in a separate core, and you can specify the number of cores to use as well as the base name for the output files.

## Prerequisites

- Python 3
- Required Python Packages:
    - subprocess
    - multiprocessing
    - time
- Freebayes
- tabix
- bgzip
- bcftools
- A BED file specifying the regions to analyze
- An indexed reference genome file
- A list of BAM files names/paths (One per line)

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/marceelrf/freebayes_multcore.git
    cd freebayes_multcore
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
    python freebayes_multicores.py
    ```

## Example

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contributing

1. Fork the repository
2. Create your feature branch (git checkout -b feature/fooBar)
3. Commit your changes (git commit -am 'Add some fooBar')
4. Push to the branch (git push origin feature/fooBar)
5. Create a new Pull Request

## Acknowledgements

- Freebayes
- Python
- multiprocessing module

## Contact

For any questions or suggestions, please open an issue or contact me at [marcel.ferreira@unesp.br].