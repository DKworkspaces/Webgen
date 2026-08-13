In short, the html branch workflow automates static site generation like this:


Triggers:
  It stays asleep until you push changes specifically to the data/ or templates/ folders.

Compiles: 
  It spins up Python and Jinja2 to automatically inject your JSON data (data/global.json) into your HTML templates.

Filters: 
  It intelligently ignores partial layout files (like _base.html), ensuring only actual pages are generated.

Minifies: 
  It processes the output with Node.js to strip comments and whitespaces, optimizing the HTML for production.

Saves: 
  It dumps the final, compressed webpages into your website/ folder and commits them back to the repository safely.
