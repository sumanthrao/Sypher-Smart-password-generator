import math
import random
import os
import datetime
from entropy import PasswordStrength
# GLOBAL VARIABLES

seq = []
times = 2
symbol = '#'
dt = None

# Set this variable to True if wanna debug
DEBUG = False

# setting the seed for generating the random number to be the process id
seed = os.getpid()
random.seed(seed)

def print_sequence(l):
    for i in l:
        print(l, end = "\t")
        print()

def debug(smth):
    if(DEBUG):
        print(smth)

def gimme_special_symbol():
    special_symbols = list(range(33, 48))
    special_symbols.extend(list(range(58, 65)))
    special_symbols.extend(list(range(91, 95)))
    special_symbols.extend(list(range(123, 127)))
    #debug("Special symbols : " + str(special_symbols))
    debug("No. of special symbols = " + str(len(special_symbols)))
    x = special_symbols[random.randint(0, (len(special_symbols) - 1))]
    debug("x = " + str(x))
    return chr(x)

def getNextChar(c, forward):
    if(c.isalpha()):
        if(forward):
            if(ord(c) in list(range(65, 91))):
                if((ord(c) + 1) > 90):
                    return chr(65)
            elif(ord(c) in list(range(97, 123))):
                if((ord(c) + 1) > 122):
                    return chr(97)
            return(chr(ord(c) + 1))
        else:
            if(ord(c) in list(range(65, 91))):
                if((ord(c) - 1) < 65):
                    return chr(90)
            elif(ord(c) in list(range(97, 123))):
                if((ord(c) - 1) < 97):
                    return chr(122)
            return(chr(ord(c) - 1))
    elif(c.isdigit()):
        if(forward):
            return str((int(c) + 1) % 10)
        else:
            if(int(c) - 1 > 0):
                return str((int(c) - 1))
            return(str(9))
    return(c)

import string
digs = string.digits + string.ascii_letters


def int2base32(x, base = 32):
    if x < 0:
        sign = -1
    elif x == 0:
        return digs[0]
    else:
        sign = 1

    x *= sign
    digits = []

    while x:
        digits.append(digs[int(x % base)])
        x = int(x / base)

    if sign < 0:
        digits.append('-')

    digits.reverse()
    return ''.join(digits)

def base32toint(x):
    i = 0
    x = x[::-1]

    convTable = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v')
    ans = 0

    for j in x:
        ans += pow(32, i) * (convTable.index(j))
        i += 1

    return ans

# ------------------------------------------------- <RULES> -------------------------------------------------

def Rule1(passwd):
    '''
    Alternate Characters Increment Decrement
    Example - hello -> idmkp
    '''
    debug("Rule1")
    new_pass = ""
    for i in range(len(passwd)):
        if(i % 2 == 0):
            new_pass += getNextChar(passwd[i], True)
        else:
            new_pass += getNextChar(passwd[i], False)
    debug(new_pass)
    debug("#*#*#*#*#*#*#*#*#*#*#*#*#*#*#")
    return new_pass

def Rule2(passwd):
    '''
    Take successive character of every character
    Example - hello -> ifmmp
    '''
    debug("Rule2")
    new_pass = ''.join(list(map(lambda x: getNextChar(x, True), list(passwd))))
    debug(new_pass)
    debug("#*#*#*#*#*#*#*#*#*#*#*#*#*#*#")
    return new_pass

def Rule3(passwd):
    '''
    Take previous character of every character
    Example - hello -> gdkkn
    '''
    debug("Rule3")
    new_pass = ''.join(list(map(lambda x: getNextChar(x, False), list(passwd))))
    debug(new_pass)
    debug("#*#*#*#*#*#*#*#*#*#*#*#*#*#*#")
    return new_pass


def Rule4(passwd):
    '''
    Take successive character of every alternate character
    Example - hello -> iemlp
    '''
    debug("Rule4")
    def f(i):
        if(i % 2 == 0):
            return getNextChar(passwd[i], True)
        else:
            return passwd[i]

    new_pass = ''.join([f(i) for i in range(len(passwd))])
    debug(new_pass)
    debug("#*#*#*#*#*#*#*#*#*#*#*#*#*#*#")
    return new_pass

