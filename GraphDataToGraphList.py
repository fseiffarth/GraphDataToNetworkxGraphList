'''
Created on 12.03.2019

@author: florian
'''

import networkx as nx
import numpy as np
from pathlib import Path
import io
import pydot
import matplotlib
from matplotlib import pyplot

def attributes_to_np_array(attr_str):
    return np.asfarray(np.array(attr_str.strip().split(",")), float)
    

def graph_data_to_graph_list(path, db):
    '''
    Convert graph dataset in the Dortmund collection to a networkx graph with node and edge labels and graph labels and attributes.

    Currently, vertex and edge labels will be the first dimension of the label vector, cast as int, or 'None' if there
    are no label information present. See getLabel above.

    Graphs will be numbered from 0 to N-1 if there are N graphs in the dataset.

    :param path: path to the unzipped location of the collection (must be terminated with '/'
    :param db: name of the dataset in the collection
    :return (graph_list, graph_label_list, graph_attribute_list): triple of python lists of networkx graphs, graph labels and graph attributes
    '''

    #return variables
    graph_list = []
    graph_label_list = []
    graph_attribute_list = []
    
    #open the data files and read first line
    edge_file = open(path + db + "/" + db + "_A.txt", "r")
    edge = edge_file.readline().strip().split(",")
    
    #graph indicator
    graph_indicator = open(path + db + "/" + db + "_graph_indicator.txt", "r")
    graph = graph_indicator.readline()
    
    #graph labels
    graph_label_file = open(path + db + "/" + db + "_graph_labels.txt", "r")
    graph_label = graph_label_file.readline()   
    
    #node labels
    node_labels = False
    if Path(path + db + "/" + db + "_node_labels.txt").is_file():
        node_label_file = open(path + db + "/" + db + "_node_labels.txt", "r")
        node_labels = True
        node_label = node_label_file.readline()    
    
     
    #edge labels
    edge_labels = False
    if Path(path + db + "/" + db + "_edge_labels.txt").is_file():
        edge_label_file = open(path + db + "/" + db + "_edge_labels.txt", "r")
        edge_labels = True
        edge_label = edge_label_file.readline()
        
    #edge attribures
    edge_attributes = False
    if Path(path + db + "/" + db + "_edge_attributes.txt").is_file():
        edge_attribute_file = open(path + db + "/" + db + "_edge_attributes.txt", "r")
        edge_attributes = True
        edge_attribute = edge_attribute_file.readline()
    
    #node attribures
    node_attributes = False
    if Path(path + db + "/" + db + "_node_attributes.txt").is_file(): 
        node_attribute_file = open(path + db + "/" + db + "_node_attributes.txt", "r")    
        node_attributes = True
        node_attribute = node_attribute_file.readline()

    #graph attribures
    graph_attributes = False
    if Path(path + db + "/" + db + "_graph_attributes.txt").is_file():
        graph_attribute_file = open(path + db + "/" + db + "_graph_attributes.txt", "r")
        graph_attributes = True
        graph_attribute = graph_attribute_file.readline()

    
    #go through the data and read out the graphs
    node_counter = 1
    #all node_id will start with 0 for all graphs
    node_id_subtractor = 1
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
                        G.add_node(node_counter - node_id_subtractor, label = attributes_to_np_array(node_label), attribute = attributes_to_np_array(node_attribute))
                        node_attribute = node_attribute_file.readline()
                        node_label = node_label_file.readline()
                    elif node_attributes:
                        G.add_node(node_counter - node_id_subtractor, attribute = attributes_to_np_array(node_attribute))
                        node_attribute = node_attribute_file.readline()
                    elif node_labels:
                        G.add_node(node_counter - node_id_subtractor, label = attributes_to_np_array(node_label))
                        node_label = node_label_file.readline()
                    else:
                        G.add_node(node_counter - node_id_subtractor)
                    node_counter += 1
                    graph = graph_indicator.readline() 
                else:
                    old_graph = graph 
                    new_graph = True
                    node_id_subtractor = node_counter

            if not new_graph:
                #set edge with possibly edge label and attributes and get next line
                if edge_labels and edge_attributes:
                    G.add_edge(int(edge[0]) - node_id_subtractor, int(edge[1]) - node_id_subtractor, label = attributes_to_np_array(edge_label), attribute = attributes_to_np_array(edge_attribute))
                    edge_attribute = edge_attribute_file.readline()
                    edge_label = edge_label_file.readline()
                elif  edge_labels:
                    G.add_edge(int(edge[0]) - node_id_subtractor, int(edge[1]) - node_id_subtractor, label = attributes_to_np_array(edge_label))
                    edge_label = edge_label_file.readline()
                elif edge_attributes:
                    G.add_edge(int(edge[0]) - node_id_subtractor, int(edge[1]) - node_id_subtractor, attribute = attributes_to_np_array(edge_attribute))
                    edge_attribute = edge_attribute_file.readline()
                else:
                    G.add_edge(int(edge[0]) - node_id_subtractor, int(edge[1]) - node_id_subtractor)
                    
                #get new edge
                edge = edge_file.readline()
                if edge:
                    edge = edge.strip().split(",")
    
        #add graph to list
        graph_list.append(G)
        
        #add graph label to list
        graph_label_list.append(int(graph_label))
        graph_label = graph_label_file.readline()
        
        #add graph attributes as numpy array
        if graph_attributes:        
            graph_attribute_list.append(attributes_to_np_array(graph_attributes))
            graph_attribute = graph_attribute_file.readline()
            
    #close all files
    edge_file.close()
    graph_indicator.close()
    graph_label_file.close()
    
    if node_labels:
        node_label_file.close()
    if edge_labels:
        edge_label_file.close()
    if edge_attributes:
        edge_attribute_file.close()
    if node_attributes:
        node_attribute_file.close()
    if graph_attributes:
        graph_attribute_file.close()
        
    #returns list of the graphs of the db, together with graph label list and possibly graph_attributes or an empty list of there are no attributes
    return (graph_list, graph_label_list, graph_attribute_list)

