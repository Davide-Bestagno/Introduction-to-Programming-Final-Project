import networkx as nx
import math
from matplotlib import pyplot

def main():
    pass

def interaction_time(network, label):
    '''Requires network object with nodes with class attributes equal to label and edges with 'time' attributes. The function calculates the time between interactions for each couple of nodes with the specified label and with more than one edge between them'''
    
    # create subgraph this reduces processing time because the subsequent iterations are conducted on less nodes
    label_network = network.subgraph([x for x,y in network.nodes(data=True) if y['class']==label])
    
    #sort the subgraphs in chronological order which is necessary for the next step, reverse is needed to have in descending order prepared for the subtraction for timedelta. By using reverse all values are positive.
    
    sorted_list = sorted(label_network.edges(data=True), key=lambda x: x[2]['time'], reverse = True)

    #now to collect toghether the times for i to j and j to i and mantain the chronological order a new simple undirected network is created.  This way the edges i to j and j to i times are grouped together and multiple time attributes for each interaction between the two nodes can be give to a single edge
    times_network = nx.Graph()

    for u,v,data in sorted_list: #u is the reverter v is the reverted
        t = data['time']
        if times_network.has_edge(u, v):
            times_network[u][v]['time'].append(t) #if the edge already exists add time t as an additional value for the same key ('time')
        else:
            times_network.add_edge(u,v, time = [t])

    #now we need to calculate the delta
    timedelta = []
    for u,v,data in times_network.edges(data = True):
        time = list(data['time'])
        if len(times_network[u][v]['time'])>1:
            for n in range(len(time) - 1): #i is the time of each instance of the edge (-1 needed for subtraction)
                current_edit = time[n]
                previous_edit = time[n + 1]
                if (current_edit - previous_edit).total_seconds() != 0:
                    timedelta.append(math.log10((current_edit - previous_edit).total_seconds()))
                    
    return timedelta
                    
def overlapping_histogram(list1, list2, label1, label2, bin_rule = 'auto', normal = True):
    '''Creates two histograms and plots them in a single image with bins set automatically by default (i.e. choosing the maximum the Sturges and Freedman-Diaconis bin choice) this can be changed to a specific number if needed(e.g. bin_rule = 10). The data for the histogram has to be in a list and is normalised in the plotting by default (to better compare the differences between the two datasets), but can be changed (e.g. ormal = False)'''
    
    z, x, _ = pyplot.hist(list1, bins = bin_rule, density = normal, alpha = 0.5, label = label1)
    j, k, _ = pyplot.hist(list2, bins = bin_rule, density = normal, alpha = 0.5, label = label2)
    
    #this is needed to fix the max value of the y-axis to the max value of y in either histogram
    
    if z.max() >= j.max():
        y = z
    else:
        y = j
    
    pyplot.legend(loc='upper right')
    pyplot.ylim(top = y.max(), bottom = 0)
    return pyplot.show()    
    

if __name__=='__main__':
    main()