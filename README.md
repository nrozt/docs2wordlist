# docs2wordlist

Simple scripts for wordlist creation from swaggers and Postman collections. Can extract URLs, headers and query parameters.

Usage:

```
usage: swagger2wordlist.py [-h] -i INPUT [-o OUTPUT] [-m] [-q]
                           [-op OUTPUT_PARAMS] [-ope] [-oh OUTPUT_HEADERS]
                           [-ohe]

DESC

options:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Path to input file
  -o OUTPUT, --output OUTPUT
                        Path to URLs output file. Use "-" to print to stdin
  -m, --methods         Add methods to URLs
  -q, --query-params    Add query parameters to URLs
  -op OUTPUT_PARAMS, --output-params OUTPUT_PARAMS
                        Path to parameters output file. Use "-" to print to
                        stdin
  -ope                  Add example values to parameters output file
  -oh OUTPUT_HEADERS, --output-headers OUTPUT_HEADERS
                        Path to headers output file. Use "-" to print to stdin
  -ohe                  Add example values to headers output file

```

