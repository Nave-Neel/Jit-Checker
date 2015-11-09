import os
import subprocess
import sys

flagged_methods = []
temp_file = "/tmp/parse.tmp"

def process_file(file_path):
        print(file_path)
        if "$" in file_path:
                file_path = file_path.replace("$", "\$")
        cmd ="javap -c " + file_path + " >| " + temp_file
        os.system(cmd)
        with open(temp_file) as f:
                processing = False
                prev_line = ""
                method_name = ""
                for line in f:
                        if not processing:
                                if "Code:" in line:     
                                        #print("Method Name" + prev_line)
                                        processing = True
                                        method_name = prev_line
                        else:
                                if line in ['\n', '\r\n'] or line == "}\n" or "Exception table" in line:
                                        #print("Offending line:" + prev_line)
                                        arr = prev_line.split(":")
                                        try:
                                                method_size = int(arr[0])
                                                if method_size > 8000:
                                                        #print(method_size)
                                                        flagged_methods.append(file_path+"::"+method_name)
                                        except:
                                                print("Exception occured at: " + prev_line)
                                        processing = False
                        prev_line = line



def search_dir(directory):
        subdirectories = os.listdir(directory)
        for root, dirs, files in os.walk(directory):
                for f in files:
                        file_path = os.path.join(root, f)
                        process_file(file_path)
                        #print("\n\n\n")


if __name__ == "__main__":
        total = len(sys.argv)
        if total != 2:
                print("Wrong number of arguments! Usage: python javap_parser.py [relative_path_to_base_dir]")
                sys.exit(1)
        # Get the arguments list 
        base_dir = sys.argv[1]
        curr_dir = os.getcwd() 
        base_dir = curr_dir + "/" + base_dir 
        search_dir(base_dir)
        for method in flagged_methods:
                print (method)
