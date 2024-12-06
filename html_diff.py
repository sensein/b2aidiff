from os import getenv
import os
from dotenv import load_dotenv

import json
import argparse
load_dotenv(".env", override=True)
import diff_match_patch as dmp_module

def read_files_in_directory(root_folder):
    file_contents = {}

    # Walk through the folder and all sub-folders
    for dirpath, dirnames, filenames in os.walk(root_folder):
        for filename in filenames:
            # Construct the full file path
            file_path = os.path.join(dirpath, filename)
            relative_path = os.path.join(*file_path.split("/")[1:])

            try:
                # Open the file and read its contents
                with open(file_path, 'r', encoding='utf-8') as file:
                    file_contents[relative_path] = file.read()
            except Exception as e:
                print(f"Error reading {file_path}: {e}")
    
    return file_contents

def get_diff(json1, json2):
    json_str1 = json.dumps(json1, indent=2)
    json_str2 = json.dumps(json2, indent=2)
    dmp = dmp_module.diff_match_patch()
    diffs = dmp.diff_main(json_str2, json_str1)


    # HTML Header
    if len(diffs) ==1 and diffs[0][0] ==0:
        return None 

    return dmp.diff_prettyHtml(diffs)

def filter2(json):
    # removed potential un-important changes
    filtered_json = json
    json.pop("schemaVersion", None)
    json.pop("version", None)
    json.pop("@context", None)
    return filtered_json

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Passing in 2 versions of the protocol")
   
    # Add arguments for the folder paths
    parser.add_argument("new_protocol", type=str, help="Path to the first folder")
    parser.add_argument("old_protocol", type=str, help="Path to the second folder")
    args = parser.parse_args()
    mood_protocol = read_files_in_directory(args.new_protocol)
    redcap_protocol = read_files_in_directory(args.old_protocol)

    for key in mood_protocol.keys(): # mood
        value = json.loads(mood_protocol[key])
        mood_protocol[key] = filter2(value)

    for key2 in redcap_protocol.keys(): #redcap
        value2 = json.loads(redcap_protocol[key2])
        redcap_protocol[key2] = filter2(value2)
    
    for questionnaire in mood_protocol:
        i = questionnaire.replace("/", "-")
        if questionnaire in redcap_protocol:
            diff = (get_diff(mood_protocol[questionnaire], redcap_protocol[questionnaire]))
            if diff != None:
                diff = diff.replace("&para;", "")
                if diff != "":
                    with open(f"individual-file-diffs/{i}.html", 'w') as file:
                            if diff != "":
                                file.write(diff)
        else:
            pass
                                    
                        