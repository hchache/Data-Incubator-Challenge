
###### Author: Hitesh Sahadeo Chache 
# 
#  Jupyter Link: https://github.com/hchache/Data-Incubator-Challenge/blob/master/Question%201.ipynb
#  
###### Code - Start

import math as m
import random as r
import numpy as np

# Generates random number 0 or 1 based on current x,y position
def generate_rand(arr,m,n):
    if arr.count(0) == m:
        return 1
    elif arr.count(1) == n:
        return 0
    else:
        return r.randint(0,1)

# Calculates deviation based on given formula
def cal_deviate(x1,y1,m,n):
    return max((x1/m-y1/n),(y1/n-x1/m))

# https://www.python.org/doc/essays/graphs/
def get_paths(graph, start, end, path=[]):
    path = path + [start]
    if start == end:
        return [path]
    if start not in graph:
        return []
    paths = []
    for node in graph[start]:
        if node not in path:
            newpaths = get_paths(graph, node, end, path)            
            for newpath in newpaths:
                paths.append(newpath)
    return paths

def develop_graph(n,m):
    d = {}
    deviation = {}
    for x in range(n+1):
        for y in range(m+1):
            index = str(x)+str(y)
            deviation[index] = cal_deviate(x,y,m,n)
            if index == (str(n)+str(m)):
                break
            if y != m or x != n:
                d[index] = [str(x+1)+str(y),str(x)+str(y+1)]
            elif y == m:
                d[index] = [str(x+1)+str(y)]
            elif x == n:
                d[index] = [str(x)+str(y+1)]
    return d, deviation

# This approach is similar to previous one but in this approach all paths are not derived.
# Instead it takes random direction at every single point
def random_traverse_approach(n,m):
    n = int(n)
    m = int(m)
    x,y,max_N,max_E = 0,0,m,n 
    D,B,A = [0.0],[[0,0]],[]
    if(x==n and y==m): return
    for i in range(m+n):
        b = generate_rand(A,m,n)
        A.append(b)
        if b == 0 and max_N!=0:
            y = y + 1
            max_N = max_N - 1
            # print("max_N",max_N)
        if b == 1 and max_E!=0:
            x = x + 1
            max_E = max_E - 1
            # print("max_E",max_E)
        D.append(cal_deviate(x,y,m,n))
        # B gives x and y co-ordinates
        B.append([x,y])
    return D

# This approach is similar to random_traverse_approach but in this approach ant takes NENENENE path.
# Instead of taking random direction at every single point, it takes NENENE approach
def equi_traverse_approach(n,m):
    n = int(n)
    m = int(m)
    x,y,max_N,max_E = 0,0,m,n 
    D,B,A = [0.0],[[0,0]],[]
    b = 0
    if(x==n and y==m): return
    for i in range(m+n):
#         b = generate_rand(A,m,n)
        A.append(b)
        if max_N == 0:
            b = 1
        elif max_E == 0:
            b = 0
            
        if b == 0 and max_N!=0:
            y = y + 1
            max_N = max_N - 1
            # print("max_N",max_N)
        elif b == 1 and max_E!=0:
            x = x + 1
            max_E = max_E - 1
            # print("max_E",max_E)
        D.append(cal_deviate(x,y,m,n))
        b = abs(b-1)
        # B gives x and y co-ordinates
        B.append([x,y])
#         print(B)
    return D

# This approach return Deviation list D of random paths from all path list (instead of deviation of a path at x,y).
# Size of D is m+n+1
def all_path_random_approach(n, m):
    graph, deviation = develop_graph(n, m)
    D = []
    start = '00'
    end = str(n)+str(m)
    paths = get_paths(graph, start, end)
    i = r.randint(0, len(paths)-1)
    random_path = paths[i]
    for p in random_path:
        D.append(float(deviation[p]))
    return D

