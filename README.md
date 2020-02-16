# Zipcracker

I first created this program for a challenge, then I decided to spend more time on it to personalize it with different options. *Zipcracker* is not optimal and there are certainly several ways to improve it.

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

With the default values:

```
DEFAULT_PREFIX          = ''
NUMSET                  = '0123456789'
CHARSET                 = 'abcdefghjiklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
DEFAULT_ALPHABET        = NUMSET + CHARSET
# Password length contains the prefix!
DEFAULT_MIN_LENGTH      = 1
DEFAULT_MAX_LENGTH      = 6
```

## Examples 

To start cracking myfile.zip on passwords of size between 1 and 6 (default values) with integers and characters:
```
python3 zipcracker.py --input myfile.zip
```

To start cracking myfile.zip on passwords of size between 3 and 5 and containing only integers:
```
python3 zipcracker.py --input myfile.zip --with-int --min 3 --max 6
```

To start cracking myfile.zip on passwords of maximum size 12 with '123abcABC' characters:
```
python3 zipcracker.py --input myfile.zip --alphabet '13abcABC' --max 12
```

To start cracking myfile.zip on passwords of maximum size 6 starting by '123' and with characters:
```
python3 zipcracker.py --input myfile.zip --prefix '123' --with-chr --max 6
```
