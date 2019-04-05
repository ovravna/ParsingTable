from tabulate import tabulate
from enum import Enum
import re
from collections import OrderedDict
import sys
import os

grammar_pattern = re.compile(r"(.+?)[=-]>\|?(.+)")

def grammar(g):
    
    
    G = OrderedDict()
    def add(k, v):
        m = G.get(k, [])
        m += v
        G[k] = m
    
    for i, match in enumerate(grammar_pattern.finditer(g)):
        t, s2 = match.group(1), match.group(2)
        t = t.strip()
        
        
        s2 = [s.strip().split(" ") for s in s2.split("|")]
        add(t, s2)
        
    K = list(G.keys())
    for i in range(len(K)):
        G[i] = G[K[i]]
        del G[K[i]]

 
    
        
    
    mp = lambda s: K.index(s) if s in K else s if s != '€' else ''
    for k in G: 
        
        G[k] = [[mp(s) for s in n] for n in G[k]]
        
    
    return G, K


def first_set(G):
       
    first = dict()

    def add(k, v):
        m = first.get(k, set())
        m.add(v)
        first[k] = m
    
    def f(k):
        r = []
        
        for X in G[k]:
            
            for x in X:
                if  isinstance(x, str):                  
                    add(x, x)
                    r.insert(0, x)
                    if x == '':                     
                        add(k, x)
                        
                    else:                        
                        break
                else:
                    Z = f(x)
                
                    for x__ in {Z[i] for i in range(Z.index('') if '' in Z else len(Z))}:
                        r.insert(0, x__)
                        add(k, x__)
           
        for n in r:
            add(k, n)
        return r

    for k in G:
        
        f(k)
    return first

def follow_set(G, S, first = None):
    
    first = first or first_set(G)
    follow = dict()
    
    def add(k, v):
        m = follow.get(k, set())
        m.add(v)
        follow[k] = m
    add(S, '$')
    
    def f(A):
        
        for X in G[A]:
            
            for i, x in enumerate(X):
                if  not isinstance(x, str): 
                    n = [first.get(y, {y}) for y in X[i+1:]]        
                        
                    for y in n:
                   
                        for y_ in y:
                          
                            if y_ != '':
                                add(x, y_)
                        if '' not in y:
                            
                            break
                    
                    if len(n) == 0 or '' in n[0]:
                        for a in follow.get(A, {}):
                                    add(x, a)

    for k in G:
        f(k)
    for k in G:
    
        f(k)
    return follow

def parse_table(G, first = None, follow = None):
    first = first or first_set(G)
    follow = follow or follow_set(G, 0, first)

    M = dict()
    
    def add(N, k, F, t):
        m = M.get(N, dict())
        hm = m.get(k, set())
        hm.add((F, t))
        m[k] = hm
        M[N] = m
    def frst(a):
        frs = set()
        for x in a: 
            f = first[x]
            frs = frs.union(f)
            if '' not in f:
                break
        
        return frs - {''}
    def P(A):
        for i, X in enumerate(G[A]):
            for a in frst(X):
                add(A, a, A, i)
            for x in X:

                if isinstance(x, str):                  

                    if x == '':  
                        for b in follow[A]:                   
                            add(A, b, A, i)
                        
                    else:    
                                           
                        break
              
    for g in G:
        P(g)
    return M

def as_table(G, N, M = None, first = None, follow = None, **kwargs):
    first = first or first_set(G)
    follow = follow or follow_set(G, 0, first)
    terminals = set(n for v in first.values()  for n in v).union(set(n for v in follow.values()  for n in v))
    terminals -= {''}

    nonterminals = set(v for v in follow.keys())

    M = M or parse_table(G, first, follow)
    s = lambda s: s if s != '' else 'ε'


    z = sorted(list(terminals))
    z.reverse()
    z[4], z[3] = z[3], z[4]
    data = []
    for n in nonterminals:
        
        data2 = [N[n]]
        for t in z:
            l3 = ""
            if M.get(n) and M[n].get(t):
                
                for i, p in enumerate(M[n][t]):
                    A, x = p
                    x = "".join([s(e) if isinstance(e, str) else N[e] for e in G[A][x]])
                    if i > 0:
                        l3 += "\n"
                    l3 += ("%-2s → %-2s" % (N[A], x))
                    
                    
            
            data2.append(l3)
        data2.append("  ".join(s(c) for c in first[n]))
        data2.append("  ".join(s(c) for c in follow[n]))
        data.append(data2)
        
    return tabulate(data, headers=["NON -\nTERMINALS"] + z+["FIRST", "FOLLOW"], **kwargs)

if __name__ == "__main__":
    l = len(sys.argv) 
    fmts = ["plain" , "simple" , "github" , "grid" , "fancy_grid" , "pipe" , "orgtbl" , "jira" , "presto" , "psql" , "rst" , "mediawiki" , "moinmoin" , "youtrack" , "html" , "latex" , "latex_raw" , "latex_booktabs" , "textile"]
        
    g = """
        E -> T E'
        E' -> + T E' | € 
        T -> F T'
        T' -> * F T' | €
        F -> ( E ) | id
        """
    if l >= 2:
        arg = sys.argv[1]
        if arg in ("--help", "-h"):
            print("Give me grammar!")
            print("Like this: \n%s" % g)
            print("""€ is empty terminal
Use space (' ') as seperator in production
Seperate productions with pipe ('|') or with different arrow-productions
Any string on the left side of -> is a nonterminal
Any non-nonterminal on the rightside of -> is a terminal
            """)
            print("Third argument is style of table. Default: fancy_grid \nValid options are:")
            for i, f in enumerate(fmts): 
                if i % 12 == 11:
                    print()
                print(f, end=" ")
            print()

            exit()
        elif os.path.isfile(arg):
            with open(arg, "r") as file:
                G, N = grammar(file.read())
        elif re.match(grammar_pattern, arg):
            G, N = grammar(arg)
        
        
        fmt = 'fancy_grid'
        if l >= 3:
            if sys.argv[2] in fmts:
                fmt = sys.argv[2]
            else:
                print("Invalid table style: %s\nSee --help for valid options" % arg)
            
        
    else:
        print("""
No recognized grammar!
For more info see --help

Example parse table:""")
        G, N = grammar(g)
        
    table = as_table(G, N, tablefmt='fancy_grid')

    print(table)
