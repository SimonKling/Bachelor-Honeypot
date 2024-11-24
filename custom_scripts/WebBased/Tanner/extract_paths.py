import os
import json
from collections import defaultdict


def extract_and_count_paths_for_each_file(input_dir, output_dir):

    os.makedirs(output_dir, exist_ok=True)


    for filename in os.listdir(input_dir):
        if filename.endswith('.json'):
            input_file_path = os.path.join(input_dir, filename)
            output_file_path = os.path.join(output_dir, f"{os.path.splitext(filename)[0]}_output.txt")

            path_count = defaultdict(int)  
            post_requests = []  

            with open(input_file_path, 'r', encoding='utf-8') as file:
                for line in file:
                    try:
                        json_obj = json.loads(line.strip())

                        if 'path' in json_obj and 'method' in json_obj:
                            path = json_obj['path']
                            path_count[path] += 1  

                            if json_obj['method'] == 'POST' and 'post_data' in json_obj:
                                post_requests.append({
                                    "path": path,
                                    "post_data": json_obj['post_data']
                                })

                    except json.JSONDecodeError as e:
                        print(f"Invalid JSON in file {filename} on this line: {line.strip()}")
                        print(f"Error: {e}")

            with open(output_file_path, 'w', encoding='utf-8') as out_file:
                out_file.write(f"Results for {filename}\n\n")

                out_file.write("Path Occurrences:\n")
                for path, count in path_count.items():
                    out_file.write(f"{path}: {count}\n")

                out_file.write("\nPOST Requests with post_data:\n")
                for post_request in post_requests:
                    out_file.write(f"Path: {post_request['path']}, Post Data: {post_request['post_data']}\n")

            print(f"Results written to {output_file_path}")


input_dir = 'tanner_files'  
output_dir = 'paths_tanner'  

extract_and_count_paths_for_each_file(input_dir, output_dir)
