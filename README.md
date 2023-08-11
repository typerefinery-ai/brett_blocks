# brett_blocks

This is an experimental repo for containg data flow blocks for use in Type Refinery.

Each block is documented in a sub-directory, named after the block, and contains:
- Script - a python or javascript file containing the exact script to be executed in the block
- Config - a JSON file that contains the exact data needed to fill out the other config fields
- UI_Code - a HTML file that contians the javascript and HTML from the Edit part of the block
- README - a markdown file that contains the description of how the block works, and how to get the best out of it (unlike those TotalJS tossers)

The Python blocks can be loaded and tested locally. Each Script wil take imports and export a file, and so testing and glue code can be written

It is not clear yet how the HTLM code, or javascript code could be tested locally, so we are open to suggestions.

Note Poetry Install, Python v3.9