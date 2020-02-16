import argparse
import pyzipper
import itertools
import string
import time

# Default values
DEFAULT_PREFIX          = ''
NUMSET                  = '0123456789'
CHARSET                 = 'abcdefghjiklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
DEFAULT_ALPHABET        = NUMSET + CHARSET
# Password length contains the prefix!
DEFAULT_MIN_LENGTH      = 1
DEFAULT_MAX_LENGTH      = 6

# Return the password if it founds it, None otherwise.
def crack(fzip, fzipAES, prefix, alphabet, minlength, maxlength):
    count_range = range(minlength, maxlength + 1)
    for length in count_range:
        print('[x] TESTING WITH LENGTH ' + str(length) + '')
        for chars in itertools.product(alphabet, repeat=length):
            word = prefix + ''.join(list(chars))
            print('[x] TESTING WITH ' + word)
            try:
                fzipAES.setpassword(word.encode())
                fzipAES.extractall()
                return word
            except:
                pass
    return None

# Initialize zip files input and start cracking. Print the result.
def init(input, prefix, alphabet, minlength, maxlength):
    fzip = zipfile.ZipFile(input)
    fzipAES = pyzipper.AESZipFile(input)

    print('[x] CRACKING')
    start = time.time()
    result = crack(fzip, fzipAES, prefix, alphabet, minlength, maxlength)
    end = time.time()
    done = end - start
    print('[x] Done in ' + str(done) + ' seconds')
    if (result == None):
        print("[-] No password found :(")
    else:
        print("[+] Password found: " + result)

# Initialize the arguments.
def parse_args():
    parser = argparse.ArgumentParser(description='A simple program to crack zip password')
    parser.add_argument('--input', '-i', action='store', type=str, required=True, help='zip file to crack')
    alphabet = parser.add_mutually_exclusive_group(required=False)
    alphabet.add_argument('--with-int', '-wi', action='store_true', required=False, help='use only integers')
    alphabet.add_argument('--with-chr', '-wc', action='store_true', required=False, help='use only french alphabet')
    alphabet.add_argument('--all', action='store_true', required=False, help='use integers and french alphabet')
    alphabet.add_argument('--alphabet', '-a', action='store', type=str, required=False, help='use integers and french alphabet')
    parser.add_argument('--prefix', '-p', action='store', type=str, required=False, help='prefix password')
    parser.add_argument('--min', action='store', type=int, required=False, help='min password length, default is ' + str(DEFAULT_MIN_LENGTH))
    parser.add_argument('--max', action='store', type=int, required=False, help='max password length, default is ' + str(DEFAULT_MAX_LENGTH))
    return parser.parse_args()

if __name__ == '__main__':
    args        = parse_args()
    prefix      = DEFAULT_PREFIX
    alphabet    = DEFAULT_ALPHABET
    minlength   = DEFAULT_MIN_LENGTH
    maxlength   = DEFAULT_MAX_LENGTH

    if args.min != None:
        minlength = args.min
    if args.max != None:
        maxlength = args.max
    if args.prefix != None:
        prefix = args.prefix
        minlength = minlength - len(prefix)
        maxlength = maxlength - len(prefix)
    if args.with_int:
        alphabet = NUMSET
    elif args.with_chr:
        alphabet = CHARSET
    elif args.all:
        alphabet = NUMSET + CHARSET
    elif args.alphabet:
        alphabet = args.alphabet
    else:
        alphabet = DEFAULT_ALPHABET

    init(args.input, prefix, alphabet, minlength, maxlength)
