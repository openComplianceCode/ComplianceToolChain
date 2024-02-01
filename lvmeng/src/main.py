# -*- coding: utf-8 -*-
import json
import os
import time

from pkg_resources import resource_filename
import argparse

from fossscan.atarashii import build_scanner_obj, run_scan, __version__
from scancode import api


def main():
    '''
    Calls atarashii_runner / scancode / file_diff
    '''
    # start = time.time()
    parser = argparse.ArgumentParser()
    defaultProcessed = resource_filename("src", "data/licenses/processedLicenses.csv")
    defaultJSON = resource_filename("src", "data/Ngram_keywords.json")

    parser.add_argument("-m", "--method", required=True,
                        choices=['file', 'text'],
                        help="Select scan file or text")

    parser.add_argument("inputPath", help="Specify the input file/directory path /text to scan")

    parser.add_argument("-l", "--processedLicenseList", required=False,
                        help="Specify the location of processed license list file")
    parser.add_argument("-a", "--agent_name", required=True,
                        choices=['wordFrequencySimilarity', 'DLD', 'tfidf', 'Ngram', 'scancode'],
                        help="Name of the agent that needs to be run")
    parser.add_argument("-s", "--similarity", required=False, default="CosineSim",
                        choices=["ScoreSim", "CosineSim", "DiceSim", "BigramCosineSim"],
                        help="Specify the similarity algorithm that you want."
                             " First 2 are for TFIDF and last 3 are for Ngram")
    parser.add_argument("-j", "--ngram_json", required=False,
                        help="Specify the location of Ngram JSON (for Ngram agent only)")
    parser.add_argument("-v", "--verbose", help="increase output verbosity",
                        action="count", default=0)
    parser.add_argument('-V', '--version', action='version',
                        version='%(prog)s ' + __version__)

    args = parser.parse_args()
    agent_name = args.agent_name

    return_code = 0
    if agent_name == "scancode":
        inputPath = args.inputPath
        if os.path.isfile(inputPath):
            result = api.get_licenses(inputPath)
            print(result)
        else:
            print("Error: Can not understand '" + inputPath + "'. Please enter a " +
                  "correct path or a directory")
            return_code |= 6
    else:
        method = args.method
        inputPath = args.inputPath
        similarity = args.similarity
        verbose = args.verbose
        processedLicense = args.processedLicenseList
        ngram_json = args.ngram_json

        if processedLicense is None:
            processedLicense = defaultProcessed
        if ngram_json is None:
            ngram_json = defaultJSON

        scanner_obj = build_scanner_obj(processedLicense, agent_name, similarity,
                                        ngram_json, verbose)
        if scanner_obj == -1:
            return -1

        # Determine whether file or text
        if method == 'file':
            if os.path.isfile(inputPath):
                try:
                    result = run_scan(scanner_obj, inputPath, method)
                except FileNotFoundError as e:
                    result = ["Error: " + e.strerror + ": '" + e.filename + "'"]
                    return_code |= 2
                except UnicodeDecodeError as e:
                    result = ["Error: Can not encode file '" + inputPath + "' in '" + \
                              e.encoding + "'"]
                    return_code |= 4

                result = list(result)
                result = {"licenses": result}
                result = json.dumps(result, sort_keys=False, ensure_ascii=False, indent=4)
                print(result + "\n")

            elif os.path.isdir(inputPath):
                print("[")
                printComma = False
                for dirpath, dirnames, filenames in os.walk(inputPath):
                    for file in filenames:
                        fpath = os.path.join(dirpath, file)
                        try:
                            result = run_scan(scanner_obj, fpath, method)
                        except FileNotFoundError as e:
                            result = ["Error: " + e.strerror + ": '" + e.filename + "'"]
                            return_code |= 2
                        except UnicodeDecodeError as e:
                            result = ["Error: Can not encode file '" + fpath + "' in '" + \
                                      e.encoding + "'"]
                            return_code |= 4
                        result = list(result)
                        result = {"results": result}
                        if printComma:
                            print(",", end="")
                        else:
                            printComma = True
                        print(json.dumps(result, sort_keys=False, ensure_ascii=False))
                print("]")

            else:
                print("Error: Can not understand '" + inputPath + "'. Please enter a " +
                      "correct path or a directory")
                return_code |= 6
        elif method == 'text':
            result = run_scan(scanner_obj, inputPath, method)
            result = list(result)
            result = {"Text": inputPath, "results": result}
            result = json.dumps(result, sort_keys=False, ensure_ascii=False, indent=4)
            print(result + "\n")
        else:
            print("Error: Please select method from file and text")

    # end = time.time()
    # print("useTime : %.2f" % (end - start))
    return return_code


if __name__ == '__main__':
    import sys

    sys.path.append(os.path.dirname(sys.path[0]))
    main()
