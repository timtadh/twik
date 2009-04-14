
END_MARK = '~'
NXT_MARK = '^'
SEP_MARK = '|'
LST_MARK = '>'
REP_END = '%#001'
REP_NXT = '%#002'
REP_SEP = '%#003'
REP_LST = '%#003'

INT_MARK = '%#int'
FLT_MARK = '%#flt'

SILENT_FAIL = False

def type_error(s, t):
    if SILENT_FAIL: return s
    else: raise Exception, 'String "' + s + '" did not match type ' + t 

def syntax_error():
    if SILENT_FAIL: return None, list()
    else: raise Exception, "invalid syntax"

def mark_filter(s):
    s = str(s)
    s = s.replace(END_MARK, REP_END)
    s = s.replace(SEP_MARK, REP_SEP)
    s = s.replace(NXT_MARK, REP_NXT)
    s = s.replace(LST_MARK, REP_LST)
    return s

def int_out(i):
    if type(i) == type(int()):
        i = INT_MARK + ' ' + str(i)
    return i

def float_out(f):
    if type(f) == type(float()):
        f = FLT_MARK + ' ' + str(f)
    return f

OUT_FILTERS = [int_out, float_out, mark_filter]

def out_filter(s):
    for f in OUT_FILTERS:
        s = f(s)
    return s

def rep_filter(s):
    s = str(s)
    s = s.replace(REP_END, END_MARK)
    s = s.replace(REP_SEP, SEP_MARK)
    s = s.replace(REP_NXT, NXT_MARK)
    s = s.replace(REP_LST, LST_MARK)
    return s

def int_in(s):
    if not type(s) == type(str()): return s
    if s[:len(INT_MARK)] == INT_MARK:
        i = s[len(INT_MARK):].lstrip()
        if i.isdigit(): return int(i)
        else: return type_error(s, 'int')
    return s

def float_in(s):
    if not type(s) == type(str()): return s
    if s[:len(FLT_MARK)] == FLT_MARK:
        f = s[len(FLT_MARK):].lstrip()
        if f.replace('.', '').isdigit(): return float(f)
        else: return type_error(s, 'float')
    return s

IN_FILTERS = [rep_filter, float_in, int_in]

def in_filter(s):
    s = str(s)
    for f in IN_FILTERS:
        s = f(s)
    return s
    

def build_dict(lines):
    dictionary = {}
    x = 0
    
    while x < len(lines) and lines[x] != END_MARK:
        if lines[x][-1] == SEP_MARK:
            key = lines[x][:-1]
            
            sub_dict, unused_lines = build_dict(lines[x+1:])
            del lines[x+1:]

            if key: dictionary.update({in_filter(key):sub_dict}) 
            else: return syntax_error()
            
            if unused_lines: lines += unused_lines
        elif lines[x][-1] == LST_MARK:
            line_split = lines[x].split(SEP_MARK)
            if len(line_split) == 2: key = line_split[0]
            else: return syntax_error()
            
            l = list()
            x += 1
            while x < len(lines) and lines[x] != END_MARK:
                l.append(in_filter(lines[x]))
                x += 1
            if x >= len(lines):
                return syntax_error()
            
            dictionary.update({in_filter(key):l})
        else:
            line_split = lines[x].split(SEP_MARK)
            if len(line_split) == 2: dictionary.update({in_filter(line_split[0]):in_filter(line_split[1])})
            else: return syntax_error()
        x += 1
             
    unused_lines = lines[x+1:]
    return dictionary, unused_lines

#Pre: pass in a dictionary object, no other objects in dict except for diction and primative
#Post: returns the dictionary in advanceDDB format
    # File:
    #    Key|Value
    #    Key|
    #    Key|Value
    #    ~
    #    ~
def encode(d):
    s = ''
    keys = d.keys()
    for x in keys:
        if type(d[x]) == type({}): #if current item a dictionary object
            s += out_filter(x) + SEP_MARK + NXT_MARK
            s += encode(d[x]) #recursive call
        elif type(d[x]) == type(list()):
            s += out_filter(x) + SEP_MARK + LST_MARK + NXT_MARK
            s += NXT_MARK.join([out_filter(c) for c in d[x]])
            s += NXT_MARK + END_MARK + NXT_MARK
        else: s += out_filter(x) + SEP_MARK + out_filter(d[x]) + NXT_MARK #put key val pair in string
    s += END_MARK + NXT_MARK #end the dictionary
    return s

def decode(string):
    rawList = string.split(NXT_MARK)
    if rawList[rawList.__len__()-1] == '': del rawList[rawList.__len__()-1]
    return build_dict(rawList)[0]

#pass in valid file name for file in AdvanceDDB format return a Dictionary Obj
def openDDB(filename):
    file = open(filename)
    fileList = file.readlines()
    file.close()
    str = ''
    for x in fileList:
        str += x
    rawList = str.split(NXT_MARK)
    if rawList[rawList.__len__()-1] == '': del rawList[rawList.__len__()-1]
    return build_dict(rawList)[0]

#Pass in filename and dictionary object, returns true if successful write of
#an AdvanceDDB of the dictionary
def saveDDB(filename, dict):
    str = makeAdvanceDDB(dict)
    file = open(filename, 'w')
    file.write(str)
    file.close()
    return True

#backwards compatibility names
accessAdvanceddb = build_dict
saveAdvanceDDB = saveDDB
decodeDDB = decode
openAdvanceDDB = openDDB
makeAdvanceDDB = encode

if __name__ == '__main__':
    NXT_MARK = '\n'
    test = {1:1.2234, 1234:.9182376, 'list test':[1,2,'1123123',4,5,6,7,8,9],
            'dict test':{1:1.2234, 1234:.9182376, 'list test':[1,2,'1123123',4,5,6,7,8,9]}}
    s = encode(test)
    print test
    print s
    print test
    print decode(s)