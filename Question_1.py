from datetime import datetime
import networkx as nx

def main():
    pass

def get_data(fname):
    '''Opens Wikipedia revert data in file fname and returns
    list of formatted values.'''
    with open(fname, 'r') as f:
        f.readline() # skip column labels

        data = []
        for edit in f.readlines():
            title, dt, rev, version, user = edit.strip().split('\t')
            data.append([title.strip(), datetime.strptime(dt, "%Y-%m-%d %H:%M:%S"), int(rev), int(version), user])
    return data
    #the result is a nested list for each edit

def create_network(data):
    '''creates directed network from data in nested list following the format [title, time, revert, version, user]. Returns the number of nodes and edges in the network and creates a pickled file of the network'''

    #first create a directed multigraph because connected edges have a direction (from reverter to reverted), and there can be more than one edge between nodes.
    wiki_network = nx.MultiDiGraph()

    #For loop ends at data[len(data)-1] to have space for next_edit_index to exists. This is not an issue because the last item in data is the first ever edit on the wikipedia page, hence it cannot be a revert.
    for n in range(len(data)-1):
        edit = data[n]
        next_edit_list = data[n+1]
        #If statements are used to identify the reverts and to prevent the inclusion of edits without change and self reverts
        if edit[2] == 1 and edit[3] != next_edit_list[3]:

            while edit[3] != next_edit_list[3]:
                reverted = next_edit_list
                n += 1
                next_edit_list = data[n]

            if  edit[4] != reverted[4]:  
    #finally an edge between edit (the reverter) and reverted is created, the usernames are taken as labels for the nodes and the time of the reverter edit is giving as an attribute of the edge
                wiki_network.add_edge(edit[4],reverted[4], time = edit[1])

    return 'The number of nodes is: ' + str(len(wiki_network.node())) + ' and the number of edges is: ' + str(len(wiki_network.edges()))
    #lastly pickle the network
    nx.write_gpickle(wiki_network,'wiki_network')

if __name__=='__main__':
    main()