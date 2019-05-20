#!/usr/bin/python

import sys

def code (key, val) :
    key = str(key)
    i = 0
    while True :
        if len(key) == i :
            break
        if len(key) == i + 1 :
            val = val + (int(key[i]) * 10)
            break
        if int(key[i]) < 4 :
            val = val + int(key[i + 1])
            i = i + 2
            continue
        if int(key[i]) < 7:
            val = val - int(key[i + 1])
            i = i + 2
            continue
        val = val * int(key[i + 1])
        i = i + 2
    return val

def decode (key, val) :
    key = str(key)
    i = len(key) - 1
    if len(key) % 2 == 1:
        val = val - (int(key[len(key) - 1]) * 10)
        i = i - 1
    while True :
        if i < 0 :
            break
        if int(key[i - 1]) < 4 :
            val = val - int(key[i])
            i = i - 2
            continue
        if int(key[i - 1]) < 7:
            val = val + int(key[i])
            i = i - 2
            continue
        val = int(val / int(key[i]))
        i = i - 2
    return val

def check (key) :
    key = str(key)
    if len(key) > 30 or len(key) < 4 :
        return ('key should be between 4 and 30 symbols')
    for i in key :
        if i.isalpha() == True :
            return ('only numbers are allowed in key')
        if i == '0' :
            return ('zeros in key are not allowed')
    a = {}
    a[0] = 11
    for i in range(1, (int(len(key) / 2)) + 1) :
        a[i] = code(key[(i * 2) - 2] + key[(i * 2) - 1], a[i - 1])
        y = i - 1
        while y > -1 :
            if a[y] == a[i] :
                return ('ineffective conversions between step ' + str(y + 1) + ' and ' + str(i))
            y = y - 1
    return('')
        
usage = 'Usage : ' + sys.argv[0] + ' <mode> <key> <input type> <input> <options>'

try :
    wr = False
    qu = False
    hd = False
    if len(sys.argv) > 5 :
        for i in range(len(sys.argv)-5) :
            if sys.argv[i + 5] == '-q' :
                qu = True
            if sys.argv[i + 5] == '-w' :
                wr = True
            if sys.argv[i + 5] == '-h' :
                hd = True
    if sys.argv[1] == 'h' :
        print ('Encrypting input using key as algorithm\nModes : e (encrypt) d (decrypt) h (help) c (check key)')
        print ('Input types: n (num), s (string), f (file), d (dir, recursive encryption)')
        print ('Options : -q (quiet), -w (result will be written to the input file), -h (show first 20 bytes of result)')
        print (usage)
        print ('Example : ' + sys.argv[0] + ' -e 354872 f /tmp/foo')
        sys.exit()
    if sys.argv[1] == 'c' :
        print (check(sys.argv[2]))
    if sys.argv[1] == 'e' :
        if check(sys.argv[2]) != '' :
            print ('Wrong key. Exiting')
        else :
            if sys.argv[3] == 'n' :
                num = 0
                try :
                    num = int(sys.argv[4])
                except :
                    print ('Wrong input. Exiting')
                print (code(sys.argv[2], num))
            if sys.argv[3] == 's' :
                res = ''
                for c in sys.argv[4] :
                    res = res + str(code(sys.argv[2],ord(c))) + '='
                print (res)
            if sys.argv[3] == 'f' :
                try :
                    val = open(sys.argv[4], "r")
                except :
                    print ('Could not open input file')
                    sys.exit()
                x = 0
                with open(sys.argv[4]) as f :
                    f.readlines()
                    x = f.tell()
                res = ''
                for i in range(x - 1) :
                    res = res + str(code(sys.argv[2],ord(val.read(1)))) + '='
                val.close()
                if qu == False :
                    print (res)
                if wr :
                    try :
                        val = open(sys.argv[4], 'w')
                    except :
                        print ('Could not open output file')
                    val.write(res)
                    val.write('\n')
                    val.close
    if sys.argv[1] == 'd' :
        if check(sys.argv[2]) != '' :
            print ('Wrong key. Exiting')
        else :
            if sys.argv[3] == 'n' :
                print (decode(sys.argv[2], int(sys.argv[4])))
            if sys.argv[3] == 's' :
                res = ''
                arr = sys.argv[4].split('=')
                arr.pop(len(arr) - 1)
                try :
                    for c in arr :
                        res = res + chr(decode(sys.argv[2], int(c)))
                except ValueError:
                    print ('Wrong input. Exiting')
                    sys.exit()
                print (res)
            if sys.argv[3] == 'f' :
                try :
                    val = open(sys.argv[4], "r")
                except :
                    print ('Could not open input file')
                    sys.exit()
                x = 0
                with open(sys.argv[4]) as f :
                    f.readlines()
                    x = f.tell()
                res = ''
                word = ''
                for i in range(x) :
                    b = val.read(1)
                    if b == '=' :
                        res = res + chr(decode(sys.argv[2], int(word)))
                        word = ''
                    else :
                        word = word + b
                val.close()
                if qu == False :
                    print (res)
                if wr :
                    try :
                        val = open(sys.argv[4], 'w')
                    except :
                        print ('Could not open output file')
                    val.write(res)
                    val.write('\n')
                    val.close

except IndexError: 
    print (usage)
    sys.exit()
        