def Rule5(passwd):
    '''
    Take previous character of every alternate character
    Example - hello -> gekln
    '''
    debug("Rule5")
    def f(i):
        if(i % 2 == 0):
            return getNextChar(passwd[i], False)
        else:
            return passwd[i]
    new_pass = ''.join([f(i) for i in range(len(passwd))])
    debug(new_pass)
    debug("#*#*#*#*#*#*#*#*#*#*#*#*#*#*#")
    return new_pass

def Rule6(passwd):
    '''
    Take successive character of every character at position
    indicated by your random number sequence
    '''
    debug("Rule6")
    my_seq = []
    for i in seq:
        my_seq.append(i % len(passwd))

    def f(i):
        if(i + 1 in my_seq):
            return getNextChar(passwd[i], True)
        else:
            return passwd[i]

    new_pass = ''.join([f(j) for j in range(len(passwd))])
    debug(new_pass)
    debug("#*#*#*#*#*#*#*#*#*#*#*#*#*#*#")
    return new_pass

def Rule7(passwd):
    '''
    Take previous character of every character at position
    indicated by your random number sequence
    '''
    debug("Rule7")
    my_seq = []
    for i in seq:
        my_seq.append(i % len(passwd))
    def f(i):
        if(i + 1 in my_seq):
            return getNextChar(passwd[i], False)
        else:
            return passwd[i]
    new_pass = ''.join([f(i) for i in range(len(passwd))])
    debug(new_pass)
    debug("#*#*#*#*#*#*#*#*#*#*#*#*#*#*#")
    return new_pass

def Rule8(passwd):
    '''
    Replace characters at even places by a particular symbols/alphabets/number - Easy
    Example - hello ->  h@l@o  (Replacing even places by symbol @)
    '''
    debug("Rule8")
    '''
    p = list(passwd)
    p[::2] = [symbol] * (len(passwd)//2)
    new_pass = ''.join(p)
    '''
    new_pass = ""
    for i in range(len(passwd)):
        if(i % 2 == 0):
            new_pass += symbol
        else:
            new_pass += passwd[i]
    debug(new_pass)
    debug("#*#*#*#*#*#*#*#*#*#*#*#*#*#*#")
    return new_pass

def Rule9(passwd):
    '''
    Replace characters at odd places by a particular symbols/alphabets/number - Easy
    Example - hello ->  h@l@o  (Replacing even places by symbol @)
    '''
    debug("Rule9")
    '''
    p = list(passwd)
    p[1::2] = [symbol] * (len(passwd)//2)
    new_pass = ''.join(p)
    '''
    new_pass = ""
    for i in range(len(passwd)):
        if(i % 2 != 0):
            new_pass += symbol
        else:
            new_pass += passwd[i]
    debug(new_pass)
    debug("#*#*#*#*#*#*#*#*#*#*#*#*#*#*#")
    return new_pass

def Rule10(passwd):
    '''
    change the order of Characters

    Example - hello

    the order sequence we generate is 132 -> What does this sequence mean??
    So character at postion 1 goes to position 3
    character at position 3 goes to position 2
    character at position 2 goes to position 1

    so hello becomes elhlo
    '''
    debug("Rule10")
    seq2 = list(map(lambda x: ((x - 1)%(len(passwd))), seq))
    new_pass = list(passwd)

    i = 1
    copy = new_pass[seq2[i - 1]]
    while(i != 0):
        copy2 = new_pass[seq2[i]]
        new_pass[seq2[i]] = copy
        debug(new_pass)
        copy = copy2
        i = (i + 1) % len(seq2)
    new_pass[seq2[i]] = copy

    debug(''.join(new_pass))
    debug("#*#*#*#*#*#*#*#*#*#*#*#*#*#*#")
    return ''.join(new_pass)

def Rule11(passwd):
    '''
    reverse the password
    '''
    debug("Rule11")

    new_pass = passwd[::-1]

    debug(new_pass)
    debug("#*#*#*#*#*#*#*#*#*#*#*#*#*#*#")
    return new_pass

