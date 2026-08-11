import json
import os
import shutil
from jinja2 import Environment, FileSystemLoader

# Set up paths
template_dir = 'templates'
data_file = 'data/basic_pages.json'
output_dir = 'dist'  # Saving pages in a separate folder keeps the repo clean

# Ensure output directory exists and is empty
if os.path.exists(output_dir):
    shutil.rmtree(output_dir)
os.makedirs(output_dir)

# Load JSON data array
with open(data_file, 'r') as f:
    pages_data = json.load(f)

# 1. Build navigation links from the array data
nav_links = []
for p in pages_data:
    nav_links.append({
        "title": p["title"],
        "url": f"{p['slug']}.html"
    })

# 2. Setup Jinja2 environment
env = Environment(loader=FileSystemLoader(template_dir))
# 3. Loop through array and generate each individual sub-page
sub_page_template = env.get_template('layout.html')
for page in pages_data:
    filename = f"{page['slug']}.html"
    output_path = os.path.join(output_dir, filename)
    
    rendered_html = sub_page_template.render(page=page, nav_links=nav_links)
    with open(output_path, 'w') as f:
        f.write(rendered_html)
    print(f"Generated sub-page: {output_path}")

# 4. Generate the automatic index.html landing page
index_template = env.get_template('index_layout.html')
index_output_path = os.path.join(output_dir, 'index.html')

rendered_index = index_template.render(nav_links=nav_links)
with open(index_output_path, 'w') as f:
    f.write(rendered_index)
print(f"Generated landing page: {index_output_path}")
print("All files including landing page successfully generated!")
