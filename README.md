The Automation Strategy

Triggers: 
Runs only on pushes to the assets branch.

Path Filters: 
Runs only when files in src/js/ or src/css/ change.

Tools: 
Uses standard npm packages (terser and clean-css-cli) without heavy frameworks.

Output: 
Saves minified files into a dist/ folder (e.g., dist/js/ and dist/css/).