def Rule12(passwd):
    '''
    replicate password
    '''
    debug("Rule12")

    new_pass = passwd * times

    debug(new_pass)
    debug("#*#*#*#*#*#*#*#*#*#*#*#*#*#*#")
    return new_pass

def Rule13(passwd):
    '''
    palindromify
    '''
    debug("Rule13")

    new_pass = passwd + passwd[::-1]

    debug(new_pass)
    debug("#*#*#*#*#*#*#*#*#*#*#*#*#*#*#")
    return new_pass

def Rule14(passwd):
    '''
    add a symbol and palindromify
    '''
    debug("Rule14")

    new_pass = passwd + symbol + passwd[::-1]

    debug(new_pass)
    debug("#*#*#*#*#*#*#*#*#*#*#*#*#*#*#")
    return new_pass

def Rule15(passwd):
    '''
    replicate and then palindromify
    '''
    debug("Rule15")
    new_pass = passwd * times

    debug(new_pass + new_pass[::-1])
    debug("#*#*#*#*#*#*#*#*#*#*#*#*#*#*#")

    return new_pass + new_pass[::-1]

def Rule16(passwd):
    '''
    replicate, add a special symbol and then palindromify
    '''
    debug("Rule16")
    new_pass = passwd * times

    debug(new_pass + symbol + new_pass[::-1])
    debug("#*#*#*#*#*#*#*#*#*#*#*#*#*#*#")

    return new_pass + symbol + new_pass[::-1]

'''
def Rule17(passwd):

    delete chars at position indicated by users unique sequence

    return ''.join(passwd[i] for i in range(len(passwd)) if i+1 not in seq)
'''

def Rule17(passwd):
    '''
    The random number which we give to the user.....we can increment so many characters by that number

    Example : hello
    Random Sequence generated for this user for this password = 135

    h gets incremented by 1
    e gets incremented by 3
    l gets incremented by 5

    hello -> ihqlo
    '''
    debug("Rule17")
    new_pass = list(passwd)

    my_seq = []
    for i in seq:
        my_seq.append(i % len(passwd))

    i = 0
    for j in my_seq:
        for k in range(j):
            #print(i)
            new_pass[i % len(new_pass)] = getNextChar(new_pass[i % len(new_pass)], True)
        i = i + 1

    debug(''.join(new_pass))
    debug("#*#*#*#*#*#*#*#*#*#*#*#*#*#*#")

    return ''.join(new_pass)
    return passwd

def Rule18(passwd):
    '''
    surround the password by the symbol
    hello with symbol $ becomes $hello$
    '''
    debug("Rule18")

    new_pass =  symbol + passwd + symbol

    debug(new_pass)
    debug("#*#*#*#*#*#*#*#*#*#*#*#*#*#*#")
    return new_pass

def Rule19(passwd):
    """
    user enters a multiword password
    my company is amazing -> this is too long!
    mycoisam              -> perfect! just the initial two letters
    mcia                  -> if its more than 5 words long
    """
    debug("Rule19")
    debug("#*#*#*#*#*#*#*#*#*#*#*#*#*#*#")
    return passwd

def Rule20(passwd):
    '''
    A list of the most rarely used  characters are
    appended to increase entropy
    '''
    debug("Rule20")
    l = ["|" , "^" , "~" , "!" , "%" , "#", "(", ")"]

    passwd += l[seq[0] % len(l)]

    debug(passwd)
    debug("#*#*#*#*#*#*#*#*#*#*#*#*#*#*#")

    return passwd

def Rule21(passwd):
    '''
    Replace chars like s with $ and so on...
    '''
    debug("Rule21")

    def add_val(dicti, key, value):
        dicti[key] = value

    dicti = {}
    add_val(dicti, "s", "$")
    add_val(dicti, "E", "3")
    add_val(dicti, "g", "9")
    add_val(dicti, "a", "@")
    add_val(dicti, "o", "0")
    add_val(dicti, "H", "#")
    add_val(dicti, "G", "6")
    add_val(dicti, "l", "/")
    add_val(dicti, 'S', "$")
    add_val(dicti, 'A', "4")
    add_val(dicti, 'i', "!")
    add_val(dicti, "D", "|)")

    debug(dicti)

    for i in passwd:
        if i in dicti:
            passwd = passwd.replace(i, dicti[i])

    debug(passwd)
    debug("#*#*#*#*#*#*#*#*#*#*#*#*#*#*#")

    return passwd

