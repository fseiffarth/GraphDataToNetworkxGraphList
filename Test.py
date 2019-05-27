'''
Created on 27.05.2019

@author: florian
'''

from ReadGraphs.GraphDataToGraphList import *


def main():
    path = "/home/florian/Dokumente/Databases/GraphData/DS_all/"
    db = "REDDIT-BINARY"
    graph_data = graph_data_to_graph_list(path, db)
    graph_list, graph_labels, graph_attributes = graph_data
    
    draw_graph(graph_list[1])


if __name__ == '__main__':
    main()