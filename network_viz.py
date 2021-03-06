'''
Created on Tue Aug 27 2014

@author: wronk

network_viz.py
'''
import numpy as np
import matplotlib.pyplot as plt
from os import path as op


def plot_3D_network(node_names, node_positions, node_label_set, edges,
                    edge_label_set, node_sizes=None, node_colors=None,
                    node_alpha=None, edge_sizes=None, edge_colors=None,
                    edge_alpha=None, save_fpath=None):
    '''
    Plot clustering coefficient probability density function

    Parameters
    ----------
    node_names : list
        matrix of clustering coefficients
    node_positions : N x 3 array
        array of positions
    edges : list
        connections between nodes
    node_label_set : list of bool
        whether or not to text label the nodes
    edges : list of tuples
        edges between nodes (use graph.edges())
    edge_label_set : list of bool
        whether or not to label the edges
    node_sizes : list | None
        size of each node's marker in the graph
    node_colors : list | None
        color of each node's marker
    edge_sizes : list | None
        size of each edge's line
    edge_colors : list | None
        color of each edge's line
    save_fpath : str | None
        name of filepath to save images (if not None)

    Returns
    --------
    fig : fig
        figure object of distribution histogram for plotting
    ax : ax
        figure axis
    '''

    # Png params
    elev = 20.  # elevation angle for movie

    # Initialize figure
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d', axisbg='black')
    fig.set_facecolor('black')
    node_label_offset = 0.05
    edge_label_offset = 0.05

    ###################################

    if node_sizes is None:
        node_sizes = [50] * len(node_names)
    if node_colors is None:
        node_colors = ['green'] * len(node_names)
    if node_alpha is None:
        node_alpha = [1.] * len(node_names)
    if edge_sizes is None:
        edge_sizes = [1] * len(edges)
    if edge_colors is None:
        edge_colors = ['blue'] * len(edges)
    if edge_alpha is None:
        edge_alpha = [1.] * len(edges)

    ###################################
    # Add nodes to graph
    for ni, node_pt in enumerate(node_positions):
        ax.scatter(node_pt[0], node_pt[1], node_pt[2],
                   s=node_sizes[ni], c=node_colors[ni],
                   alpha=node_alpha[ni], depthshade=False, lw=0)
        if node_label_set[ni]:
            ax.text(node_positions[ni, 0], node_positions[ni, 1],
                    node_positions[ni, 2] + node_label_offset, node_names[ni],
                    color=node_colors[ni], alpha=node_alpha[ni], ha='center')

    ###################################
    # Convert edges to list
    edge_inds = [[node_names.index(n1), node_names.index(n2)]
                 for n1, n2 in edges]

    # Generate list of 2 x 3 array corresponding to list of end edge points
    edge_positions = [np.vstack((node_positions[e[0]], node_positions[e[1]]))
                      for e in edge_inds]

    ###################################
    # Add edges to graph
    for ei, edge_pt in enumerate(edge_positions):
        ax.plot(edge_pt[:, 0], edge_pt[:, 1], edge_pt[:, 2],
                lw=edge_sizes[ei], c=edge_colors[ei],
                alpha=edge_alpha[ei], dash_capstyle='round', zorder=-1)

        # Add text edge label to graph
        if edge_label_set[ei]:
            mean_pt = np.mean(edge_pt, axis=0)
            vec_dir = edge_pt[1, :] - edge_pt[0, :]

            ax.text(mean_pt[0], mean_pt[1], mean_pt[2] + edge_label_offset,
                    node_names[edge_inds[ei][0]] + '<->' +
                    node_names[edge_inds[ei][1]], vec_dir,
                    alpha=edge_alpha[ei], color=edge_colors[ei], ha='center')

    # Cleanup
    ax.set_xlabel('A <-> P')
    ax.set_ylabel('L <-> M <-> L')
    #ax.set_zlabel('S <-> I')
    ax.set_axis_off()

    ax.set_title('Top Clustering Coefficients')

    if(save_fpath is not None):
        for ai, ang in enumerate(np.arange(-270, 90, 3)):
            ax.view_init(elev=elev, azim=ang)
            plt.savefig(op.join(save_fpath, 'mov_%03i.png' % ai), ec='black',
                        fc='black', bbox_inches='tight', pad_inches=0.)

    return fig, ax

if __name__ == '__main__':

    import network_gen

    plt.close('all')
    plt.ion()

    # Set parameters
    p_th = .01  # P-value threshold
    w_th = 0  # Weight-value threshold

    # Set relative directory path
    dir_name = '../friday-harbor/linear_model'

    # Load weights & p-values
    W, P, row_labels, col_labels = network_gen.load_weights(dir_name)
    # Threshold weights according to weights & p-values
    W_net, mask = network_gen.threshold(W, P, p_th=p_th, w_th=w_th)
    # Set weights to zero if they don't satisfy threshold criteria
    W_net[W_net == -1] = 0.
    # Set diagonal weights to zero
    np.fill_diagonal(W_net, 0)

    # Put everything in a dictionary
    W_net_dict = {'row_labels': row_labels, 'col_labels': col_labels,
                  'data': W_net}
    G = network_gen.import_weights_to_graph(W_net_dict, directed=True)

    node_names = row_labels[0:5]
    node_positions = np.random.rand(5, 3)
    node_labels = [True] * len(node_names)
    edges = [('AAA_L', 'ACAv_L'), ('AD_L', 'ACAd_L')]

    node_sizes = np.random.randint(20, high=300, size=len(node_names))
    node_colors = ['green'] * len(node_names)
    node_alpha = list(np.arange(.1, 1., 1. / len(node_names)))

    edge_sizes = np.random.randint(1, high=4, size=len(edges))
    edge_colors = ['blue'] * len(edges)
    edge_labels = [False] * len(edges)
    edge_alpha = list(np.arange(.1, 1., 1. / len(node_names)))

    fig, ax = plot_3D_network(node_names, node_positions, node_labels, edges,
                              edge_labels, node_sizes, node_colors, node_alpha,
                              edge_sizes, edge_colors, edge_alpha, False)
    fig, ax = plot_3D_network(node_names, node_positions, node_labels, edges,
                              edge_labels)

    plt.draw()
    plt.show()
