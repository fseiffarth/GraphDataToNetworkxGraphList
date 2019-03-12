'''
Created on 12.03.2019

@author: florian
'''

import networkx as nx

def graph_data_to_graph_list(edge_list, graph_indicator_list, graph_labels, node_labels, edge_labels = "", edge_attributes = "", node_attributes = "", graph_attributes = ""):
    
    #return variables
    graph_list = []
    graph_label_list = []
    graph_attribute_list = []
    
    #open the data files and read first line
    edge_file = open(edge_list, "r")
    edge = edge_file.readline().strip().split(",")
    
    graph_indicator = open(graph_indicator_list, "r")
    graph = graph_indicator.readline()
    
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
        node_attribute_file = open(node_attributes, "r")
        node_attribute = node_attribute_file.readfile()

    #graph attribures
    if graph_attributes:
        graph_attribute_file = open(graph_attributes, "r")
        graph_attribute = graph_attribute_file.readline()

    
    
    
    #Read out first line of the data



    
    #go through the data and read out the graphs
    node_counter = 1
    while graph_label:
        G = nx.Graph()
        old_graph = graph
        
        #read out one complete graph
        while old_graph == graph and edge_label and edge:
            
            #set edge with possibly edge label and attributes and get next line
            if edge_labels and not edge_attributes:
                G.add_edge(int(edge[0]), int(edge[1]), label = int(edge_label))
                edge_label = edge_label_file.readline()

            elif edge_attributes:
                G.add_edge(int(edge[0]), int(edge[1]), label = int(edge_label), attribute = edge_attribute)
                edge_attribute = edge_attribute_file.readline()
                edge_label = edge_label_file.readline()

            else:
                G.add_edge(int(edge[0]), int(edge[1]))
            

            
            #set all node labels with possibly node attributes    
            while max(int(edge[0]), int(edge[1])) >= node_counter:
                graph = graph_indicator.readline()
                if node_attributes:
                    G.add_node(node_counter, label = int(node_label))
                    node_attribute = node_attribute_file.readfile()
                    node_label = node_label_file.readline()
                else:
                    G.add_node(node_counter, label = int(node_label))
                    node_label = node_label_file.readline()
                node_counter += 1
                
            
            edge = edge_file.readline().strip().split(",")
            old_graph = graph                
            graph = graph_indicator.readline()
            
                
            
        #add graph to list
        graph_list.append(G)
        
        #add graph label to list
        graph_label_list.append(int(graph_label))
        graph_label = graph_label_file.readline()
        
        if graph_attributes:        
            graph_attribute_list.append(graph_attributes)
            graph_attribute = graph_attribute_file.readline()
        
    return (graph_list, graph_label_list, graph_attribute_list)
