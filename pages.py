import os
def md(location):
    """Assembles index pages using pre-compiled components into dist/."""
    os.makedirs(location, exist_ok=True)
    
def base_template(basefile, op_loc, op_file):
    # Load master layout structure and output final production build
    base_temp = env.get_template(basefile)
    op_tg = os.path.join(op_loc, op_file)
    return base_temp, op_tg

def generate (base_temp,op_tg,content):
    with open(op_tg, 'w', encoding='utf-8') as o_f:
        o_f.write(base_temp.render(content))
    print(f"Success: Isolated page generated explicitly at: {op_tg}")





