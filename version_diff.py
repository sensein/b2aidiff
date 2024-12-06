from os import getenv
from openai import OpenAI
import os
from dotenv import load_dotenv
from deepdiff import DeepDiff
import json
import argparse
load_dotenv(".env", override=True)

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
    diff = DeepDiff(json2, json1)
    return diff


def filter_json(json):
    filtered_json = json
    json.pop("schemaVersion", None)
    json.pop("version", None)
    json.pop("@context", None)
    return filtered_json

def prompt_llm(prompt):
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=getenv("OPENROUTER_API_KEY"),
    )
    completion = client.chat.completions.create(
        model="openai/gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    return completion.choices[0].message.content


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
        mood_protocol[key] = filter_json(value)

    for key2 in redcap_protocol.keys(): #redcap
        value2 = json.loads(redcap_protocol[key2])
        redcap_protocol[key2] = filter_json(value2)

    for questionnaire in mood_protocol:
        i = questionnaire.replace("/", "-")
        with open('diff.html', 'a') as file:
            if questionnaire in redcap_protocol:
                diff = (get_diff(mood_protocol[questionnaire], redcap_protocol[questionnaire]))
                if diff != {}:
                    output = prompt_llm(f"give me a human readable version of the following deepdiff, list all changes: {diff} in the following format, Added: , Changed, Removed.")
                    file.write(f"<div>  <a href='./individual-file-diffs/{i}.html'> <h3>{questionnaire}</h3> </a>")
                    file.write(f"<pre>{output}</pre> </div>")
            else:
                file.write( f"{questionnaire}  is not present in the redcap protocol")
            
            
            

        
