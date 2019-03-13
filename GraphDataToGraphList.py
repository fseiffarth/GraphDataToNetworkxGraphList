'''
Created on 12.03.2019

@author: florian
'''

import networkx as nx
import numpy as np

def attributes_to_np_array(attr_str):
    return np.asfarray(np.array(attr_str.strip().split(",")), float)
    

def graph_data_to_graph_list(edge_list, graph_indicator_list, graph_labels, node_labels = "", edge_labels = "", edge_attributes = "", node_attributes = "", graph_attributes = ""):
    
    #return variables
    graph_list = []
    graph_label_list = []
    graph_attribute_list = []
    
    #open the data files and read first line
    edge_file = open(edge_list, "r")
    edge = edge_file.readline().strip().split(",")
    
    graph_indicator = open(graph_indicator_list, "r")
    graph = graph_indicator.readline()
    
    if node_labels:
        node_label_file = open(node_labels, "r")
        node_label = node_label_file.readline()    
    
    graph_label_file = open(graph_labels, "r")
    graph_label = graph_label_file.readline()   
     
    #edge labels
    if edge_labels:
        edge_label_file = open(edge_labels, "r")
        edge_label = edge_label_file.readline()
        
    #edge attribures
    if edge_attributes:
        edge_attribute_file = open(edge_attributes, "r")
        edge_attribute = edge_attribute_file.readline()
    
    #node attribures
    if node_attributes:
        node_attribute_file = open(node_attributes, "r+")
        node_attribute = node_attribute_file.readline()

    #graph attribures
    if graph_attributes:
        graph_attribute_file = open(graph_attributes, "r")
        graph_attribute = graph_attribute_file.readline()

    
    #go through the data and read out the graphs
    node_counter = 1
    while graph_label:
        G = nx.Graph()
        old_graph = graph
        new_graph = False
        
        #read out one complete graph
        while not new_graph and edge:
            #set all node labels with possibly node attributes    
            while max(int(edge[0]), int(edge[1])) >= node_counter and not new_graph:
                if graph == old_graph:
                    if node_attributes and node_labels:
                        G.add_node(node_counter, label = int(node_label), attribute = attributes_to_np_array(node_attribute))
                        node_attribute = node_attribute_file.readfile()
                        node_label = node_label_file.readline()
                    elif node_attributes:
                        G.add_node(node_counter, attribute = attributes_to_np_array(node_attribute))
                        node_attribute = node_attribute_file.readfile()
                    elif node_labels:
                        G.add_node(node_counter, label = int(node_label))
                        node_label = node_label_file.readline()
                    else:
                        G.add_node(node_counter)
                    node_counter += 1
                    graph = graph_indicator.readline() 
                else:
                    old_graph = graph 
                    new_graph = True

            if not new_graph:
                #set edge with possibly edge label and attributes and get next line
                if edge_labels and edge_attributes:
                    G.add_edge(int(edge[0]), int(edge[1]), label = int(edge_label), attribute = attributes_to_np_array(edge_attribute))
                    edge_attribute = edge_attribute_file.readline()
                    edge_label = edge_label_file.readline()
                elif  edge_label:
                    G.add_edge(int(edge[0]), int(edge[1]), label = int(edge_label))
                    edge_label = edge_label_file.readline()
                elif edge_attribute:
                    G.add_edge(int(edge[0]), int(edge[1]), attribute = attributes_to_np_array(edge_attribute))
                    edge_attribute = edge_attribute_file.readline()
                else:
                    G.add_edge(int(edge[0]), int(edge[1]))
                    
                #get new edge
                edge = edge_file.readline()
                if edge:
                    edge = edge.strip().split(",")
    
        #add graph to list
        graph_list.append(G)
        
        #add graph label to list
        graph_label_list.append(int(graph_label))
        graph_label = graph_label_file.readline()
        
        if graph_attributes:        
            graph_attribute_list.append(graph_attributes)
            graph_attribute = graph_attribute_file.readline()
            
        
    edge_file.close()
    graph_indicator.close()
    node_label_file.close()
    graph_label_file.close()
    
    if edge_labels:
        edge_label_file.close()
    if edge_attributes:
        edge_attribute_file.close()
    if node_attributes:
        node_attribute_file.close()
    if graph_attributes:
        graph_attribute_file.close()
        
    return (graph_list, graph_label_list, graph_attribute_list)


def graph_list_from_graph(graph):
    list = []
    for node in graph.nodes(data = True):
        list.append(node[1]["label"])
    return list
        
