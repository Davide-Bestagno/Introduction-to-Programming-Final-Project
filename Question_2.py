import networkx as nx
from collections import Counter

def main():
    pass

def classification(network, data, botfname):
    '''Requires a network object, data in a nested list with format [title, time, revert, version, user], and the filename of a list of bots' usernames. The function classifies nodes in the network into vandal, bot, or human and returns the number of nodes of each type. A pickled file of the network is also created'''
    
    bot_list=[]
    for i in open(botfname,'r'):
        bot_name = i.replace('\n','')
        bot_list.append(bot_name)

    #a vandal (i) will have all the edits reverts, hence number of times i is reverted  = number of edits. The former is obtained using the in_degree(i) method for network objects, the latter is calculated using the counter function.
    vandal_list = []
    for i in data:
        vandal_list.append(i[4])

    Vandal_counter = Counter(vandal_list)

    for node in network.nodes():
        if Vandal_counter[node] == network.in_degree(node):
            network.node[node]['class'] = 'vandal'

        elif node in bot_list:
            network.node[node]['class'] = 'bot' #defining bots after vandals prevents the issue of having bots being miscalassified as vandals

        else:
            network.node[node]['class'] = 'human'

    Class_counter = Counter([d['class'] for n,d in network.nodes(data = True)])
    
    return str(Class_counter)
    
    #lastly pickle the network
    nx.write_gpickle(network,'wiki_network')

if __name__=='__main__':
    main()