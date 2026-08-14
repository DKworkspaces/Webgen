In short, the assets branch workflow handles your frontend performance optimization like this:

Input File Locations
  CSS Files:
    src/css/*.css
  JavaScript Files:
    src/js/*.js
  Brotli Compression 
    Target Files: 
    ./web/js and ./web/css (targets .js and .css files inside these folders)
  Images: 
    src/media/clean/*.{jpg,jpeg,png,tiff}

Output Folders
  Minified CSS: 
    web/css/
  Minified JS: 
    web/js/
  Brotli Compressed Files: 
    web/js/ and web/css/ (creates .js.br and .css.br files inline)
  WebP Images: 
    media/images/

Trigger Paths (Events)
  The workflow does not use path-based filtering (such as on: push: paths:). Instead, it runs based on the following triggers:
  Scheduled Trigger: 
    Runs automatically every day at midnight (0 0 * * *) via a cron job.
  Manual Trigger: 
    Can be started manually at any time using the workflow_dispatch button in your GitHub repository actions tab.




Input File Locations
  Trigger Target Files:
    src/images/** (any changes here trigger the workflow)
  Processing Files: 
    The exact target files are handled internally by the custom script clean_images.py.

Output Folders
  Cleaned Files Destination: 
    src/clean/images/* (this is the directory pattern tracked for commits)

Trigger Paths (Events)
  Path-Based Trigger: 
    Automatically runs on a push event, but only when changes occur inside the src/images/** directory.
  Manual Trigger: 
    Can be started manually at any time using the workflow_dispatch event in the Actions tab.




Triggers: 
  It stays asleep until you push changes specifically to your raw src/js/ or src/css/ folders.

Minifies: 
  It instantly runs Node.js utilities (terser for JavaScript and clean-css for style sheets) to compress your asset files.

Optimizes: 
  It strips out all heavy developer comments, spaces, and formatting to make file sizes as small as possible.

Saves Separate: 
  It keeps your original source files completely clean and safe inside src/, while saving the optimized versions into dist/js/ and dist/css/.

Commits: 
  It pushes the updated production-ready .min.js and .min.css files back to your repository automatically without creating a loop.
