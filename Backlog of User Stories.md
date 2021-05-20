# Backlog
## User Stories

### To Do
1. As a sound designer, I want to remove redundant samples from each category
    * When the user clicks the edit button on the bucket, it will take them to a mode where they can compare and remove redundant samples
1. Users can browse more than 200 samples at a time
    * Problem: Browsers won't allow more than 200 samples to be loaded at a time so we need to preload or unload based on sample focus +/- ~10-100 samples

1. As a sound designer, I want to easily find the samples I've already categorized
    * color code categorized samples
1. Add count to export button so it reads "export 42 samples"

1. Users can click on a category button to categorize the current sample
    * focus will return to the last sample afterwards so that the user doesn't lose their place
1. Users can customize the names and shortcut keys of each category
    * Add an edit button to each bucket button, which reveals the edit mode
<!-- 1. If users give a sample more than one category, each one will prefix the exported sample -->
<!-- 1. As a sound designer, I want to keep track of the samples I have already categorized -->

1. Use JSZip on the client to zip the samples up for export

### In Progress

1. Categorized samples can be automatically renamed and downloaded by pressing the export button
    * Choose a *better* data structure and refactor for that data structure
        - 1 Array of objects for the sample list + links + src
        
    * ~~Samplenames will be prefixed with the category name and saved to the user's computer~~

1. As a patreon hustler, I need software to get out of my way to get back to making content
    * When a user categorizes a sample, the next sample is automatically focused **(need to get working with button clicks as well)**

### Done

1. Users can press tab to navigate and play samples
1. Users can load samples from their computer
1. As a sound designer, I want to easily know what shortcuts to use to categorize samples
    * Underscore first letter of category
1. Users can use the arrow keys (in addition to tab) to navigate their samples (need to fix over-indexing on linkList.length)
1. Users can categorize each sample by pressing the first letter of the category
    * Buttons are being collected instead of links