#!/usr/bin/env python
"""This script will filter vcf file(s) based on a list of SNPs in a provided
text file. 
Author: Oleksandr Moskalenko <om@hpc.ufl.edu>
Version: 0.1
Date: 2014-08-01
"""
import os, sys, operator, logging, gzip, vcf, argparse

__version="0.1"

def get_arguments():
    parser = argparse.ArgumentParser(usage='%(prog)s [options] -i input_file', epilog="You must at least provide the input file name and some vcf files as arguments.")
    parser.add_argument('-i', '--input', dest='infile', help="Input vcf file")
#    parser.add_argument('infiles', nargs='*', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('infiles', nargs='*', help="VCF files to process" )
    parser.add_argument('-o', '--outdir', dest='outdir', help="Directory for output files")
    parser.add_argument('-s', '--suffix', dest='suffix', default='filtered', help="Suffix for filtered filenames")
#    parser.add_argument('-z', '--zip', action='store_true', default=False, help="Compress output files with gzip")
    parser.add_argument('-v', '--verbose', action='store_true', default=False, help="Verbose output")
    parser.add_argument('-d', '--debug', action='store_true', default=False, help="Debug the script")
    parser.add_argument('--version', action='version', version='%(prog)s Version: {version}'.format(version=__version))
    args = parser.parse_args()
    if (not args.infile):
        parser.print_help()
        sys.exit(1)
    else:
        if not os.access(args.infile, os.R_OK):
            sys.exit("Cannot access variant list file")
    return args

def read_snp_list(args):
    snps = frozenset( x.strip() for x in open(args.infile) )
    return snps

def filter_vcf_files(args, vcf_files, snp_list):
    for input_file in vcf_files:
        if args.verbose:
            print "Processing file {0}".format(input_file)
        suffix = args.suffix
        file_basename = os.path.split(input_file)[1]
        file_name_base = file_basename.split('.vcf')[0]
        outfile_name = file_name_base + '_' + args.suffix + '.vcf'
        if args.outdir:
            outfile_name = file_name_base + '_' + args.suffix + '.vcf'
            outpath = os.path.join(args.outdir, outfile_name)
        else:
            outpath = outfile_name
        if args.verbose:
            print "Writing output to {0}".format(outpath)
        if file_basename.endswith('gz'):
            input_fh = open(input_file, 'rb')
        else:
            input_fh = open(input_file,'r')
        v_reader = vcf.Reader(input_fh)
        output_fh = open(outpath, 'w')
        v_writer = vcf.Writer(output_fh, v_reader)
        for record in v_reader:
            if args.debug:
                print "{0}\t{1}".format(record.CHROM, record.ID, record.INFO)
            if record.ID in snp_list:
                if args.verbose:
                    print "Found matching ID: {0}".format(record.ID)
                v_writer.write_record(record)

if __name__=='__main__':
    logger = logging.getLogger(__name__)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s:%(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    logger.setLevel('DEBUG')
    if sys.version_info < (2,7,0):
        print ("You need python 2.7 or later to run this script.")
        sys.exit(1)
    args = get_arguments()
    input_types = ['gz', 'vcf']
    try:
        vcf_list_fh = open(args.infile, 'r')
    except IOError:
        print 'Cannot open variant list file', arg
    vcf_files = []
    if len(args.infiles) > 0:
        if args.debug:
            print "Provided input files:\n"
            print args.infiles
        for input_file in args.infiles:
            for input_type in input_types:
                if input_file.endswith(input_type):
                    vcf_files.append(input_file)
    else:
        sys.exit("\nAt least one input file (.vcf or .vcf.gz) must be provided\n")
    snps = read_snp_list(args)
    if args.verbose:
        print("Read {0} variants from {1}".format(len(snps), args.infile))
    list_of_input_vcf_files = ", ".join(vcf_files)
    if args.verbose:
        print("\nFiles to process:\n{0}".format(list_of_input_vcf_files))
    filter_vcf_files(args, vcf_files, snps)
    sys.exit(0)
