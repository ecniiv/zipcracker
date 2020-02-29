import argparse
import pyzipper
import itertools
import string
import time
import threading
import multiprocessing
from ctypes import c_char_p

# Default values
DEFAULT_PREFIX          = ''
NUMSET                  = '0123456789'
CHARSET                 = 'abcdefghjiklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
DEFAULT_ALPHABET        = NUMSET + CHARSET
# Password length contains the prefix!
DEFAULT_MIN_LENGTH      = 1
DEFAULT_MAX_LENGTH      = 6

password = multiprocessing.Value(c_char_p, "")

class ZipIt():
    def __init__(self, fzipAES, prefix, alphabet, minlength, maxlength):
        self.fzipAES    = fzipAES
        self.prefix     = prefix
        self.alphabet   = alphabet
        self.minlength  = minlength
        self.maxlength  = maxlength
        self.password   = ""
        self.manager    = multiprocessing.Manager()

    # Test to open the zip file with word as password. Return the word if success, None otherwise.
    def testing(self, word):
        print('[x] TESTING WITH ' + word)
        try:
            self.fzipAES.setpassword(word.encode())
            self.fzipAES.extractall()
            return True
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            return False

    # Return the password if it founds it, None otherwise.
    def crackit(self, length, password):
        length = length[0]
        password = password[0]
        print('[x] TESTING WITH LENGTH ' + str(length) + '')
        for chars in itertools.product(self.alphabet, repeat=length):
            word = self.prefix + ''.join(list(chars))
            result = self.testing(word)
            print("PW: " + password.value)
            #time.sleep(0.05)
            if self.password.value != "":
                print("BREAKKK")
                break
            if result == True:
                password = self.manager.Value('c', word)
                print(password.value)
                print("Password found !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                break

    def start(self):
        count_range = range(self.minlength, self.maxlength + 1)
        processes = []
        for length in count_range:
            p = multiprocessing.Process(target=self.crackit, args=([length], [password]))
            processes.append(p)
        for p in processes:
            p.start()
        for p in processes:
            p.join()
        print("pw: " + self.password.value)


# Initialize zip files input and start cracking. Print the result.
def init(input, prefix, alphabet, minlength, maxlength):
    fzipAES = pyzipper.AESZipFile(input)
    print('[x] CRACKING')
    start = time.time()
    zi = ZipIt(fzipAES, prefix, alphabet, minlength, maxlength)
    zi.start()
    end = time.time()
    done = end - start
    print('[x] Done in ' + str(done) + ' seconds')
    '''
    if (result == None):
        print("[-] No password found :(")
    else:
        print("[+] Password found: " + result)
    '''

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
    return parser

if __name__ == '__main__':
    parser      = parse_args()
    args        = parser.parse_args()
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
    if (minlength <= len(prefix)) or (maxlength <= len(prefix)):
        print('Error: verify the prefix you choose and the min and max password length.')
        parser.print_usage()
        exit(0)
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
   
