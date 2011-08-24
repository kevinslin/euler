import logging                      
import math
import pickle     
import operator
import os                                                           

from counters import Counter #custom data structure to keep track of counts


LOG_FORMAT = '[%(levelname)s] %(asctime)s: %(message)s'
logging.basicConfig(format = LOG_FORMAT, level = logging.DEBUG, datefmt = '%H:%m.%S', filename="/tmp/simplelog.log", filemode="a+") 
sl = logging.getLogger("simplelog")


def cache(func, *args):    
    """
    Put expensive calculatinos in cache on file that can be retrieved even after 
    program has terminated
    @param:
    obj - object to be cached    
    value - name of object      
    @return:
    return value 
    args - optional arguments given to the object    
    # >>> a = binary_search(1, 12, 1)
    # >>> cache_put(a, [1, 12, 1])     
    >>> cache(binary_search, 1, 12, 1) #doctest: +NORMALIZE_WHITESPACE
    3        
    >>> cache(binary_search, 2, 12, 1) #doctest: +SKIP
    3
    """          
    sl.debug("========\nin cache")
    sl.debug("obj: %s" % str(func))
    cache_index = hash(str(func.func_name) + str(list(args))) #hash is function name + values    
    sl.debug("index: %s" % str(cache_index))                                                
    #Check if file is in cache
    if (os.path.exists(".cache/"+str(cache_index))):
        sl.debug("found item in cache")
        with open(".cache/"+str(cache_index), "r") as fh:
            r = pickle.load(fh)
            #sl.debug("item: %s" % str(r))
            return r
    else:          
        sl.debug("putting item in cache")          
        r = func(*args)   
        sl.debug("function result: %s" % str(r))
        with open(".cache/"+str(cache_index), "w") as fh:   
            pickle.dump(r, fh, pickle.HIGHEST_PROTOCOL)                          
        return r                                                                                        

def clear_cache():
    """
    Get rid of all itmes in the cache
    @param:
    #TODO: keep - list of items to keep
    """                                
    files = os.listdir(".cache")
    for f in files:
        os.remove(".cache/" + f)

def cache_put(obj, key):
    """
    Put an object into the cache
    @param:
    obj - a python object
    key - key to retrieve object
    """
    cache_index = hash(str(key))
    with open(".cache/"+str(cache_index), "w") as fh:
        pickle.dump(obj, fh, pickle.HIGHEST_PROTOCOL)
    return cache_index
    
        
def cache_get(key): 
    """
    Get object from cache
    @param:
    key - the key to fetch object by
    """
    cache_index = hash(str(key))
    if (os.path.exists(".cache/"+str(cache_index))):
        with open(".cache/"+str(cache_index)) as fh:
            return pickle.load(fh)
    else:    
        return False

def binary_search(a, b, target):         
    """                            
    Perform binary search on input with two starting values
    @param:     
    a - lower bound starting value
    b - upper bound starting value
    target - target length
    @return:
    result of binary search   
    >>> r1 = binary_search(1, 9, 2) 
    Traceback (most recent call last):
        ...                                      
    Exception: Range too small
    >>> binary_search(3, 12, 1)
    Traceback (most recent call last):
        ...                                      
    Exception: Range too small
    >>> binary_search(1, 12, 2) #doctest: +SKIP 
    9
    >>> binary_search(1, 100, 2) #doctest: +SKIP 
    9
    >>> binary_search(1, 100000, 2) #doctest: +SKIP 
    9
    >>> binary_search(1, pow(10, 5), 3) #doctest: +SKIP 
    31
    """     
    sl.debug("===========\nin binary search:\n a:%i, b:%i, target:%i" % (a, b, target))          
    offset = ''
    for i in xrange(target):
        offset = offset + str(9)            
    offset = int(offset)    
        
    m = int(math.ceil(((a+b)/2.0)))
    epsilon=0.000001
    r_a = pow(a, 2) - offset
    r_b = pow(b, 2) - offset
    r_m = pow(m, 2) - offset    
    if (r_a * r_b >= 0):        
        raise Exception("Range too small")
    else:
        return binary_search_helper(a, b, offset)    
        
