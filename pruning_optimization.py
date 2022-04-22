import numpy as np
import constants
from sharing_optimization import sharing_optimize
import math
import collections
import warnings
warnings.filterwarnings("error")

def kl_divergence(target, reference):
    keys = set(target.keys()).union(set(reference.keys()))
    target_list = []
    reference_list = []
    for key in keys:
        if key in target:
            target_list.append(float(target[key]))
        else:
            target_list.append(0.0)
        if key in reference:
            reference_list.append(float(reference[key]))
        else:
            reference_list.append(0.0)
    np_target = np.array(target_list)
    np_reference = np.array(reference_list)
    target_len = np.count_nonzero(np_target)
    reference_len = np.count_nonzero(np_reference)
    target_error = 0
    reference_error = 0
    if target_len>0:
        target_error = constants.EPSILON/target_len
    if reference_len>0:
        reference_error = constants.EPSILON/reference_len
    for i in range(len(np_target)):
        if np_target[i] > constants.EPSILON:
            np_target[i] = np_target[i]-target_error
        else:
            np_target[i] = np_target[i]+constants.EPSILON
        if np_reference[i] > constants.EPSILON:
            np_reference[i] = np_reference[i]-reference_error
        else:
            np_reference[i] = np_reference[i]+constants.EPSILON
    np_target_prob_distribution = np_target / np.sum(np_target)
    np_reference_prob_distribution = np_reference / np.sum(np_reference)
    utility = np.sum(np.log(np.divide(np_target_prob_distribution, np_reference_prob_distribution)))
    return utility


def pruning_optimization(candidate_queries):
    issues = set()
    new = 0
    for phase in range(constants.PHASES):
        married_dict, unmarried_dict = sharing_optimize(candidate_queries, phase)
        utility = {}
        for (f, a, m) in candidate_queries:
            #kld = kl_divergence(married_dict[((f, a, m))], unmarried_dict[((f, a, m))])
            try:
                utility[(f, a, m)] = kl_divergence(married_dict[((f, a, m))], married_dict[((f, a, m))])
            except Exception as e:
                if (f,a,m)   not in issues:
                    new+=1
                    issues.add((f,a,m))
        m = (phase + 1)
        if m > 1:
            top_k = collections.OrderedDict(
                sorted(utility.items(), key=lambda kv: kv[1], reverse=True)[:constants.TOPK])
            min_util = min(top_k.values())
            a = 1 - ((m - 1) / constants.PHASES)
            b = 2 * math.log(math.log(m))
            c = math.log((math.pi ** 2) / (3 * constants.DELTA))
            e = math.sqrt((a * (b + c) / 2 * m))
            for (f, a, m) in utility.keys():
                if utility[(f, a, m)] + e < min_util - e:
                    candidate_queries.remove((f, a, m))
    return top_k