#node label from node_id
def node_label_vector(graph, node_id):
    '''
    Returns node labels from given graph and node

    :param graph: networkx graph
    :param node_id: id of the node for printing the label vector
    :return numpy array of node labels or empty array if there are no node labels
    '''

    if graph.has_node(node_id):
        node = graph.nodes(data = True)[node_id]
        if "label" in node.keys():
            label = node["label"]
            return label
        else:
            return np.array([])
    else:
        return np.array([])

#simple node label array from graph node labels
def nodes_label_matrix(graph):
    '''
    Returns node labels from given graph

    :param graph: networkx graph
    :return numpy array of node labels of the graph
    '''
    if "label" in graph.nodes(data = True)[0].keys():
        label_array = np.zeros((graph.number_of_nodes(), graph.nodes(data = True)[0]["label"].size))
        for i, node in enumerate(graph.nodes(data = True), 0):
            for j, entry in enumerate(node[1]["label"], 0):
                label_array[i][j] = entry 
        return label_array
    else:
        return np.array([])

#node label matrix with one hot coding, with a previous given size of coding, labels have to be of the form 0, 1, 2, 3, 4, 5, 6
def nodes_label_coding_matrix(graph, max_coding, zeros = True):
    '''
    Returns node labels from given graph and node

    :param graph: networkx graph
    :param max_coding: maximal size of the one hot coding of the node labels
    :param zeros: True if there should be zero columns in the one hot coding
    :return numpy array of one hot coded node labels of the graph if labels are given
    '''  

    try:
        if graph.nodes(data = True)[0]["label"].size != 1:
            raise ValueError("Node label coding not possible because of multidimensional node labels")
    except ValueError:
        exit("Node label coding not possible because of multidimensional node labels")
        
    if "label" in graph.nodes(data = True)[0].keys():
        if not zeros:
            max = 0
            for node in graph.nodes(data = True):
                label = int(node[1]["label"])
                if label > max:
                    max = label
            
            if max_coding < max + 1:
                label_mat = np.zeros((graph.number_of_nodes(), max_coding))
            else:
                label_mat = np.zeros((graph.number_of_nodes(), max + 1))
            for i, node in enumerate(graph.nodes(data = True), 0):
                num = int(node[1]["label"])
                if num >= 0 and num < max_coding:
                    label_mat[i][num] = 1
            return label_mat            
        else:
            label_mat = np.zeros((graph.number_of_nodes(), max_coding))
            for i, node in enumerate(graph.nodes(data = True), 0):
                num = int(node[1]["label"])
                if num >= 0 and num < max_coding:
                    label_mat[i][num] = 1
            return label_mat
    else:
        return np.array([])


