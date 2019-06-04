'''
Created on 27.05.2019

@author: florian
'''

from ReadGraphs.GraphDataToGraphList import *


def main():
    path = "/home/florian/Dokumente/Databases/GraphData/DS_all/"
    db = "MUTAG"
    gen = graph_data_generator(path, db)
    while True:
        graph_data = next(gen)
        print(type(graph_data))
        graph, graph_label, graph_attribute = graph_data
        
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