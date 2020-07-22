import os
import sys

filename, extension = os.path.splitext(os.path.basename(sys.argv[0]))
print(sys.argv[0])
print(filename, extension)
