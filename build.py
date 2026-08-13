import os
import json
from jinja2 import Environment, FileSystemLoader

def render_modular_site():
    # 1. Load separated JSON files
    with open('data/header.json', 'r', encoding='utf-8') as h_file:
        header_data = json.load(h_file)
    with open('data/footer.json', 'r', encoding='utf-8') as f_file:
        footer_data = json.load(f_file)
    # 2. Setup production folders
    os.makedirs('temp', exist_ok=True)
    os.makedirs('dist', exist_ok=True)
    # 3. Setup Jinja framework environment
    env = Environment(loader=FileSystemLoader('templates'))
    # 4. Render standalone snippet into temp/header.html
    header_template = env.get_template('header.html')
    with open('temp/header.html', 'w', encoding='utf-8') as h_out:
        h_out.write(header_template.render(header_data))
    # 5. Render standalone snippet into temp/footer.html
    footer_template = env.get_template('footer.html')
    with open('temp/footer.html', 'w', encoding='utf-8') as f_out:
        f_out.write(footer_template.render(footer_data))
    print("Success: Generated individual components in temp/")

if __name__ == '__main__':
    render_modular_site()
    
