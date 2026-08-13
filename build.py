import os
import json
from jinja2 import Environment, FileSystemLoader

# Global environment runner setup pointing to templates folder
env = Environment(loader=FileSystemLoader('templates'))

def load_data_profiles():
    """Loads all JSON files needed for compilation."""
    with open('data/header.json', 'r', encoding='utf-8') as h_file:
        header_data = json.load(h_file)
    with open('data/footer.json', 'r', encoding='utf-8') as f_file:
        footer_data = json.load(f_file)
        
    return header_data, footer_data


def generate_layout_snippets(header_data, footer_data):
    """Generates raw, ready-to-use HTML blocks inside templates/temp/."""
    os.makedirs('templates/temp', exist_ok=True)
    
    # 1. Compile and save plain header snippet
    header_template = env.get_template('header.html')
    with open('templates/temp/header.html', 'w', encoding='utf-8') as h_out:
        h_out.write(header_template.render(header_data))
    # 2. Compile and save plain footer snippet
    footer_template = env.get_template('footer.html')
    with open('templates/temp/footer.html', 'w', encoding='utf-8') as f_out:
        f_out.write(footer_template.render(footer_data))

    print("Success: Standalone layout modules compiled into templates/temp/")


def generate_index_page(header_data, footer_data):
    """Assembles index pages using pre-compiled components into dist/."""
    os.makedirs('dist', exist_ok=True)
    

    # Merge contexts for the index page rendering pipeline parameters
    full_page_context = {
        **header_data,
        **footer_data,
        **index_config
    }

    # Load master layout structure and output final production build
    base_template = env.get_template('base.html')
    output_target = os.path.join('dist', index.html)
    
    with open(output_target, 'w', encoding='utf-8') as out_file:
        out_file.write(base_template.render(full_page_context))
        
    print(f"Success: Isolated index page generated explicitly at: {output_target}")


def main():
    """Main orchestrator running the operations in order."""
    # Step 1: Load all data profiles
    header_data, footer_data = load_data_profiles()
    # Step 2: Build the raw snippet dependencies first
    generate_layout_snippets(header_data, footer_data)
    # Step 3: Run the standalone page builder engine function
    generate_index_page(header_data, footer_data)


if __name__ == '__main__':
    main()
    