def binary_search_helper(a, b, target):
    """
    Helper to binary_search
    @param:
    a - lower bound
    b - upper bound
    target - ideal value
    """                
    sl.debug("in binary search helper:\n a:%i, b:%i" % (a, b))          
    m = int(math.ceil(((a+b)/2.0)))
    epsilon=0.000001
    r_a = pow(a, 2) - target
    r_b = pow(b, 2) - target
    r_m = pow(m, 2) - target         
    sl.debug("results; a:%i, b:%i, m: %i" %(r_a, r_b, r_m))    
    if (abs(m) <= epsilon): #since we want webM to be between 0 and epsilon, we put absolute values around webM
        return m       
    else:                  
        if (r_a * r_b > 0):        #best possible answer
            return b       
        else:
            if (r_a * r_m) < 0: 
                if (m == b):    #close enough answer                    
                    return a
                return binary_search_helper(a, m, target)
            else:                  
                if (b == m):
                    return a
                return binary_search_helper(m, b, target)

def change_key(old_dict, new_key):
    """
    Change key of dictionary with a list values
    >>> d = {1:{"foo":1, "bar":3, "foobar":5},2:{"foo":3, "bar":4, "foobar":5}}
    >>> change_key(d, "foo") #doctest: +SKIP
    {1:[{"foo":1, "bar":3,"foobar":5}],3:[{"foo":3, "bar":4, "foobar":5}]}
    """
    new_dict = {}
    for k in old_dict:
        key = old_dict[k][0][new_key]
        value = old_dict[k]
        try:
            new_dict[key].extend(value)
        except KeyError:
            new_dict[key] = []
            new_dict[key].extend(value)
    return new_dict
################################################################################                 
def gen_squares(size_limit=5):
    """
    Generate a list of squares whose size does not exc'aeed size_limit
    @param:
    size_limit - upper boundary of square length
    @return:
    a list of perfect squares           
    >>> gen_squares(2) #doctest:+NORMALIZE_WHITESPACE
    [1, 4, 9, 16, 25, 36, 49, 64,  81]
    >>> gen_squares(3)
    [1, 4, 9, 16, 25, 36, 49, 64, 81, 100, 121, 144, 169, 196, 225, 256, 289, 324, 361, 400, 441, 484, 529, 576, 625, 676, 729, 784, 841, 900, 961]
    """   
    size_cur = 0                                         
    p_squares = []
    acc = 1       
     
    limit = str(9)
    for i in xrange(size_limit - 1):
        limit = limit + str(9)        
    limit = int(limit)        
    while True:                       
        p_square = pow(acc, 2)
        if p_square > limit:
            break             
        elif (p_square % pow(10,14)) == 0:
            print (p_square)
        p_squares.append(p_square)
        acc += 1       
    return p_squares       #while loop goes one digit too far

def process_entry(entry):
    """
    Given an entry, get lenght, value and hash of number of common sequences  
    @param:
    entry - either a string or a number
    @return:
    a dictionary with:
    length - length of entry
    value - the real value of the entry
    hash - hash of count of unique symbols in entry
    hash_all - hash of count & value of unique symbols in entry
    >>> a = process_entry(11122)
    >>> b = process_entry(33355)
    >>> a['hash'] == b['hash']
    True
    >>> a['value']
    11122
    >>> a['length'] == b['length']
    True
    >>> a['hash'] 
    '23'
    >>> c = process_entry("cat")
    >>> d = process_entry(123)
    >>> c['hash'] == d['hash']
    True
    >>> c['length']
    3
    >>> e = process_entry("kitty")
    >>> f = process_entry("92133")
    >>> e2 = process_entry("ttiky")
    >>> e['hash'] == f['hash']
    True
    >>> e['hash_all'] == e2['hash_all']
    True
    >>> g = process_entry(99887652)
    >>> h = process_entry("WRITER")    
    >>> g['hash'] != h['hash']
    True
    >>> i = process_entry("cat")
    >>> j = process_entry("tic")
    >>> i['hash_all'] == j['hash_all']
    False
    >>> i['hash'] == j['hash']
    True
    >>> k = process_entry("made")
    >>> l = process_entry("dame")
    >>> k['hash_all'] == l['hash_all']
    True
    >>> m = process_entry(8649)
    >>> n = process_entry("HATE")
    >>> m['hash'] == n['hash']
    True
    """            
    c = Counter()
    entry_clean = str(entry)
    
    length = len(entry_clean)    
    
    for i in entry_clean:
        #print(i)
        c.incrementCount(i, 1)
    
    out = ''
    hash_key_and_value = ''

    for i in sorted(c.values()):    #get number of occurences of each number
        out += str(i)
    for i in sorted(c.items()):
        hash_key_and_value += str(i)

    return {"length":length, "value":entry, "hash":out, "hash_all":hash(hash_key_and_value)}    