def node_attribute_vector(graph, node_id):
    '''
    Returns attributes of a node as numpy array

    :param graph: networkx graph
    :param node_id: id of the node for printing the label vector
    :return numpy array of node attributes or empty array if there are no node attributes
    '''
    
    node = graph.nodes(data = True)[node_id]
    if "attribute" in node.keys():
        label_mat = node["attribute"]
        return label_mat
    else:
        return np.array([])

#node attribute matrix 
def nodes_attribute_matrix(graph):
    '''
    Returns attributes of a node as numpy array

    :param graph: networkx graph
    :return numpy array of node attributes or empty array if there are no node attributes
    '''
    
    if "attribute" in graph.nodes(data = True)[0].keys():
        label_mat = np.zeros((graph.number_of_nodes(), graph.nodes(data = True)[0]["attribute"].size))
        for i, node in enumerate(graph.nodes(data = True), 0):
            arr = node[1]["attribute"]
            for j in range(0, len(arr)):
                label_mat[i][j] = arr[j]
        return label_mat
    else:
        return np.array([])

#edge label from node_ids
def edge_label_vector(graph, node_i, node_j):
    '''
    Returns edge labels from given graph and edge

    :param graph: networkx graph
    :param node_i: head of edge
    :param node_i: tail of edge
    :return numpy array of edge labels or empty array if there are no edge labels
    '''

    if graph.has_edge(node_i, node_j):
        edge = graph.get_edge_data(node_i, node_j)
        if "label" in edge.keys():
            label = edge["label"]
            return label
        else:
            return np.array([])
    else:
        return np.array([])

#edge label from node_ids
def edges_label_matrix(graph):
    '''
    Returns all edge labels from given graph

    :param graph: networkx graph
    :return numpy array of all edge labels or empty array if there are no edge labels
    '''

    if len(graph.edges) != 0:
        edge = next(iter(graph.edges(data = True)))
        if "label" in edge[2].keys():
            label_mat = np.zeros((graph.number_of_edges(), edge[2]["label"].size))
            
            for i, edge in enumerate(graph.edges(data = True), 0):
                if "label" in edge[2].keys():
                    label = edge[2]["label"]
                    for j, entry in enumerate(label, 0):
                        label_mat[i][j] = entry
                else:
                    return np.array([])
            return label_mat
        else:
            return np.array([])    
    else:
        return np.array([])
    

#node label matrix with one hot coding, with a previous given size of coding, labels have to be of the form 0, 1, 2, 3, 4, 5, 6
def edges_label_coding_matrix(graph, max_coding, zeros = True):
    '''
    Returns edge label one hot coded from given graph

    :param graph: networkx graph
    :param max_coding: maximal size of the one hot coding of the edge labels
    :param zeros: True if there should be zero columns in the one hot coding
    :return numpy array of one hot coded edge labels of the graph if labels are given
    '''  
    if len(graph.edges) != 0:
        edge = next(iter(graph.edges(data = True)))
        if "label" in edge[2].keys():

            try:
                if edge[2]["label"].size != 1:
                    raise ValueError("Edge label coding not possible because of multidimensional edge labels")
            except ValueError:
                exit("Edge label coding not possible because of multidimensional node labels")
                

            if not zeros:
                max = 0
                for edge in graph.edges(data = True):
                    label = int(edge[2]["label"])
                    if label > max:
                        max = label
                
                if max_coding < max + 1:
                    label_mat = np.zeros((graph.number_of_edges(), max_coding))
                else:
                    label_mat = np.zeros((graph.number_of_edges(), max + 1))
                for i, edge in enumerate(graph.edges(data = True), 0):
                    num = int(edge[2]["label"])
                    if num >= 0 and num < max_coding:
                        label_mat[i][num] = 1
                return label_mat            
            else:
                label_mat = np.zeros((graph.number_of_edges(), max_coding))
                for i, edge in enumerate(graph.edges(data = True), 0):
                    num = int(edge[2]["label"])
                    if num >= 0 and num < max_coding:
                        label_mat[i][num] = 1
                return label_mat
        else:
            return np.array([])    
    else:
        return np.array([])    

        
