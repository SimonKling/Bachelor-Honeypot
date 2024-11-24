import os
import re
from collections import defaultdict
import matplotlib.pyplot as plt
from urllib.parse import unquote

categories = {
    'Root Path': re.compile(r'^\s*/\s*$', re.IGNORECASE),
    'Git Repository': re.compile(
        r'/\.git(?:/|$)|\.gitignore$|\.gitattributes$|/\.gitmodules$', 
        re.IGNORECASE
    ),
    'WordPress': re.compile(
        r'wordpress|/wp-(?:content|admin|includes|login|config)\b|'
        r'wp-(?:login|config|cron|signup|links-opml|trackback|comments-post)\.php|'
        r'wp-blog-header\.php|wp-settings\.php', 
        re.IGNORECASE
    ),
    'PHP related': re.compile(
        r'\.(?:php[\d]?|phar|phtml|inc|class\.php|module\.php|theme\.php)$', 
        re.IGNORECASE
    ),
    '.exe Files': re.compile(
        r'\.(?:exe|apk|dll|sys|ps1|bat|msi|com)$', 
        re.IGNORECASE
    ),
    'Bootstrap': re.compile(
        r'bootstrap|/bootstrap(?:\.min)?\.css|/bootstrap\.js|/bootstrap-theme\.css', 
        re.IGNORECASE
    ),
    'Sensitive Paths': re.compile(
        r'/(?:admin|administrator|user|login|signin|signup|register|auth|dashboard|console|download)\b|'
        r'\.(?:env|aws|bak|old|swp|orig)$|'
        r'\b(config|credentials|password|database|db|dump|backup|shell|passwd|shadow|htpasswd)\b|'
        r'phpmyadmin|wp-config\.php|mysql|/assets/|actuator|cgi-bin',
        re.IGNORECASE
    ),
    'Harmless Paths': None
}

excluded_paths = {
    '/favicon.ico', '/robots.txt', '/info.php', '/version',
    '/index.php', '/1.zip', '/a', 
}

botpoke_paths = set()
with open('../full_list_PokeBot_URLs.txt', 'r') as botpoke_file:
    for line in botpoke_file:
        path = line.strip()
        if path and path not in excluded_paths:
            botpoke_paths.add(path)

def categorize_uri(uri, count, category_counts):
    uri = unquote(uri.strip())
    if categories['Root Path'].search(uri):
        category_counts['Root Path'] += count
        return  
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

input_dir = 'paths_tanner'
output_dir = 'plots_output'
os.makedirs(output_dir, exist_ok=True)

for filename in os.listdir(input_dir):
    if filename.endswith('.txt'):
        file_path = os.path.join(input_dir, filename)
        category_counts = defaultdict(int)
        with open(file_path, 'r', encoding='utf-8') as txtfile:
            for line in txtfile:
                parts = line.split(':')
                if len(parts) == 2:
                    uri = parts[0].strip()
                    count_part = parts[1].strip()
                    try:
                        count = int(count_part)
                    except ValueError:
                        continue
                    categorize_uri(uri, count, category_counts)
        sorted_categories = sorted(category_counts.items(), key=lambda x: x[1], reverse=True)
        categories_list = [item[0] for item in sorted_categories]
        counts_list = [item[1] for item in sorted_categories]
        plt.figure(figsize=(10, 6))
        bars = plt.bar(categories_list, counts_list, color='skyblue')
        plt.xlabel('Categories')
        plt.ylabel('Counts')
        plt.title(f'Category Counts')
        plt.xticks(rotation=45)
        plt.tight_layout()
        for bar, count in zip(bars, counts_list):
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width() / 2.0, yval + 1, count, ha='center', va='bottom')
        plot_path = os.path.join(output_dir, f"{os.path.splitext(filename)[0]}_category_counts.png")
        plt.savefig(plot_path)
        plt.close()