def process_entries(entries, absolute_hash = True):
    """
    Proces a list of entries and return result as list sorted by length
    @param:
    entries - a list of numbers
    apply_filter - only get entries with more than 2 occurences 
    @return:                    
    a dictionary of processed entries 
    >>> p_num = process_entries(gen_squares(size_limit=4), absolute_hash = False)
    >>> p_word = process_entry("CARE")
    >>> get_value_for_word(p_word, p_num)[1]['value'] #doctest: +SKIP
    9802

    """ 
    sl.debug("in process entries with values")
    c = Counter()
    out = {}    #dict of prcessed entries keyed by hash               
    for i in entries:
        if isinstance(i, basestring):
            i = i.strip('"')
        p_entry = process_entry(i)
        #out.append(p_entry)        	    
        if (absolute_hash):
            c.incrementCount(p_entry['hash_all'], 1)
            try:
                out[p_entry['hash_all']].append(p_entry) 
            except KeyError:
                out[p_entry['hash_all']] = []                     
                out[p_entry['hash_all']].append(p_entry)                                       
        else:
            c.incrementCount(p_entry['hash'], 1)
            try:
                out[p_entry['hash']].append(p_entry) 
            except KeyError:
                out[p_entry['hash']] = []                     
                out[p_entry['hash']].append(p_entry)                                       
    #get only anagrams
    valid = filter(lambda x: operator.itemgetter(1)(x) >= 2, c.iteritems())
    clean = [i[0] for i in valid]
    for i in out.keys():
        if i not in clean:
            sl.debug("removing {i}".format(**locals()))
            out.pop(i)
    return out                 

def get_value_for_word(p_word, p_num):
    """
    Given a processed word, find the maximum perfect square
    @param:
    p_word - a processed word       
    p_num - a dict of processed numbers
    @return:
    a tuple containing the word and the value
    
    >>> p_word = process_entry("CARE")
    >>> p_word2 = process_entry("RACE")
    >>> p_num = process_entries(gen_squares(4), absolute_hash = False)
    >>> get_value_for_word([p_word, p_word2], p_num)[1]
    9216
    >>> p_word = process_entry("ON")
    >>> p_word2 = process_entry("NO")
    >>> p_num = process_entries(gen_squares(4), absolute_hash = False) 
    >>> get_value_for_word([p_word, p_word2], p_num) #this should lead to a keyerror
    0
    """  
    if isinstance(p_word, basestring):
        p_word = process_entry(p_word)
    try:
        valid = p_num[p_word[0]['hash']]
    except KeyError:
        return 0
    sorted_valid = sorted(valid, key=lambda x: x['value'], reverse= True)
    word1 = p_word[0]['value']
    word2 = p_word[1]['value']
    sl.info("in getting value for word with words {word1}, {word2}".format(**locals()))
    if (len(p_word) == 2):
        return get_max(word1, word2, sorted_valid)
    else:
        word3 = p_word[2]['value']
        max1 = get_max(word1, word2, sorted_valid)
        max2 = get_max(word1, word3, sorted_valid)
        max3 = get_max(word2, word3, sorted_valid)
        import pdb
        pdb.set_trace()
        return max([max1,max2,max3])

        #max_word_value = max(valid, key = lambda x: x['value'])

def get_max(word1, word2, sorted_valid):
    """
    Get max value between two processed words. Return the max_value or 0 if the proper value is not found.
    """
    squares = cache_get("squares") #all square numbers of length 11 or less, precomputed in solve()
    try:
        for i in sorted_valid:
            num_value = i['value']
            mapper_dict = {}
            for letter_index,num in enumerate(str(num_value)): #map every letter to its corresponding number
                mapper_dict[word1[letter_index]] = num
            
            num_value2 = ''
            for letter in word2:
                num_value2 += mapper_dict[letter]
            sl.info("got num_values: {num_value} and {num_value2}".format(**locals())) 
            if (num_value2[0] == '0'): #no leading zeroes
                continue
            if int(num_value2) in squares:  #there exists a valid anagram for this letter combination
                return (word1, num_value) 
            else:
                continue
    except (IndexError, KeyError):
        sl.info("could not find word in hash list")
        return 0
    sl.info("could not find matching number pair")
    return 0

