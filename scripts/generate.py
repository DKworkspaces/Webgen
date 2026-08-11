import json
import os
import shutil
from jinja2 import Environment, FileSystemLoader

# Set up paths
template_dir = 'templates'
data_file = 'data/content.json'
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
template = env.get_template('layout.html')

# 3. Loop through array and generate each individual page
for page in pages_data:
    filename = f"{page['slug']}.html"
    output_path = os.path.join(output_dir, filename)
    
    # Pass both the specific page data and the shared navigation
    rendered_html = template.render(page=page, nav_links=nav_links)
    
    with open(output_path, 'w') as f:
        f.write(rendered_html)
    
    print(f"Generated: {output_path}")

print("All multiple pages successfully generated!")