# This approach return Deviation list D as mean of all paths (instead of deviation of a path at x,y).
# Here D will have (m+n)!/m!n! entries instead of m+n+1 
def all_path_approach(n, m):
    graph, deviation = develop_graph(n, m)
    D = []
    start = '00'
    end = str(n)+str(m)
    paths = get_paths(graph, start, end)
    for path in paths:
        t = []
        for p in path:
            t.append(float(deviation[p]))
        D.append(np.mean(t))
    return D

# Due to multiple functions and different approach,
# defined each question as a function to improve readability

# What is the mean of D when m=11 and n=7?
def q1(f):
    m,n = 11,7
    D = f(n,m)
    return np.mean(D)

# What is the standard deviation of D when m=11 and n=7?
def q2(f):
    m,n = 11,7
    D = f(n,m)
    return np.std(D)

# What is the mean of D when m=23 and n=31?
def q3(f):
    m,n = 23,31
    D = f(n,m)
    return np.mean(D)

# What is the standard deviation of D when m=23 and n=31?
def q4(f):
    m,n = 23,31
    D = f(n,m)
    return np.std(D)

# What is the conditional probability that D is greater than 0.6 given that it is greater than 0.2 when m=11 and n=7?
def q5(f):
    m,n = 11,7
    D = f(n,m)
    ans = (sum(i > 0.6 for i in D)/len(D))/(sum(i > 0.2 for i in D)/len(D))
    return ans

# What is the conditional probability that D is greater than 0.6 given that it is greater than 0.2 when m=23 and n=31?
def q6(f):
    m,n = 23,31
    D = f(n,m)
    ans = (sum(i > 0.6 for i in D)/len(D))/(sum(i > 0.2 for i in D)/len(D))
    return ans

# Main function
def Main():
   # User input code
   # m = int(input("m?"))
   # n = int(input("n?"))
    print("----------random_traverse_approach-----------")
    print("Answer 1: ",format(q1(random_traverse_approach), '.10g'))
    print("Answer 2: ",format(q2(random_traverse_approach), '.10g'))
    print("Answer 3: ",format(q3(random_traverse_approach), '.10g'))
    print("Answer 4: ",format(q4(random_traverse_approach), '.10g'))
    print("Answer 5: ",format(q5(random_traverse_approach), '.10g'))
    print("Answer 6: ",format(q6(random_traverse_approach), '.10g'))
    print("----------equi_traverse_approach-----------")
    print("Answer 1: ",format(q1(equi_traverse_approach), '.10g'))
    print("Answer 2: ",format(q2(equi_traverse_approach), '.10g'))
    print("Answer 3: ",format(q3(equi_traverse_approach), '.10g'))
    print("Answer 4: ",format(q4(equi_traverse_approach), '.10g'))
    print("Answer 5: ",format(q5(equi_traverse_approach), '.10g'))
    print("Answer 6: ",format(q6(equi_traverse_approach), '.10g'))
    print("----------all_path_random_approach-----------")
    # Calculating all paths for 31 x 23 is not a good idea! Hence commented Question 3,4, and 6
    print("Answer 1: ",format(q1(all_path_random_approach), '.10g'))
    print("Answer 2: ",format(q2(all_path_random_approach), '.10g'))
#     print("Answer 3: ",q3(all_path_random_approach))
#     print("Answer 4: ",q4(all_path_random_approach))
    print("Answer 5: ",format(q5(all_path_random_approach), '.10g'))
#     print("Answer 6: ",q6(all_path_random_approach))
    print("-------------all_path_approach---------------")
    print("Answer 1: ",format(q1(all_path_approach), '.10g'))
    print("Answer 2: ",format(q2(all_path_approach), '.10g'))
#     print("Answer 3: ",q3(all_path_approach))
#     print("Answer 4: ",q4(all_path_approach))
    print("Answer 5: ",format(q5(all_path_approach), '.10g'))
#     print("Answer 6: ",q6(all_path_approach))
    print("------------------END------------------------")
if __name__ == '__main__':
    Main() 

