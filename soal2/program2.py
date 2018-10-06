#!/usr/bin/python3
import argparse

parser = argparse.ArgumentParser(description="Sort the input file and return a sorted output file ")
parser.add_argument('-i', '--input', type=str, metavar='', required=True, help="Path to the input file")
parser.add_argument('-o', '--output', type=str, metavar='', required=True, help="Path to the output file")
args = parser.parse_args()

def sort_age(input_file_path, output_file_path):
	f = open(input_file_path, 'r')
	age_data = f.read()
	f.close()

	f = open(output_file_path, 'a')
	# since we're focused on execution time, I prefer using built-in function to sorting rather make own function.
	f.writelines(map(lambda x: x+'\n', sorted(age_data.strip(' \n').split('\n'), key=int)))
	f.close()
if __name__ == '__main__':
	sort_age(args.input, args.output)