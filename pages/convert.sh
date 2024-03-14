#/bin/bash

pandoc  --metadata=title="Dateroll" --variable=title="" -H index_header.html -c github-markdown.css  -s -f markdown -t html ../README.md  > build/index.html
pandoc  --metadata=title="Dateroll Docs" --variable=title="" -H index_header.html -c github-markdown.css  -s -f markdown -t html ../DOCS.md  > build/docs.html
pandoc  --metadata=title="Dateroll Examples" --variable=title="" -H index_header.html -c github-markdown.css  -s -f markdown -t html ../EXAMPLES.md  > build/examples.html