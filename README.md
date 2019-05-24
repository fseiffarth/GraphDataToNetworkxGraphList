# GraphDataToNetworkxGraphList

Reads graph data from:

https://ls11-www.cs.tu-dortmund.de/staff/morris/graphkerneldatasets

and outputs them as a list of python networkx graphs.

Functions:

graph_data_to_graph_list(path, db)
  
  #Takes database path {path} and database-name {db} and outputs the graph data in form of a triple:
  (graph_list, graph_labels, graph_attributes)

  graph_list: python list of networkx graphs with graph information given by the database
  
  graph_labels: python list of integers as the labels of the graphs according to the database
  
  graph_attributes: python list with additional attributes of the graphs according to the database or empty list if there are none

node_label_vector(graph, node_id)

node_attribute_vector(graph, node_id)
  
  #outputs vector of node_label/node_attributes of node with {node_id} in graph {graph}
 
nodes_label_matrix(graph)

nodes_attribute_matrix(graph)

  #same as above but outputs all labels/attributes of nodes of graph {graph}
  
edge_label(graph, node_i, node_j)

edge_attribute_matrix(graph, node_i, node_j)

  #outputs vector of edge_labels/edge_attributes of edge (node_i, node_j) in graph {graph}




Python example:

        path = "path_to_dbs"
        db = "DBLP_v1"
        graph_data = graph_data_to_graph_list(path, db)
        graph_list, graph_labels, graph_attributes = graph_data
