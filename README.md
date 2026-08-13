In short, the assets branch workflow handles your frontend performance optimization like this:


Triggers: 
  It stays asleep until you push changes specifically to your raw src/js/ or src/css/ folders.

Minifies: 
  It instantly runs Node.js utilities (terser for JavaScript and clean-css for style sheets) to compress your asset files.

Optimizes: 
  It strips out all heavy developer comments, spaces, and formatting to make file sizes as small as possible.

Saves Separate: 
  It keeps your original source files completely clean and safe inside src/, while saving the optimized versions into website/js/ and website/css/.

Commits: 
  It pushes the updated production-ready .min.js and .min.css files back to your repository automatically without creating a loop.
