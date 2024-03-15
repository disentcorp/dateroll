#/bin/bash

cp ../logo.png /dev/null
if [[ $? = 0 ]]; then
    mkdir -p build/docs
    cp ../logo.png build
    cp ../logo.png build/docs
    cp github-markdown.css build
    cp github-markdown.css build/docs
else
    echo "ERROR: you must run this script from the pages directory."
    exit 1
fi

pandoc  --metadata=title="Dateroll" --variable=title="" -H index_header.html -c github-markdown.css  -s -f markdown -t html ../README.md  > build/index.html
pandoc  --metadata=title="Dateroll Docs" --variable=title="" -H index_header.html -c github-markdown.css  -s -f markdown -t html ../DOCS.md  > build/docs/docs.html
pandoc  --metadata=title="Dateroll Examples" --variable=title="" -H index_header.html -c github-markdown.css  -s -f markdown -t html ../EXAMPLES.md  > build/examples.html
