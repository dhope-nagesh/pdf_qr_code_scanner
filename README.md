# Help

```bash
$ python main.py --help                                                                                                  (kind-kind/default)
usage: main.py [-h] -i INPUT_FOLDER [-o OUTPUT_FOLDER] [-d]

Scan pdfs

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_FOLDER, --input-folder INPUT_FOLDER
                        Where all pdf files take place.
  -o OUTPUT_FOLDER, --output-folder OUTPUT_FOLDER
                        Put unrecognized files here
  -d, --deep-search     Deep search

```

# Example

```bash
python main.py -i /Users/nageshdhope/Downloads/file 
```

```bash
python main.py -i /Users/nageshdhope/Downloads/file -d
```

```bash
 python main.py -i /Users/nageshdhope/Downloads/file -o /Users/nageshdhope/Downloads/tests
```

```bash
 python main.py -i /Users/nageshdhope/Downloads/file -o /Users/nageshdhope/Downloads/tests -d
```