# Zipcracker

## Usage

```
usage: zipcracker.py [-h] --input INPUT
                     [--with-int | --with-chr | --all | --alphabet ALPHABET]
                     [--prefix PREFIX] [--min MIN] [--max MAX]

A simple program to crack zip password

optional arguments:
  -h, --help            show this help message and exit
  --input INPUT, -i INPUT
                        zip file to crack
  --with-int, -wi       use only integers
  --with-chr, -wc       use only french alphabet
  --all                 use integers and french alphabet
  --alphabet ALPHABET, -a ALPHABET
                        use integers and french alphabet
  --prefix PREFIX, -p PREFIX
                        prefix password
  --min MIN             min password length, default is 1
  --max MAX             max password length, default is 6
```
