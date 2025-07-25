          
from flask import Flask, render_template, request, redirect
import re
import matplotlib.pyplot as plt
import numpy as np
app = Flask(__name__)
@app.route('/graph', methods = ['POST','GET'])
def graph():
    if request.method=='GET':
        return render_template("graph.html")
    eqn = str(request.form.get("eqn")).split("+")
    minx = int(request.form.get("min"))
    maxx= int(request.form.get("max"))
    plotStyle = request.form.get("plotStyle")
    equation = []
    for i in range(len(eqn)):
        equation.append(re.split(r'[*^]+',eqn[i]))
    """
    1*x^2 + 2*x^1 + 1*x^0
    x^1+2*x^0
    """
    """
        even power, odd power -> U or S accordingly
        roots: x=0 change in behaviour of graph at place
        
        how to store: list according to power -> position of the list
        [1,2,1]
        
        finding roots:
        
        create a sample list first then according to the shift and change ?:
        eg: len(eqn) = 3 | X^2
        
        or
        ->maybe specify range and just calculate each value -> takes so much time
    """
    x = [i for i in np.arange(minx,maxx+1,0.1)]
    y = []
    for i in x: 
        ssum = 0
        for j in range(len(equation)):
            ssum+=int(equation[j][0])*(i**int(equation[j][2]))
        y.append(ssum)
    plt.figure()
    plt.grid()
    if plotStyle == 'line':
        plt.plot(x,y)
    if plotStyle == 'scatter':
        plt.scatter(x,y)
    if plotStyle == 'bar':
        plt.plot(x,y)
    plt.plot([minx,0,maxx+1],[0,0,0],scalex=False,scaley=False)
    plt.plot([0,0,0],[min(y),0,max(y)],scalex=False,scaley=False)
    plt.title('Line Graph')
    filename = 'static/graph.png'
    plt.savefig(filename)
    plt.close
    return render_template("graph.html",graph = 'static/graph.png')
@app.route('/matrixop',methods=['POST','GET'])
def matrixop():
   if request.method == 'GET':
       return render_template('matrixop.html')
   if not all(request.form.get(f'a{i}{j}') for i in range(1, 4) for j in range(1, 4)):
       return render_template('error.html', error_message="Missing element")
   a11,a12,a13,a21,a22,a23,a31,a32,a33 = int(request.form.get('a11')),int(request.form.get('a12')),int(request.form.get('a13')),int(request.form.get('a21')),int(request.form.get('a22')),int(request.form.get('a23')),int(request.form.get('a31')),int(request.form.get('a32')),int(request.form.get('a33'))
   matrix1 = [[a11,a12,a13],[a21,a22,a23],[a31,a32,a33]]
   
   b11,b12,b13,b21,b22,b23,b31,b32,b33 = int(request.form.get('b11')),int(request.form.get('b12')),int(request.form.get('b13')),int(request.form.get('b21')),int(request.form.get('b22')),int(request.form.get('b23')),int(request.form.get('b31')),int(request.form.get('b32')),int(request.form.get('b33'))
   matrix2 = [[b11,b12,b13],[b21,b22,b23],[b31,b32,b33]]
   
   operation = request.form.get('operation')
   result = [[0,0,0],[0,0,0],[0,0,0]]
   if operation == 'sum':
       for i in range(0,3):
           for j in range(0,3):
               result[i][j] = matrix1[i][j] + matrix2[i][j]
   elif operation == 'sub':
       for i in range(0,3):
           for j in range(0,3):
               result[i][j] = matrix1[i][j] - matrix2[i][j]
   elif operation == 'multiplication':
       for i in range(0,3):
           for j in range(0,3):
               for k in range(3): result[i][j]+=matrix1[i][k]*matrix2[k][j]
   return render_template('matrixop.html',submit = 1,c11 = result[0][0],c12=result[0][1],c13 =result[0][2],c21 = result[1][0],c22=result[1][1],c23 =result[1][2],c31 = result[2][0],c32=result[2][1],c33 =result[2][2])
app.run(debug = True)