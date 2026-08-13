import os
import json
from jinja2 import Environment, FileSystemLoader

def render_modular_site():
    # 1. Load separated JSON files
    with open('data/header.json', 'r', encoding='utf-8') as h_file:
        header_data = json.load(h_file)
    with open('data/footer.json', 'r', encoding='utf-8') as f_file:
        footer_data = json.load(f_file)
    
    # 2. Setup production folders and Jinja environment
    env = Environment(loader=FileSystemLoader('templates'))
    os.makedirs('dist', exist_ok=True)
    

    # 3. RENDER READY-TO-USE HEADER INTO TEMP/
    header_template = env.get_template('header.html')
    compiled_header = header_template.render(header_data)
    with open('templates/temp/header.html', 'w', encoding='utf-8') as h_out:
        h_out.write(compiled_header)

    # 4. RENDER READY-TO-USE FOOTER INTO TEMP/
    footer_template = env.get_template('footer.html')
    compiled_footer = footer_template.render(footer_data)
    with open('templates/temp/footer.html', 'w', encoding='utf-8') as f_out:
        f_out.write(compiled_footer)
    print("Success: Generated individual components in temp/")

if __name__ == '__main__':
    render_modular_site()
    
