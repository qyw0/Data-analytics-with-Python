# -*- coding: utf-8 -*-
"""
Created on Fri Sep 16 19:53:35 2016

@author: qinya wang
GWID: G37220174
"""
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
from sklearn import linear_model
from pandas import DataFrame
from sklearn.metrics import r2_score
from mpl_toolkits.mplot3d import *

def fileinput(filename):
    """
    Input = name of csv text file with comma separated numbers
    Output = numpy array
    """
    df = pd.read_csv(filename)
    #arr = DataFrame(data = df, columns = ['y', 'x1', 'x2'])
    arr = df.as_matrix()
    return arr
   
def regress(myData):
    """
    Input = numpy array with three columns
    Column 1 is the dependent variable
    Columns 2 and 3 are the independent variables
    Returns = a column vector with the b coefficients
    """
    xa = myData[:, 1:]
    X = np.array([np.concatenate((v,[1])) for v in xa])
    ya = myData[:, 0]
    model = linear_model.LinearRegression(fit_intercept = True)
    fit = model.fit(X,ya)
    pred = model.predict(X)
    r2 = r2_score(ya,pred) 
    b= [fit.intercept_.round(2), fit.coef_[0].round(2), fit.coef_[1].round(2), r2]
    return (b)
    
def myPlot(myData, b):
    """
    Input = numpy array with three columns
            Column 1 is the dependent variable
            Columns 2 and 3 are the independent variables
            and
            a column vector with the b coefficients
    Returns = Noting
    Output = 3D plot of the actual data and 
             the surface plot of the linear model
    """        
    # http://stackoverflow.com/questions/15229896/matplotlib-3d-plots-combining-scatter-plot-with-surface-plot

    fig = plt.figure()
    ax = fig.gca(projection='3d')               # to work in 3d
    plt.hold(True)
    
    x_max = max(myData[:,1])    
    y_max = max(myData[:,2])   
    
    b0 = float(b[0])
    b1 = float(b[1])
    b2 = float(b[2])   
    
    x_surf=np.linspace(0, x_max, 100)                # generate a mesh
    y_surf=np.linspace(0, y_max, 100)
    x_surf, y_surf = np.meshgrid(x_surf, y_surf)
    z_surf = b0 + b1*x_surf +b2*y_surf         # ex. function, which depends on x and y
    ax.plot_surface(x_surf, y_surf, z_surf, cmap=cm.hot, alpha=0.2);    # plot a 3d surface plot
    
    x=myData[:,1]
    y=myData[:,2]
    z=myData[:,0]
    ax.scatter(x, y, z);                        # plot a 3d scatter plot
    
    ax.set_xlabel('x1')
    ax.set_ylabel('y2')
    ax.set_zlabel('y')

    plt.show()
