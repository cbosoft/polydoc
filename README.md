# POLYDOC - the polyglottal project documentation system

Picture the scenario: you're writing a server in `Python`, with the frontend handled by `javascript`. How can you document this in a consistent way? I suppose you could direct people to read the comments, but nicely formatted documentation is missing!

Enter, polydoc. You write documentation in comments (as many documentation systems do) except the system doesn't care about language (too much): your python API doc can link to the relevant javascript function and vice-versa.

Polydoc doesn't care or try to understand too much about the languages, so don't expect code traversal or anything. What it relies on is the author to write about each of the functions/methods/classes/modules as necessary. If the documentation for a function is missing? Then it's undocumented! (And won't appear in the documentation.)

# Usage

Clone this repo:
```bash
git clone git@github.com:cbosoft/polydoc
```

Run polydoc:
```bash
python -m polydoc --root path/to/your/project
```

Output will be placed in `path/to/your/project/polydoc` as a bunch of html files. Open them up in your favourite web browser!