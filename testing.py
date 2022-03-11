import statistics

from pandas import cut

def average(list):
    """
    Returns the average value of the given list.
    """
    return sum(list) / len(list)

def find_boundaries(sd):
    #TB = average(sd) + statistics.pstdev(sd) * 11
    #TS = average(sd) * 2

    TB = 7
    TS = 2

    cuts = list()
    gradual_trans = list()
    fs_candi = -1
    lower_than_ts = 0
    fs_candi_set = False
    cut_found = False

    for i in range(len(sd)):

        # if greater than TB, it's a cut
        if sd[i] >= TB:
            # Cs = i, Ce = i+1
            cuts.append((i, i + 1))
            cut_found = True
        
        # if we didn't find a cut on this iter
        if not cut_found:
            # if greater that TS and less than TB, it's possibly a gt
            if sd[i] >= TS and sd[i] < TB:
                # if we haven't set a start candi
                if not fs_candi_set:
                    # set it
                    fs_candi = i
                    fs_candi_set = True
                    #print('fs_candi:', fs_candi)
                else:
                    # fs is already set and we're trying to find the end
                    # set fe
                    fe_candi = i
                    #print('fe_candi:', fe_candi)
            else:
                # sd[i] < TS so we need to track that
                if fs_candi_set:
                    lower_than_ts += 1

        # if we've hit the Tos or a cut boundary
        if lower_than_ts > 2 or i in [Cs for Cs, Ce in cuts]:

            # get the sum of sds from fs to fe
            gt_sum = sum([sd[i] for i in range(fs_candi, fe_candi + 1, 1)])
            
            # if this sum is bigger than TB
            if gt_sum >= TB:
                # we found a gt!
                gradual_trans.append((fs_candi, fe_candi))
                
            # reset all vales
            fs_candi_set = False
            cut_found = False
            lower_than_ts = 0
        
    return cuts, gradual_trans

sd = [1,4,1,4,8,3,3,1,1]
print(find_boundaries(sd))
