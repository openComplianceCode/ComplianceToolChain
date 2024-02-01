
import argparse
import json
import sys
import os
from source.sourceFind import Source_file
sys.path.append(os.path.dirname(sys.path[0]))


def commn():
    '''
    Calls source file find
    '''
    parser = argparse.ArgumentParser()

    parser.add_argument("-m", "--method", required=True,
                        choices=['list', 'cp'],
                        help="Select list or cp")
    
    parser.add_argument("path", help="Specify the repo path to find")

    parser.add_argument("--cpPath", required=False, help="Specify the cp path")

    args = parser.parse_args()
    method = args.method

    if method == 'list':
        source_file = Source_file()
        result = source_file.find_source_files(args.path)
        jsonRe = json.dumps(result)
        print(jsonRe + "\n")
    else:
        source_file = Source_file()
        result = source_file.cp_source_files(args.path, args.cpPath)
        jsonRe = json.dumps(result) 
        print(jsonRe + "\n")
    

if __name__ == '__main__':
    commn()