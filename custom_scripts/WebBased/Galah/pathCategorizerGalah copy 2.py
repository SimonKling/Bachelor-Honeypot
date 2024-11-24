import csv
import re
from collections import defaultdict
import matplotlib.pyplot as plt

categories = {
    'Git Repository': re.compile(r'\.git', re.IGNORECASE),
    'WordPress': re.compile(r'wordpress|/wp-', re.IGNORECASE),
    'PHP related': re.compile(r'\.php', re.IGNORECASE),
    '.exe Files': re.compile(r'\.exe$|\.apk$', re.IGNORECASE),
    'Sensitive Paths': re.compile(r'admin|assets|password|user|login|\.env|config|\.aws|\.', re.IGNORECASE),
    'Harmless Paths': None  
}

category_counts = defaultdict(int)

botpoke_paths = set()
with open('full_list_PokeBot_URLs.txt', 'r') as botpoke_file:
    for line in botpoke_file:
        path = line.strip()
        if path:  
            botpoke_paths.add(path)

def categorize_uri(uri, count):
    if uri in botpoke_paths:
        category_counts['Botpoke'] += count
        return  

    matched = False

    for category, pattern in categories.items():
        if pattern is not None and pattern.search(uri):
            category_counts[category] += count
            matched = True
            break  
    if not matched:
        category_counts['Other'] += count

with open('outputdo.csv', 'r', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if not row or row.get('Request Path', '').strip().startswith('#'):
            continue

        uri = row.get('Request Path', '').strip()
        count_part = row.get('Count', '1').strip()  # Default to '1' if 'Count' column is missing

        try:
            count = int(count_part)
        except ValueError:
            # If count is not a valid integer, skip this row
            continue

        # Categorize the URI
        categorize_uri(uri, count)

# # Process .txt file with URI and counts
# with open('output.txt', 'r', encoding='utf-8') as txtfile:
#     for line in txtfile:
#         # Split each line by the colon to separate the URI and the count
#         parts = line.split(':')
#         if len(parts) == 2:
#             uri = parts[0].strip()
#             count_part = parts[1].strip()

#             try:
#                 count = int(count_part)
#             except ValueError:
#                 # If count is not a valid integer, skip this line
#                 continue

#             # Categorize the URI
#             categorize_uri(uri, count)

print("Category Counts:")
for category, count in category_counts.items():
    print(f"{category}: {count}")

sorted_categories = sorted(category_counts.items(), key=lambda x: x[1], reverse=True)
categories_list = [item[0] for item in sorted_categories]
counts_list = [item[1] for item in sorted_categories]

plt.figure(figsize=(10, 6))
bars = plt.bar(categories_list, counts_list, color='skyblue')
plt.xlabel('Categories')
plt.ylabel('Counts')
plt.title('URI Category Counts')
plt.xticks(rotation=45)
plt.tight_layout()

for bar, count in zip(bars, counts_list):
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2.0, yval + 1, count, ha='center', va='bottom')

plt.savefig('uri_category_counts.png')

plt.show()
