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
        target_list.append(float(target.get(key,0.0)))
        reference_list.append(float(reference.get(key,0.0)))
    np_target = np.array(target_list)
    np_reference = np.array(reference_list)
    np_target[np_target==0] +=constants.EPSILON
    np_reference[np_reference==0] +=constants.EPSILON
    np_target_prob_distribution = np_target / np.sum(np_target)
    np_reference_prob_distribution = np_reference / np.sum(np_reference)
    utility = np.sum(np.log(np.divide(np_target_prob_distribution, np_reference_prob_distribution)))
    return utility


def pruning_optimization(candidate_queries):
    issues = set()
    new = 0
    utility = {}
    for phase in range(constants.PHASES):
        print(len(candidate_queries))
        married_dict, unmarried_dict = sharing_optimize(candidate_queries, phase)
        new_utils={}
        for (f, a, m) in candidate_queries:
            #kld = kl_divergence(married_dict[((f, a, m))], unmarried_dict[((f, a, m))])
            try:
                new_utils[(f, a, m)] = utility.get((f, a, m),0.0)+kl_divergence(married_dict[((f, a, m))], unmarried_dict[((f, a, m))])/(phase+1)
            except Exception as e:
                issues.add((f,a,m))
                print(e)
        m = (phase + 1)
        if m > 1:
            top_k = collections.OrderedDict(
                sorted(new_utils.items(), key=lambda kv: kv[1], reverse=True)[:constants.TOPK])
            min_util = min(top_k.values())
            a = 1 - ((m - 1) / constants.PHASES)
            b = 2 * math.log(math.log(m))
            c = math.log((math.pi ** 2) / (3 * constants.DELTA))
            e = math.sqrt((a * (b + c) / 2 * m))
            for (f, a, m) in new_utils.keys():
                if new_utils[(f, a, m)] + e < min_util - e:
                    candidate_queries.remove((f, a, m))
        utility=new_utils

    print(issues)
    return top_k
