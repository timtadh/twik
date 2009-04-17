#!/usr/bin/python

# This file includes implementations of several algorithms useful in database dependency theory. 
# These alogorithms can be used to improve your database design. All algorithms are based
# off of Jeffery Ullman's "Principles of Database and Knowledge-Base Systems" 1988. citations 
# included where appropriate.

# # see algorithm 7.1 on page 388 of:
# Ullman, Jeffery D. "Principles of Database and Knowledge-Base Systems" Computer Science Press.
#   Rockville, Maryland. 1988.
def closure(x, F):
    x = set([i for i in x])
    x_l = None
    F = [(set([i for i in f[0]]), set([i for i in f[1]])) for f in list(F)]
    while x != x_l:
        x_l = set(x)
        for f in F:
            if f[0] <= x: x = x | f[1]
    
    return x

# # computes the closure of x with respect to the decomposition of R
# # see algorithm 7.3 on page 400 of:
# Ullman, Jeffery D. "Principles of Database and Knowledge-Base Systems" Computer Science Press.
#   Rockville, Maryland. 1988.
def closure_G(x, F, p): 
    x = set([i for i in x])
    x_l = None
    p = [set([i for i in r]) for r in p]
    #F = [(set([i for i in f[0]]), set([i for i in f[1]])) for f in list(F)]
    while x != x_l:
        x_l = set(x)
        for r in p:
            x = x | (closure(x&r, F) & r)
    
    return x
    
# # see algorithm 7.3 on page 400 of:
# Ullman, Jeffery D. "Principles of Database and Knowledge-Base Systems" Computer Science Press.
#   Rockville, Maryland. 1988.
def dependencies_preserved(F, p):
    for f in F:
        Z = closure_G(f[0], F, p)
        Y = set([i for i in f[1]])
        #print f[0], ''.join(Y), ''.join(Z), Y <= Z
        if not (Y <= Z): return False
    return True

def all_perm(s, arr=None):
    if not arr: arr = list()
    if len(s) == 1:
        arr.append(s)
    else:
        arr = all_perm(s[:-1], arr)
        new_arr = list(arr)
        for i in arr: 
            new_arr.append(i + s[-1])
        new_arr.append(s[-1])
        arr = new_arr
    return arr

def compute_keys(U, F):
    lefts = set()
    attrs_in_F = set()
    for f in list(F):
        l = set([i for i in f[0]])
        r = set([i for i in f[1]])
        for a in f[0]: lefts.add(a)
        for a in U:
            if a in l or a in r: attrs_in_F.add(a)
    known_primes = ''.join(list(U - attrs_in_F))
    
    possible = all_perm(''.join([i for i in lefts]))
    possible.sort()
    
    actual = list()
    for p in possible:
        p = p + known_primes
        #print p, closure(p, F)
        if closure(p, F) == U:
            to_del = list()
            dont_add = False
            for i, a in enumerate(actual):
                if set(p) < set(a): 
                    to_del.append(a)
                elif set(a) < set(p):
                    dont_add = True
                    break
            for i in to_del: actual.remove(i)
            if not dont_add: actual.append(p)
            
    return actual

def print_matrix(m):
    print ' '*(len(m)+2),
    for i in xrange(len(m[0])):
        print ' '*(7-len(str(i))) + str(i),
    print '\n', '-'*(len(m[0])+1)*7 + '-'*(len(m)+1)
    
    for i, r in enumerate(m):
        print  ' '*((len(m)+1)-len(str(i))) + str(i) + '|',
        for c in r:
            c = str(c)
            print ' '*(7-len(c)) + c,
        print
    print


class a(object):
    def __init__(self, j): self.j = j
    def __repr__(self): return str(self)
    def __str__(self): return 'a_' + str(self.j)
    def __hash__(self): return hash(self.j)
    def __eq__(self, b): return hash(self) == hash(b)
    def __ne__(self, b): return hash(self) != hash(b)

class b(object):
    def __init__(self, i, j): 
        self.i = i
        self.j = j
    def __repr__(self): return str(self)
    def __str__(self): return 'b_' + str(self.i) + ',' + str(self.j)
    def __hash__(self): return hash((self.i, self.j))
    def __eq__(self, b): return hash(self) == hash(b)
    def __ne__(self, b): return hash(self) != hash(b)

