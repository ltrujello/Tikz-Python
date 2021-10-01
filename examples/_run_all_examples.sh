#!/bin/bash 

# Usage: If you want to run, compile, and view all the pdfs:
#    ./_run_all_examples.sh show
# If you want to simply run the python code but not compile or view the pdfs
#   ./_run_all_examples.sh

for pyfile in `find . -name "*.py" -type f`; do
    if [ "$1" = "show" ]
    then 
        python3 $pyfile || break # Run the .py
    else
        sed -i "" "s|^tikz.show()|#tikz.show()|g" $pyfile # Comment out tikz.show(). Don't want to see the pdf.
        python3 $pyfile || break  # Run the .py
        sed -i "" "s|^#tikz.show()|tikz.show()|g" $pyfile # Uncomment tikz.show()
    fi
done