def edge_attribute_vector(graph, node_i, node_j):
    '''
    Returns attributes of a edge as numpy array

    :param graph: networkx graph
    :return numpy array of edge attributes or empty array if there are no edge attributes
    '''

    if graph.has_edge(node_i, node_j) and "attribute" in graph.edges[node_i, node_j].keys():
        label_mat = graph.edges[node_i, node_j]["attribute"]
        return label_mat
    else:
        return np.array([])

#edge label from node_ids
def edges_attribute_matrix(graph):
    '''
    Returns all edge labels from given graph

    :param graph: networkx graph
    :return numpy array of all edge attributes or empty array if there are no edge attributes
    '''

    if len(graph.edges) != 0:
        edge = next(iter(graph.edges(data = True)))
        if "attribute" in edge[2].keys():
            label_mat = np.zeros((graph.number_of_edges(), edge[2]["attribute"].size))
            
            for i, edge in enumerate(graph.edges(data = True), 0):
                if "attribute" in edge[2].keys():
                    label = edge[2]["attribute"]
                    for j, entry in enumerate(label, 0):
                        label_mat[i][j] = entry
                else:
                    return np.array([])
            return label_mat
        else:
            return np.array([])    
    else:
        return np.array([])


def array_to_str(array):
    '''
    Prints an array to some string representation

    :param array: numpy array of numbers
    :return str_: string from array
    '''

    str_ = ""
    for x in array:
        str_ += str(x)
        str_ += " "
    return str_
    
    
    

def draw_graph(graph):
    '''
    Draws a graph with given node and edge labels

    :param graph: networkx graph to draw
    :return None:
    '''

    pos = nx.nx_pydot.graphviz_layout(graph)
    nx.draw(graph, pos)
    
    
    node_labels = {}
    for (key, value) in graph.nodes(data = True):
        if "label" in value:
            node_labels[key] = array_to_str(value["label"])
        else:
            node_labels[key] = ""
    
    nx.draw_networkx_labels(graph, pos, labels = node_labels)
    
    edge_labels = {}
    for (key1, key2, value) in graph.edges(data = True):
        if "label" in value:
            edge_labels[(key1, key2)] = int(value["label"])
        else:
            edge_labels[(key1, key2)] = ""
    nx.draw_networkx_edge_labels(graph, pos, edge_labels = edge_labels)
    pyplot.show()
    
def draw_graph_labels(graph, node_labels = None, edge_labels = None):
    '''
    Draws a graph with manually assigned node and edge labels    

    :param graph: networkx graph to draw
    :param node_labels: list of node labels to print at the nodes of the graph if not None
    :param edge_labels: list of triples (node1, node2, value) for edge labels of edge (node1, node2) to print at the edges of the graph if not None
    :return None:
    '''
    
    pos = nx.nx_pydot.graphviz_layout(graph)
    nx.draw(graph, pos)
    
    if node_labels is not None:
        try:
            if graph.number_of_nodes() != len(node_labels):
                raise ValueError("Node labels length and graph number of nodes do not fit together")
            
        except ValueError:
            exit("Node labels length and graph number of nodes do not fit together")
        
        nx.draw_networkx_labels(graph, pos, labels = {key: value for key, value in enumerate(node_labels, 0)})
    
    if edge_labels is not None:
        try:
            if graph.number_of_edges() != len(edge_labels):
                raise ValueError("Edge labels length and graph number of edges do not fit together")
            
        except ValueError:
            exit("Edge labels length and graph number of edges do not fit together")
    
        nx.draw_networkx_edge_labels(graph, pos, edge_labels = {(key1, key2): value for (key1, key2, value) in edge_labels})

    pyplot.show()
    
    
def example_graph():
    graph = nx.Graph()
    for i in range(0, 4):
        graph.add_node(i, label = attributes_to_np_array("0"))
    for i in range(4, 6):
        graph.add_node(i, label = attributes_to_np_array("1"))
    graph.add_edge(0, 4)
    graph.add_edge(1, 4)
    graph.add_edge(2, 5)
    graph.add_edge(3, 5)
    graph.add_edge(4, 5)
    return graph




