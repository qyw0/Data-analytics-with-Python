# -*- coding: utf-8 -*-
"""
Created on Fri Sep 16 19:53:35 2016

@author: qinya wang
GWID: G37220174
"""
import A02Module_G37220174 as md
import argparse
def Main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    
    parser.add_argument("filename", type = str, help="input filename")
    
    group.add_argument("-b", "--brief", help="brief output", action="store_true")
    group.add_argument("-v", "--verbose", help="verbose output", action="store_true")
    
    parser.add_argument('-o', dest='outfile', action='store', help='output file')
    parser.add_argument("-p", "--plot", help="plot regression",action="store_true")
    
    args = parser.parse_args()    
    myData = md.fileinput(args.filename)
    b=md.regress(myData)
    v_output = "The equation is: y =%s + %sx1 + %sx2\nThe R^2 value is: %s\n  y    x1    x2\n=================\n%s"%(b[0],b[1],b[2],b[3],myData)

    if args.brief:
        print ("intercept =", b[0], "\nb1 =", b[1], "\nb2 =", b[2])
    elif args.verbose: 
        print (v_output)
    else:
        print ("intercept =", b[0], "\nb1 =", b[1], "\nb2 =", b[2])
        print ("The R^2 value is: ",b[3])    
    if args.outfile:
        with open(args.outfile, 'a') as f:
            f.write(v_output)
        print ("Output being sent to", args.outfile)
    if args.plot:
        md.myPlot(myData, b)
    
        
if __name__ == "__main__":
    Main()