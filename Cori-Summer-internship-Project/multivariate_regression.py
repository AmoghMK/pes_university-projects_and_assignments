import numpy as np

def regression2(x,y,z):
    order=6
    features=np.empty([len(x),order],dtype=float)
    theta=np.zeros(order)
    cost=0
    cost_prev=0
    tolerance=1e-4
    iterations=10000
    learning_rate=0.01
    l1_penalty=0.1
    l2_penalty=0.1
    for i in range(len(x)):
        features[i][0]=1
        features[i][1]=x[i]
        features[i][2]=y[i]
        features[i][3]=x[i]*y[i]
        features[i][4]=pow(x[i],2)
        features[i][5]=pow(y[i],2)
    log=0
    for repeat in range(iterations):
        mat_mult = features.dot(theta)-z
        theta[0]-=(learning_rate/len(x))*(mat_mult*features[:,0]).sum()
        for j in range(1,order):
            theta[j]-=(learning_rate/len(x))*((mat_mult*features[:,j]).sum() 
                            + l1_penalty + l2_penalty*theta[j])
            if(repeat%10 == 0):
                cost = (1./(2*len(x))) * (np.power(features.dot(theta) - z, 2).sum() 
                            + l1_penalty*theta.sum() 
                            + l2_penalty*np.power(theta,2).sum())
                if(log > 1 and np.abs(cost - cost_prev) < tolerance):
                    break
                log += 1
                cost_prev = cost
    return (theta, cost, repeat)

def predict(x,y,theta):
    order=6
    result=np.zeros(len(x))
    result += theta[0]
    result += theta[1]*np.power(x,1)
    result += theta[2]*np.power(y,1)
    result += theta[3]*np.array(x)*np.array(y)
    result += theta[4]*np.power(x,2)
    result += theta[5]*np.power(y,2)
    return (result)
