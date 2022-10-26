#!/usr/bin/python
# encoding:utf8
# authors: Balakrishnan subramanian
"""
This script takes one fastq (or fastq.gz) file and seperate them to read1 and read 2 files.
** pure python script, 
** reads the fastq file of any size and continually write them to read1 and 2 files accordingly, 
doesnt have any RAM requirement to store the sequence data.
"""

import os
import sys
import io,gzip
import zipfile


def parseFqfiles(inFile,isPaired,outOneName,outTwoName=None, gz=False, quiet=False):
 singleRead = []

 f = readFile(gz,inFile)
 unKnownRead = 'unKnown'
 for line in f:
  if(len(singleRead)>=4):
   processRead(singleRead,isPaired,unKnownRead,outOneName,outTwoName,quiet)
   singleRead = []
   singleRead.append(line.strip())
  else:
   singleRead.append(line.strip())

def readFile(gz,inFile):
 if(gz):
  f = gzip.open(os.path.abspath(inFile), 'r')
  return f
 else:
    return open(inFile)


def processRead(readAr,isPaired,unKnown,outOneName,outTwoName=None, quiet=False):
 if readAr[0].endswith('/1'):
  saveReadToFile(readAr,outOneName)
 elif readAr[0].endswith('/2'):
  saveReadToFile(readAr,outTwoName)
 else:
  saveReadToFile(readAr,unKnown)
  

def saveReadToFile(read,fileName):
 f = open(fileName, 'a') 
 f.write("\n")
 f.write("\n".join(read))


def usage(msg=None):
 if msg:
  print msg
 print __doc__
 print """\
Usage:  parseFq {opts} -i:filename.fastq{.gz} -1:read1 file -2:read2 file

Parameters:
  -i:fileName.fq               input interleaved fq file
  -1:read1.fq               read 1 output file name
  -2:read2.fq               read 2 output file name

Options:
  -gz              input is the gz compressed sequence file

"""
 sys.exit(1)


if __name__ == "__main__":
  fname = None
  outOneName = None
  outTwoName = None
  outtemplate = None
  isPaired = False
  gz = False
  isQuite = False

  for arg in sys.argv[1:]:
   if arg == '-h':
    usage()
   elif arg == '-gz':
    gz = True
   elif arg.startswith('-i'):
    fname = arg.split(":")[1]
   elif arg.startswith('-1'):
    outOneName = arg.split(":")[1]
   elif arg.startswith('-2'):
    outTwoName = arg.split(":")[1]

  if outOneName and outTwoName:
   isPaired = True
  if not fname or not outOneName or not outTwoName:
   usage()

  parseFqfiles(fname,isPaired,outOneName,outTwoName,gz,isQuite)