# # see algorithm 7.2 on page 394 of:
# Ullman, Jeffery D. "Principles of Database and Knowledge-Base Systems" Computer Science Press.
#   Rockville, Maryland. 1988.
def lossless_join(R, F, p):
    
    def matrices_equal(a, b):
        if b == None: return False
        if a == None: return False
        
        for i, x in enumerate(a):
            for j, y in enumerate(x):
                if y != b[i][j]: return False
        return True
    
    F = [(tuple([i for i in f[0]]), tuple([i for i in f[1]])) for f in list(F)]
    R_map = dict([(attr, i) for i, attr in enumerate(R)])
    
    #print R
    m = [[0 for n in xrange(len(R))] for k in p]
    
    for i, r in enumerate(p):
        #print r
        for j, attr in enumerate(R):
            #print attr, attr in r
            if attr in r: m[i][j] = a(j)
            else: m[i][j] = b(i,j)
        #print
    
    
    #print_matrix(m)
    m_l = None
    
    while not matrices_equal(m, m_l):
        m_l = [[o for o in n] for n in m]
        for f in F:
            X = [R_map[attr] for attr in f[0]]
            Y = [R_map[attr] for attr in f[1]]
            for i, r in enumerate(m):
                for i2, r2, in enumerate(m):
                    match = True
                    for attr in X:
                        if r[attr] != r2[attr]: 
                            match = False
                            break
                    if match:
                        for y in Y:
                            if type(r[y]) == a:
                                #print r[y], r2[y]
                                r2[y] = r[y]
                            elif type(r2[y]) == a:
                                #print r[y], r2[y]
                                r[y] = r2[y]
        #print_matrix(m)
    for r in m:
        lossless = True
        for c in r:
            if type(c) != a: lossless = False
        if lossless: return True
    return False

def test(U, F, p):
    print 'U:', U
    print 'F:', F
    print 'p:', p
    print 'keys: ', compute_keys(U, F)
    print 'lossless join: ', lossless_join(U, F, p)
    print 'dependencies preserved: ', dependencies_preserved(F, p)
    print

if __name__ == '__main__':
    
    U = set('CTHRSG')
    F = [('C', 'T'), ('HR', 'C'), ('HT', 'R'), ('CS', 'G'), ('HS', 'R')]
    p = ('CT', 'CHR', 'THR', 'CSG')
    test(U, F, p)
    
    #U = set('BOISQD')
    #F = [('S', 'D'), ('I', 'B'), ('IS', 'Q'), ('B', 'O')]
    #p = ('ISQ', 'SD', 'IO', 'IB')
    #key = 'IS'
    #test(U, F, p)
    
    #U = set('STVCPD')
    #F = [('V', 'SCT'), ('SD', 'PV')]
    #p = ('DVT', 'SDC', 'SDPV')
    ##p = ('VC', 'VS', 'SDP', 'SDV', 'ST')
    #test(U, F, p)
    #U = set('BOISQD')
    #F = [('S', 'D'), ('I', 'B'), ('IS', 'Q'), ('B', 'O')]
    #p = ('ISQ', 'SD', 'IO', 'IB')
    #test(U, F, p)
    
    
    #U = set('ISQ')
    #F = [('IS', 'Q')]
    #test(U, F, p)
    
    #U = set('SD')
    #F = [('S', 'D')]
    #test(U, F, p)
    
    #U = set('IO')
    #F = [('I', 'I')]
    #test(U, F, p)
    
    
    #U = set('IB')
    #F = [('I', 'B')]
    #test(U, F, p)
    #U = set([i for i in 'ABCD'])
    
    #F = [('B', 'C'), ('D', 'A')]
    #p = ('BC', 'AD')
    #test(U, F, p)
    
    #F = [('AB', 'C'), ('C', 'A'), ('C', 'D')]
    #p = ('ACD', 'BC')
    #test(U, F, p)
    
    #F = [('A', 'BC'), ('C', 'AD')]
    #p = ('ABC', 'AD')
    #test(U, F, p)
    
    #F = [('A', 'B'), ('B', 'C'), ('C', 'D')]
    #p = ('AB', 'ACD')
    #test(U, F, p)
    
    
    #F = [('A', 'B'), ('B', 'C'), ('C', 'D')]
    #p = ('AB', 'AD', 'CD')
    #test(U, F, p)
    
    #U = set([i for i in 'ABCDEG'])#H0123456789IJKLMNOPQ'])
    #F = set([('AB', 'C'), ('AC', 'B'), ('AD', 'E'), ('B', 'D'), ('BC', 'A'), ('E', 'G')])#,
            ## ('0123', 'J'), ('K', 'L'), ('H', '34567890')])
    #p = ('ABC', 'BD', 'ADE', 'EG')
    
    #print 'U:', U
    #print 'F:', F
    #print 'p:', p
    
    #print 'keys: ', compute_keys(U, F)
    
    #print 'lossless join: ', lossless_join(U, F, p)
    #print 'dependencies preserved: ', dependencies_preserved(F, p)
    
    #p = ('AB', 'BC', 'ABDE', 'EG')
    #print
    #print 'p:', p
    #print 'lossless join: ', lossless_join(U, F, p)
    #print 'dependencies preserved: ', dependencies_preserved(F, p)
    
    #p = ('ABC', 'ACDE', 'ADG')
    #print
    #print 'p:', p
    #print 'lossless join: ', lossless_join(U, F, p)
    #print 'dependencies preserved: ', dependencies_preserved(F, p)
