# vcf_filter
Filter vcf files based on a list of SNPs

This script requres python-2.7 and either uses the PyVCF python module
(https://github.com/jamescasbon/PyVCF) or just processes a vcf file as
tab-delimited text in the basic mode to filter the data for SNPs listed in a
separate file.

Usage: filter_vcf.py [options] -i input_file

positional arguments:
  infiles               VCF files to process

optional arguments:
  -h, --help            show this help message and exit
  -i INFILE, --input INFILE
                        Input vcf file
  -o OUTDIR, --outdir OUTDIR
                        Directory for output files
  -s SUFFIX, --suffix SUFFIX
                        Suffix for filtered filenames
  -v, --verbose         Verbose output
  -d, --debug           Debug the script
  -b, --basic           Basic Mode - do not use PyVCF; treat as plain text
  --version             show program's version number and exit

You must at least provide the input file name and some vcf files as arguments.


Example:

$ vcf_filter.py -b -i snp_list.txt -o filtered_data input_data/*.vcf

Performance:

The script can take a 300k+ list of SNPs and process the entire Denisovan genome
in a few minutes or the Neanderthal genome data from the 1000 genomes project in
under an hour when run in parallel on all chromosomes.
