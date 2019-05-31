'''
Created on 27.05.2019

@author: florian
'''

from ReadGraphs.GraphDataToGraphList import *


def main():
    path = "/home/florian/Dokumente/Databases/GraphData/DS_all/"
    db = "DHFR"
    graph_data = graph_data_to_graph_list(path, db)
    graph_list, graph_labels, graph_attributes = graph_data
    
    graph = graph_list[1]
    draw_graph(graph)
    print(nodes_label_matrix(graph))
    print(type(nodes_label_matrix(graph)))
    #print(nodes_label_coding_matrix(graph, 50, False))
    
    print(edges_attribute_matrix(graph))
    print(edges_label_coding_matrix(graph, 5, False))
    print(has_node_labels(graph))
    print(node_attribute_dimension(graph))

if __name__ == '__main__':
    main()