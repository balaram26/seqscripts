#!/usr/bin/python
# encoding:utf8
# author: Balakrishnan Subramanian

"""This script takes two fastq or fastq.gz files combines them into one appending /1 or /2 accordingly.

I have modified the original script from Erik Garrison interleave 
to append /1 or /2 and combine two fastq files into one.

Usage:
    interleave-fasta fasta_file1 fasta_file2
"""

import sys


def interleave(f1, f2):
    """Interleaves two (open) fastq files.
    """
    while True:
        line = f1.readline()
        if line.strip() == "":
            break

        r1 = []
        r1.append(line.strip()+"/1")
        for i in xrange(3):
            r1.append(f1.readline().strip())
        
        r2 = []
        for i in xrange(4):
            r2.append(f2.readline().strip())
        r2[0] +='/2'
        print "\n".join(r1)
        print "\n".join(r2)


if __name__ == '__main__':
    try:
        file1 = sys.argv[1]
        file2 = sys.argv[2]
    except:
        print __doc__
        sys.exit(1)

    if file1[-2:] == "gz":
        import gzip
        with gzip.open(file1) as f1:
            with gzip.open(file2) as f2:
                interleave(f1, f2)
    else:
        with open(file1) as f1:
            with open(file2) as f2:
                interleave(f1, f2)
        