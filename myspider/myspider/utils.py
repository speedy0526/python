# -*- coding: utf-8 -*-

def strips(s, charArray):
    if s == None or s == "":
        return ""
    
    if isinstance(charArray,list) == False:
        raise Exception("charArray Must be Char List")
         
    for a in charArray:
       s = s.strip(a)
       
    return s
        
