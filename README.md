We are going to automate this so you never have to minify code manually again. We will set up a workflow that watches the assets branch, minifies the code automatically, and commits it back.

This Branch we only add CSS code n JS code

The Automation Strategy

Triggers: 
Runs only on pushes to the assets branch.

Path Filters: 
Runs only when files in src/js/ or src/css/ change.

Tools: 
Uses standard npm packages (terser and clean-css-cli) without heavy frameworks.

Output: 
Saves minified files into a dist/ folder (e.g., dist/js/ and dist/css/).
