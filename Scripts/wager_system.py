

#returns suggested base amount for bet
#over/unders are generally in slight minus odds, for the purpose of this excercise we will assume a line of -112
#This means a $112 dollar bet pays out $100
#For the example above this function should return 112, NOT 100
#If using this function for purposes other than this excercise, all values can be scaled by a constant value to fit
#your personal financial constraints
#returns 0 if prediction and projection are within threshold
def wager(thresh, base, rate, pred, proj):
    value = 0
    thresh2 = thresh
    if pred<=proj:
        thresh2 = -1*thresh
        
    if abs(pred-proj)<=thresh:
        return value
    else:
        value = base + rate*abs(pred-proj-thresh2)
        return value

def optimal_wager(pred, proj):
    return wager(3,1,15, pred, proj)


        
        


# In[12]:


wager(2, 1, 1, 200, 199)


# In[20]:


print(wager(2, 1, 1, 200, 201))
print(wager(2,1,1, 200, 203))
print(wager(2, 1, 1, 200, 199))
print(wager(2,1,1, 200, 197))

