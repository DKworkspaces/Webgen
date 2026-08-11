import os
from jinja2 import Environment, FileSystemLoader

def build_static_site():
    # Target the templates folder
    env = Environment(loader=FileSystemLoader('templates'))
    
    # Structure data to inject into templates
    context = {
        "site_title": "Automated Jinja2 Generator",
        "introduction": "This page was fully compiled via GitHub Actions directly into the root.",
        "steps": [
            {"phase": "Step 1", "desc": "Modify components inside /templates"},
            {"phase": "Step 2", "desc": "Push changes to your main branch"},
            {"phase": "Step 3", "desc": "GitHub Actions compiles the final workspace"}
        ]
    }
    
    # Compile template file
    template = env.get_template('index.html')
    rendered_html = template.render(context)
    
    # Save the output index.html into the root directory
    output_path = 'index.html'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(rendered_html)
        
    print(f"✅ Success: Generated site at '{output_path}'")

if __name__ == "__main__":
    build_static_site()
