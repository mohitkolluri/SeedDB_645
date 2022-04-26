import numpy as np
import constants
from sharing_optimization import sharing_optimize
import math
import collections
import warnings
warnings.filterwarnings("error")
from scipy import stats
def kl_divergence(target, reference):
    keys = set(target.keys()).intersection(set(reference.keys()))
    target_list = []
    reference_list = []
    for key in keys:
        target_list.append(float(target.get(key,0.0)))
        reference_list.append(float(reference.get(key,0.0)))
    np_target = np.array(target_list)
    np_reference = np.array(reference_list)
    np_target[np_target==0] +=constants.EPSILON
    np_reference[np_reference==0] +=constants.EPSILON
    #target_sum = np.sum(np_target)
    #ref_sum = np.sum(np_reference)
    np_target_prob_distribution = np_target / np.sum(np_target)
    np_reference_prob_distribution = np_reference / np.sum(np_reference)
    utility = stats.entropy(np_target_prob_distribution,np_reference_prob_distribution)
    '''if target_sum!=0 and ref_sum!=0:
        np_target_prob_distribution = np_target / np.sum(np_target)
        np_reference_prob_distribution = np_reference / np.sum(np_reference)
        for i in range(len(np_target)):
            if np_target_prob_distribution[i]!=0 and np_reference_prob_distribution[i]!=0:
                utility+= math.log(np_target_prob_distribution[i], np_reference_prob_distribution[i])'''
    return utility


def pruning_optimization(candidate_queries):
    issues = set()
    new = 0
    utility = collections.defaultdict(float)
    for phase in range(constants.PHASES):
        print(len(candidate_queries))
        married_dict, unmarried_dict = sharing_optimize(candidate_queries, phase)
        for (f, a, m) in candidate_queries:
            try:
                utility[f,a,m]+=kl_divergence(unmarried_dict[((f, a, m))], married_dict[((f, a, m))])
            except Exception as e:
                issues.add((f,a,m))
                print(e)
        m = (phase + 1)
        #print(utility)
        if m > 1:
            top_k = collections.OrderedDict(
                sorted(utility.items(), key=lambda kv: kv[1], reverse=True)[:constants.TOPK])
            a = 1 - ((m - 1) / constants.PHASES)
            b = 2 * math.log(math.log(m))
            c = math.log((math.pi ** 2) / (3 * constants.DELTA))
            e = math.sqrt((a * (b + c) / 2 * m))
            min_util = min(top_k.values())/(phase+1)-e
            prunelist = set()
            for (f, a, m) in utility.keys():
                if utility[(f, a, m)]/(phase+1) + e < min_util:
                    prunelist.add((f,a,m))
            for (f, a, m) in prunelist:
                if (f,a,m) in candidate_queries:
                    candidate_queries.remove((f,a,m))
                if (f,a,m) in utility.keys():
                    utility.pop((f,a,m))
    #print(issues)
    return top_k
