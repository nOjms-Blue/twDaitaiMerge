import sys

from .merge import twMerge

def main():
	if len(sys.argv) >= 2:
		print(twMerge(*sys.argv[1:]))

if __name__ == "__main__":
	main()