import os
from jinja2 import Environment, FileSystemLoader

def build_site():
    # Setup Jinja2 environment
    env = Environment(loader=FileSystemLoader('templates'))
    
    # Define production output folder
    output_dir = 'dist'
    os.makedirs(output_dir, exist_ok=True)
    
    # Mock data to pass into your templates
    site_data = {
        "heading": "Hello from Jinja2 & Python!",
        "description": "This static page was automatically compiled using GitHub Actions."
    }
    
    # Render index.html
    template = env.get_template('index.html')
    output_from_parsed_template = template.render(site_data)
    
    # Save the compiled HTML file
    with open(os.path.join(output_dir, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(output_from_parsed_template)
        
    # Copy an empty .nojekyll file to prevent GitHub from running Jekyll processing
    with open(os.path.join(output_dir, '.nojekyll'), 'w') as f:
        pass

    print("Successfully built static site in /dist folder!")

if __name__ == "__main__":
    build_site()
