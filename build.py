import os
import json
from jinja2 import Environment, FileSystemLoader, Template

# Global environment runner setup pointing to templates folder
env = Environment(loader=FileSystemLoader('templates'))
# Register Python's json.loads as the 'from_json' filter
env.filters['from_json'] = json.loads

def md(location):
    """Assembles index pages using pre-compiled components into dist/."""
    os.makedirs(location, exist_ok=True)
    
def base_f(basefile):
    # Load master layout structure and output final production build
    return env.get_template(basefile)
    
def base_template(basefile, op_loc, op_file):
    # Load master layout structure and output final production build
    base_temp = base_f(basefile)
    op_tg = os.path.join(op_loc, op_file)
    return base_temp, op_tg

def generate (base_temp,op_tg,**kwargs):
    with open(op_tg, 'w', encoding='utf-8') as o_f:
        o_f.write(base_temp.render(kwargs))
    print(f"Success: Isolated page generated explicitly at: {op_tg}")


def load_json (json_file):
# Loads JSON filesneeded for compilation 
    with open(json_file, 'r', encoding='utf-8') as h_f:
        return json.load(h_f)

def load_data_profiles():
    """Loads header n footer JSON files needed for compilation."""
    hd= load_json ('data/header_footer.json')
    return hd

def generate_layout_snippets():
    """Generates raw, ready-to-use HTML blocks inside templates/temp/."""
    os.makedirs('templates/temp', exist_ok=True)
    with open('data/header_footer.json', 'r', encoding='utf-8') as h_f:
        hd= json.load(h_f)
    
    h_t= env.get_template('_nav.html')
    with open('templates/temp/nav.html', 'w', encoding='utf-8') as o_f:
        o_f.write(h_t.render(site_config=hd))
    print(f"Success: Isolated page generated explicitly at: {'templates/temp/nav.html'}")
    
    f_t= env.get_template('_footer.html')
    with open('templates/temp/footer.html', 'w', encoding='utf-8') as o_f:
        o_f.write(f_t.render(site_config=hd))
    print(f"Success: Isolated page generated explicitly at: {'templates/temp/footer.html'}")

    


def generate_page(base_file,op_loc,op_file,**kwargs):
    md(op_loc)
    bt,ot=base_template(base_file,op_loc,op_file)
    generate(bt,op_loc+"/"+op_file,**kwargs)
    
def generate_template_page(op_loc,op_file,content):
    md(op_loc)
    template = Template(content)
    generate(template,op_file)
    
def gen_headfoot():
    # Step 1: Build the raw snippet dependencies first
    generate_layout_snippets()

def set_global():
    gb= load_json ('data/global.json')
    env.globals.update(site_config=gb)
def gen_home():
    # Read the global cache directly from Jinja2's global dictionary
    hm= load_json ('data/page/home.json')
    generate_page('home.html','web','index.html', page_data=hm)
def gen_about():
    hm= load_json ('data/page/about.json')
    generate_page('about.html','web','about_us.html',hm)
def gen_contact():
    hm= load_json ('data/page/contact.json')
    generate_page('contact.html','web','contact_us.html',hm)
def gen_privacy():
    hm= load_json ('data/page/privacy.json')
    generate_page('privacy.html','web','privacy_policy.html',hm)
def gen_editorial():
    hm= load_json ('data/page/edit.json')
    generate_page('edit.html','web','editorial_policy.html',hm)
def gen_terms():
    hm= load_json ('data/page/terms.json')
    generate_page('terms.html','web','terms_conditions.html',hm)

def gen_404():
    template_content = """<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>404 Page Not Found</title><style>
        body{font-family:Helvetica,sans-serif;background-color:#f7fafc;color:#2d3748;text-align:center;padding:80px 20px}
        .container{max-width:500px;margin:0 auto;background:white;padding:40px;border-radius:8px;box-shadow:0 4px 6px rgba(0,0,0,0.05)}
        h1{font-size:3rem;margin-bottom:10px;color:#e53e3e}
        p{font-size:1.1rem;color:#4a5568;line-height:1.6}
        .url-display{font-family:monospace;background-color:#edf2f7;padding:4px 8px;border-radius:4px}
        .btn {display:inline-block;margin-top:25px;background-color:#3182ce;color:white;padding:12px 24px;text-decoration:none;border-radius:6px;font-weight:bold}
        .btn:hover { background-color: #2b6cb0; }</style>
        </head><body><div class="container"><h1>404</h1><p>Sorry, the page you are looking for does not exist.</p><p>You tried to visit: <span id="broken-url" class="url-display"></span></p><a href="/index.html" class="btn">Return to Home</a></div></body></html>"""
    generate_template_page('web','web/404.html',template_content)
    
                  
    
    

def main():
    """Main orchestrator running the operations in order."""
    gen_headfoot()
    #set_global()
    #gen_home()
    gen_404()
if __name__ == '__main__':
    main()
    
