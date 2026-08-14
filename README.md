In short, the html branch workflow automates static site generation like this:




Input File Locations
  Jinja2 Templates Directory:
    templates/ (ignores files starting with an underscore, like _*)
  Context Data File:
    data/global.json
    
Output Folders
  Production HTML Directory:
    website/ (files are rendered and minified directly inside this folder)

Trigger Paths (Events)
  Path & Branch Trigger:
    Automatically runs on a push event, but only if the push is to the html branch and changes occur in either the templates/** or data/** directories.
  Manual Trigger:
    Can be started manually at any time using the workflow_dispatch button in your GitHub UI.




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
