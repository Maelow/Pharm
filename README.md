Companies crawler
=================
(it's better if you run this in a separate virtualenv)

    pip install -r requirements.txt
    cd Pharm
    scrapy crawl --nolog -o - -t csv compendium

`--nolog` disables logging output at all
`-o -` enables output of crawled items to  `STDOUT`
`-t csv` sets the output format to Comma-Separated Values