def solve():
    """
    Solve euler
    """ 
    sol = ''
    d_values = {}
    counter = Counter()    
    max_value = 0
    with open("words.txt") as fh:
        text = fh.read()
        text = text.split(",")

    p_words = process_entries(text)

    squares = cache(gen_squares, 11)
    cache_put(squares, "squares") #used later in get_value_for_words, a little hackish though 
    p_num = cache(process_entries, squares)
    p_num = cache(change_key, p_num, "hash") #key by relative hash instead of absolute hash
    for i in p_words:
        word_values = get_value_for_word(p_words[i],p_num)
        if (word_values == 0): #got an invalid value 
            continue
        word = word_values[0]
        cur_value = word_values[1]
        if (cur_value > max_value):
            print("found new max value %d" % int(cur_value))
            print("value found on words: %s" % p_words[i][0]['value'])
            max_value = cur_value
            sol = word
    return max_value,sol, p_words, p_num

    try:
        word_value = words
    except KeyError:
        pass

    last_length = words[-1]['length']
    last_value = cache(binary_search, 1, pow(10, 100), 16)            
    sl.debug("last_length: %s, last_value: %s" % (str(last_length), str(last_value)))
    for w in reversed(words):                   
        word_length = w['length']                            
        sl.debug("word: %s" % w['value'])
        sl.debug("word_length: %s" % word_length)
        sl.debug("last_lenght: %s" % last_length)
        sl.debug("last_value: %s" % last_value)        
        #Build index incrementally 
        if last_length >= word_length:            
            while True:
                last_value -=1
                p_target = process_entry(pow(last_value, 2))
                counter.incrementCount(p_target['hash'], 1)     
                if (last_value % 100000) == 0:
                    sl.debug("processing %s..." % (last_value))                             
                    #sl.debug("d_values is: %s" % str(d_values))
                try:
                    d_values[p_target['hash']].append(p_target['value']) 
                except (KeyError, AttributeError):
                    d_values[p_target['hash']] = []
                    d_values[p_target['hash']].append(p_target['value']) 
                if (p_target['length'] < word_length):  
                    sl.debug("%s vs %s" % (str(p_target['length']), str(word_length)))
                    sl.info("finished processing %s" % word_length)
                    last_length = word_length                    
                    break     
                if (counter.has_key('555362096768664290')):   
                    sl.info("found hash in counter") 
                    if counter['5553620:177096768664290'] > 2:
                        sl.debug("found a candidate: %s" % str(w))
                        sl.debug("solutions: %s" % str(d_values[w['hash']]))        
                        num = max(d_values['555362096768664290'], key=lambda x: x['value'])
                        return (w['value'], num)                                                             
                else:
                    continue        
        try:                     
            sl.debug("counter: %s " % str(counter))
            if counter[w['hash']] > 2:
                sl.debug("found a candidate: %s" % str(w))
                sl.debug("solutions: %s" % str(d_values[w['hash']]))        
                num = max(d_values[w['hash']], key=lambda x: x['value'])
                return (w['value'], num)            
        except KeyError:     
            sl.info("didn't find hash")
            pass
                
    return False
    
    # size_limit = len(max(text, key=len))   
    #     print(size_limit)
    #     print ("generating numbers...") 
    #     p_num = process_entries(gen_squares(size_limit))
    #     print ("finished processing entries...")
    #     sol = (None, 0)        
    #     for i in text:
    #         val = get_value_for_word(i, p_num)
    #         if val[1] > sol[1]:
    #             print("found new solution: %s" % str(val))
    #             sol = val
    #     return sol                             

def show_prompt():
    print """
    By replacing each of the letters in the word CARE with 1, 2, 9, and 6 respectively, we form a square number: 1296 = 362. What is remarkable is that, by using the same digital substitutions, the anagram, RACE, also forms a square number: 9216 = 962. We shall call CARE (and RACE) a square anagram word pair and specify further that leading zeroes are not permitted, neither may a different letter have the same digital value as another letter.

    Using words.txt (right click and 'Save Link/Target As...'), a 16K text file containing nearly two-thousand common English words, find all the square anagram word pairs (a palindromic word is NOT considered to be an anagram of itself).

    What is the largest square number formed by any member of such a pair?
    """                                                                   

if __name__ == "__main__":
    import doctest           
    #doctest.testmod()     
    #show_prompt()    
    #print solve()
    
