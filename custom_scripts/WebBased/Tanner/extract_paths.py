import json
from collections import defaultdict

def extract_and_count_paths(input_file, output_file):
    path_count = defaultdict(int) 
    post_requests = []  

    with open(input_file, 'r') as file:
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
                print(f"Invalid JSON on this line: {line.strip()}")
                print(f"Error: {e}")

    with open(output_file, 'w', encoding='utf-8') as out_file:
        out_file.write("Path Occurrences:\n")
        for path, count in path_count.items():
            out_file.write(f"{path}: {count}\n")

        out_file.write("\nPOST Requests with post_data:\n")
        for post_request in post_requests:
            out_file.write(f"Path: {post_request['path']}, Post Data: {post_request['post_data']}\n")

    print(f"Data successfully written to {output_file}")


input_file = 'do_tanner.json'  # Replace with the path to your JSON file
output_file = 'output.txt'      # Output file where the results will be written
extract_and_count_paths(input_file, output_file)
