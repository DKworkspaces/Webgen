def generate_index_page(header_data, footer_data):
    """Assembles index pages using pre-compiled components into dist/."""
    os.makedirs('dist', exist_ok=True)
    

    # Merge contexts for the index page rendering pipeline parameters
    full_page_context = {
        **header_data,
        **footer_data,
    }

    # Load master layout structure and output final production build
    base_template = env.get_template('base.html')
    output_target = os.path.join('dist', 'index.html')
    
    with open(output_target, 'w', encoding='utf-8') as out_file:
        out_file.write(base_template.render(full_page_context))
        
    print(f"Success: Isolated index page generated explicitly at: {output_target}")