def Rule22(passwd):
    '''
    Insert the length of the string in the
    password
    '''
    debug("Rule22")

    value = len(passwd)
    #index = random.randint(1, len(passwd) - 1)
    index = ((max(seq) + min(seq)) // 2)
    index = index % value
    myString = passwd[ :index] + str(value) + passwd[index : ]

    debug(myString)
    debug("#*#*#*#*#*#*#*#*#*#*#*#*#*#*#")
    return myString

def Rule23(passwd):
    '''
     Turn alternate chars to caps and small
    '''
    debug("Rule23")
    temp = ""
    i = 0
    for character in passwd:
        if((i % 2) == 0):
            if(character.isalpha() and character.isupper()):
                temp += character.lower()
            elif(character.isalpha()):
                temp += character.upper()
            else:
                temp += character
        else:
            temp += character
    debug(temp)
    debug("#*#*#*#*#*#*#*#*#*#*#*#*#*#*#")
    return temp

def Rule24(passwd):
    '''
    replace two inferred indices with the
    sum of the digits of theur ascii value
    '''
    debug("Rule24")
    val = ord(passwd[seq[0] % len(passwd)])
    val = str(val)
    a = (sum(list(map(int, str(val))))) % 10
    passwd = passwd.replace(passwd[(seq[0] % len(passwd))], str(a))
    val = ord(passwd[seq[1] % len(passwd)])
    val = str(val)
    a = (sum(list(map(int, str(val))))) % 10
    passwd = passwd.replace(passwd[(seq[1] % len(passwd))], str(a))

    debug(passwd)
    debug("#*#*#*#*#*#*#*#*#*#*#*#*#*#*#")
    return passwd

def Rule25(passwd):
    '''
    input = original string,two int values a and b,
    a and b better be connnected with
    user sequence to enhance remembaribilty
    output=passwd1+2=3
    '''
    debug("Rule25")
    a = seq[1]
    b = seq[2]
    value = seq[0] % 4
    if(value == 1):
        operator = "+"
        result = a + b
    elif(value == 2):
        operator = "-"
        result = a - b
    elif(value == 3):
        operator = "*"
        result = a * b
    else:
        operator = "/"
        result = a / b

    debug(passwd + str(a) + operator + str(b) + "=" + str(result))
    debug("#*#*#*#*#*#*#*#*#*#*#*#*#*#*#")

    return passwd + str(a) + operator + str(b) + "=" + str(result)

def Rule26(inp_str):
    '''
    adding something between the words
    (ex - "the!cat~is(out_of/the;box")
    - there is an array with all the special chrs ,
    the order in which they are applied is infered from
    user sequence !
    '''
    debug("Rule26")
    chrs = ['!','@','%','$','#','^','&','_','~']
    l = inp_str.strip()
    l1 = inp_str.split(" ")
    l2 = []
    for i in range(0, len(l1)):
        l2.append(l1[i])
        l2.append(chrs[seq[i % len(seq)] % 9])

    out_str = "".join(l2)

    debug(out_str)
    debug("#*#*#*#*#*#*#*#*#*#*#*#*#*#*#")

    return out_str

def Rule27(inp_str):
    '''
    adding a smiley at the end of the string ,
    the smiley is inferred from the seq again
    '''
    debug("Rule27")
    smileys = [':(',':)',':P',':D',':p',':d',':o','*_*','o_o','^.^',':|']
    num = sum(seq)
    out = inp_str + smileys[num % len(smileys)]

    debug(out)
    debug("#*#*#*#*#*#*#*#*#*#*#*#*#*#*#")

    return out

def Rule28(inp_str):
    '''
    swapping cases at indices mentioned by the seq
    '''
    debug("Rule28")
    new = list(inp_str)
    for i in seq:
        new[i % len(inp_str)] = inp_str[i % len(inp_str)].swapcase()

    out = "".join(new)

    debug(out)
    debug("#*#*#*#*#*#*#*#*#*#*#*#*#*#*#")

    return out

# Check this function --- Introducing Gibberish characters
def Rule29(inp_str):
    '''
    depending on the seq , either the odd indices
    or the even indices are either incremented or decremented
    by sum(seq)%3
    '''
    debug("Rule29")
    chrs = list(inp_str);
    a = sum(seq) % 3

    if(sum(seq) % 2 == 0):
        for i in range(0, len(chrs)):
            if(i % 2 == 0):
                chrs[i] = chr(33+(ord(chrs[i]) + a)%(126-33))
            else:
                chrs[i] = chr(33+(ord(chrs[i]) - a)%(126-33))
    else:
        for i in range(0, len(chrs)):
            if(i % 2 == 0):
                chrs[i] = chr(33+(ord(chrs[i]) - a)%(126-33))
            else:
                chrs[i] = chr(33+(ord(chrs[i]) + a)%(126-33))

    out = "".join(chrs)

    debug(out)
    debug("#*#*#*#*#*#*#*#*#*#*#*#*#*#*#")

    return out

def Rule30(inp_str):
    '''
    adding all the ascii's of chrs in the inp_str
    and appending the equivalent character of the
    ascii number obtained
    '''
    debug("Rule30")

    chrs = list(inp_str)
    s = 0

    for i in range(0, len(chrs)):
        s = s + ord(chrs[i])

    chrs.append(chr(33 + (s % (126-33))))
    out = "".join(chrs)

    debug(out)
    debug("#*#*#*#*#*#*#*#*#*#*#*#*#*#*#")

    return out

def Rule31(inp_str):
    '''
    condenses consecutive same characters
    into countCharacter
    '''
    debug("Rule31")
    chrs = list(inp_str)
    out = []
    count = 1
    i = 0

    while(i < len(chrs)):
        while((i + 1) < len(chrs) and chrs[i] == chrs[i+1]):
            count += 1
            i += 1

        if(count > 1):
            out.append(str(count))

        out.append(chrs[i])
        count = 1
        i += 1

    out = "".join(out)

    debug(out)
    debug("#*#*#*#*#*#*#*#*#*#*#*#*#*#*#")

    return out

def Rule32(inp_str):
    '''
    interchanging the two halfs of the myString
    shahid -> hidsha
    '''
    debug("Rule32")
    chrs = list(inp_str)
    half = chrs[0 : int(len(chrs)/2)]
    half_2 = chrs[int(len(chrs)/2) : ]

    out = half_2 + half
    out = "".join(out)

    debug(out)
    debug("#*#*#*#*#*#*#*#*#*#*#*#*#*#*#")

    return out

def Rule33(inp_str):
    '''
    adding 1 to first chr's ascii , 2 to the second and so on..
    '''
    debug("Rule33")
    chrs = list(inp_str)

    for i in range(0, len(chrs)):
        chrs[i] = chr(33+(ord(chrs[i]) + i)%(126-33))

    out = "".join(chrs)

    debug(out)
    debug("#*#*#*#*#*#*#*#*#*#*#*#*#*#*#")

    return out

def Rule34(inp_str):
    '''
    introducing the current system date-time
    into the password , at indices inferred from the user-sequence
    '''
    global dt
    debug("Rule34")

    chrs = list(inp_str)
    dt = str(datetime.datetime.now())
    dt = dt.strip()
    dt = dt.split(" ")
    st = str(dt[1])
    ins = st.split(":")
    ins[2] = ins[2][0:4]
    j = 0

    for i in seq:
        chrs.insert(i % len(chrs), ins[j % 3])
        j += 1

    out = "".join(chrs)
    debug(out)
    debug("#*#*#*#*#*#*#*#*#*#*#*#*#*#*#")

    return out

def Rule35(inp_str):
    '''
    Replacing certain characters by thier sound
    '''
    debug("Rule35")

    d = { 'a': "yEh",
          'e': "eH",
          'i': "4i!",
          'o': "0Hh",
          'u': "y0U",
          'y': "whAi!",
          'r': "aRr",
          's': "YaS$",
          't': "TeA!!",
          'w': "d0ubleU"
          }
    chrs = list(inp_str)

    for i in range(len(chrs)):
        if(chrs[i] in d.keys()):
            chrs[i] = d[chrs[i]]

    out = "".join(chrs)

    debug(out)
    debug("#*#*#*#*#*#*#*#*#*#*#*#*#*#*#")
    return out

# ------------------------------------------------- </RULES> ------------------------------------------------

def main():
    global seq
    global times
    global symbol
    rules = ['Shit', Rule1, Rule2, Rule3, Rule4, Rule5, Rule6, Rule7, Rule8, Rule9, Rule10, Rule11, Rule12, Rule13, Rule14, Rule15, Rule16, Rule17, Rule18, Rule19, Rule20, Rule21, Rule22, Rule23, Rule24, Rule25, Rule26, Rule27, Rule28, Rule29, Rule30, Rule31, Rule32, Rule33, Rule34, Rule35]
    print("\n\t\tSMART PASSWORD GENERATOR\n\n  1 - Generate a password\n  2 - Log IN\n  3 - Exit\n\n  ::  ", end = "")
    option = int(input())
    if(option == 1):
        print("\n\t\tTHE PASSWORD GENERATOR\n\n")
        user_pass = input("  Enter some password you can remember (It can be phrase too)\n\n  : ")

        # We give a random number sequence to the user indicating the positions at which
        # tweaking should be done to the base password incase that rule is applied to the password

        # The length the sequence is limited to be 3 - 7
        user_sequence_length = (random.randint(3, random.randint(3, 7)))

        times = (user_sequence_length % 3) + 1

        symbol = gimme_special_symbol()

        # We now generate the sequence of random numbers
        seq = [random.randint(1, len(user_pass)) for i in range(user_sequence_length)]

        debug("user pass = " + user_pass)
        debug("user_sequence = " + str(seq))
        debug("times = " + str(times))
        debug("symbol = " + str(symbol))

        # debug(Rule10(user_pass, user_sequence))
        # How many rules to apply for this user?

        # Generate random number of random numbers!!

        num_rules = (random.randint(5, random.randint(5, 8)))

        l = [random.randint(1, 35) for i in range(num_rules)]
        debug("l = " + str(l))

        def map_func(x):
            if(len(str(x)) == 1):
                return '0' + str(x)
            else:
                return str(x)

        l1 = list(map(map_func, l))
        debug("l1 = " + str(l1))
        num = ''.join(l1)
        debug(num)

        to_remember = int2base32(int(num))

        print("\n\nRemember this shit !! --> ", to_remember, end = '\n\n')



        # l = [31, 6, 31, 7, 28, 30, 29]
        # Cascade apply the rules
        ends = user_pass

        #l = [6, 10, 11, 19]
        #times = 4
        for i in l:
            ends = rules[i](ends)

        ends = Rule18(ends)

        print("\n\nGENERATED PASSWORD --> ", ends, end = '\n\n')
        strength = PasswordStrength()
        print("Entropy of your base_password", user_pass, "=", strength.calculate_entropy(user_pass))
        print("Entropy of your generated password", ends, "=", strength.calculate_entropy(ends))

    elif(option == 2):
        print("\n\t\tLOG IN\n\n")
        base_pass = input("  Enter the base password\n\n  : ")
        secret_code = input("\n  Enter the secret code\n\n  : ")
        print()

        ruleset = base32toint(secret_code)
        debug("Rule Set : " + str(ruleset))

        ruleset = str(ruleset)

        rules_to_apply = []
        i = 0
        if(len(ruleset) % 2 != 0):
            if(i == 0):
                rules_to_apply.append(int(ruleset[i]))
                i += 1

        while(i < len(ruleset)):
            rules_to_apply.append(int(ruleset[i: i + 2]))
            i += 2

        debug("list of rules to apply : " + str(rules_to_apply))

        ends = base_pass

        for i in rules_to_apply:
            ends = rules[i](ends)

        ends = Rule18(ends)

        print("\n\nYour password --> ", ends, end = '\n\n')


    elif(option == 3):
        print("\n\t\tTHANK YOU FOR USING THE APPLICATION.....UNTIL NEXT TIME...\n\n")
        exit(0)

if __name__ == "__main__":
    while(1):
        main()
