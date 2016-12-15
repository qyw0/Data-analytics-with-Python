# -*- coding: utf-8 -*-
"""
Created on Thu Nov 17 20:38:31 2016

@author: qwang
"""

import json
import numpy as np
from scipy import stats
import argparse as ap
import pulp as pu

def readLPData(fn):
    """
    Input = name of JSON file
    Returns = JSON object
    """
    try:
        with open(fn, 'r') as f:
            LPdata = json.load(f)
        return LPdata
    except:
        return None

def CreateAndSolveLP(LPdata):
    
    #initialise the model
    if LPdata['objective'] == "MIN":
        my_model = pu.LpProblem('My Model', pu.LpMinimize)
    elif LPdata['objective'] == "MAX":
        my_model = pu.LpProblem('My Model', pu.LpMaximize)
    else:
        print ("Neither max nor min")
        exit(0)
    
    # make a list of decision variables
    decVars = LPdata['variables'] 

    # create a dictionary of pulp variables with keys from input vars
    # the default lower bound is -inf, make it 0
    x = pu.LpVariable.dict('x_%s', decVars, lowBound = 0)

    # Objective function data
    objCoeffList = LPdata["objCoeffs"]
    objective = dict(zip(decVars, objCoeffList))
    
    # create the objective
    my_model += sum( [objective[i] * x[i] for i in decVars])

    # create the constraints
    constraintKeys = LPdata["LHS"].keys()
    
    for key in constraintKeys:
        LHScoeffs = dict(zip(decVars,LPdata["LHS"][key]))
        
        if LPdata["conditions"][key] == '<=':
            my_model += sum([LHScoeffs[j]*x[j] for j in decVars]) <= LPdata['RHS'][key]
        elif LPdata["conditions"][key] == '>=':
            my_model += sum([LHScoeffs[j]*x[j] for j in decVars]) >= LPdata['RHS'][key]
        elif LPdata["conditions"][key] == '==':
            my_model += sum([LHScoeffs[j]*x[j] for j in decVars]) == LPdata['RHS'][key]
        else:
            print ("Problems with constraint {}".format(key))
            exit(0)
    
    # solve the LP
    my_model.solve()
    solution = {}
    solution['objective'] = LPdata['objective']
    solution['optimal'] = pu.value(my_model.objective)
    solution['variables'] = {}
    for v in my_model.variables():
        solution['variables'][v.name] = v.varValue
    return (solution)
    
def outputFormat(solution):
    output = {}
    output['brief'] = solution['optimal']
    output['default'] = 'The optimal value is ' + str(solution['optimal'])
    if solution['objective'] == 'MAX':
        obj = 'maximum'
    elif solution['objective'] == 'MIN':
        obj = 'minimum'
    else:
        obj = 'neither max nor min'
    x = ''
    for i in solution['variables']:
        x += i +': ' + str(solution['variables'][i]) + '\n'
    output['detailed'] = 'The %s value is %s\nThe decision variables and their values are:\n%s'%(obj, solution['optimal'], x)
    return(output)

'''   
def writeFile(filename):
    with open(filename, 'a') as f:
            f.write()
    print ("Output written to", filename)
'''
def Main():
    parser = ap.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    
    parser.add_argument("filename", type = str, help="input filename")
    
    group.add_argument("-b", "--brief", help="brief output", action="store_true")
    group.add_argument("-d", "--detailed", help="detailed output", action="store_true")
    
    parser.add_argument('-o', dest='outfile', action='store', help='output file')
    
    args = parser.parse_args()     
    modelData = readLPData(args.filename)
    solution = CreateAndSolveLP(modelData)
    output = outputFormat(solution)
    
    if args.brief:
        print (output['brief'])
    elif args.detailed: 
        print (output['detailed'])
    else:
        print (output['default'])
    if args.outfile:
        with open(args.outfile, 'a') as f:
            f.write(output['detailed'])
        print ("Output written to", args.outfile)
        
if __name__ == "__main__":
    Main()