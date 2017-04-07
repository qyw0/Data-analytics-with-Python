# -*- coding: utf-8 -*-
"""
Created on Sun Nov 20 23:19:31 2016

@author: qwang
"""

import json
import argparse as ap
import pulp as pu
import os
import pymongo

def ReadAndStore():
    included_extenstions = ['json' ]
    file_names = [fn for fn in os.listdir(os.getcwd())
    if any([fn.endswith(ext)
    for ext in included_extenstions])];
    client = pymongo.MongoClient()
    client.drop_database('problems0')
    db = client["problems0"]
    db.collection.drop()
    collection = db["lp0"]
    for fn in file_names:
        try:        
            with open(fn, 'r') as f:
                LPdata = json.load(f)
                collection.insert_one(LPdata)
        except:
            pass
    return collection
    
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
    solution['problemName'] = LPdata['name']
    if pu.LpStatus[my_model.status] == 'Optimal':
        solution['optimalValue'] = pu.value(my_model.objective)
    else:
        solution['optimalValue'] = 'NA'
    return (solution)

def solve(collection):
    output = []
    for i in collection.find():
        solution = CreateAndSolveLP(i)
        output.append(solution)
    return (output) 

def Main():
    parser = ap.ArgumentParser()
    
    parser.add_argument('-d', dest='database', action="store", help="store to database")
    parser.add_argument('-t', dest='outfile', action='store', help='output file')
    
    args = parser.parse_args()     
    modelData = ReadAndStore()
    output = solve(modelData)
    
    txt = []
    for i in output:
        txt.append('The optimal value for %s is %s'%(i['problemName'], i['optimalValue']))
    for i in txt:
        print (i)
    
    if args.database:
        client = pymongo.MongoClient()        
        client.drop_database('LP')
        db = client['LP']
        db.collection.drop()
        collection = db[args.database]
        for i in output:
            collection.insert_one(i)
        print ('Output written to table: %s in the LP database'%(args.database))

    if args.outfile:
        with open(args.outfile, 'a') as f:
            for i in txt:
                f.write(i + '\n')
        print ("Output written to", args.outfile)
        
if __name__ == "__main__":
    Main()
