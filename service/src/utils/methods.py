import numpy as np

def entropy(data):
    base = np.log(data.shape[0])
    prob = data/(np.sum(data))
    log_prob = []
    for p in prob:
        if p != 0.0:
            log_prob.append(np.log(p))
        else:
            log_prob.append(0.0)
    print(log_prob)
    log_prob = np.array(log_prob)
    H_x = prob * (log_prob/base)
    return -np.sum(H_x)
