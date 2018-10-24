import argparse, sys


parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('integers, ints', metavar='N', type=int, nargs='+',
                    help='an integer for the accumulator')
parser.add_argument('--sum',  action='store_const',
                    const=sum, default=max,
                    help='sum the integers (default: find the max)')

group = parser.add_mutually_exclusive_group()
group.add_argument('-v','--verbose', action='store_true')
group.add_argument('-q','--quiet', action='store_true') 

args = parser.parse_args()
print args
print args.ints
#print(args.accumulate(args.integers))

