# -*- coding: utf-8 -*-
"""
Created on Wed Sep  3 15:06:56 2014

@author: sid
"""

import networkx as nx
import plot_net
import matplotlib.pyplot as plt; plt.close('all')
import numpy as np
import network_gen
from networkx.generators.classic import empty_graph
import aux_random_graphs

import standard_graphs

plot_functions = True
LogLogPlot = False
PLOT_HISTS = False
plot_twoplots = False

RGCs = {'Brain':'k','ER':'b','WS':'g','BA':'r','PWC':'c','BIO':'m'}
FontSize = 20

# Set parameters
p_th = .01 # P-value threshold
w_th = 0 # Weight-value threshold

# Set relative directory path
dir_name = 'friday-harbor/linear_model'
#dir_name = '../Data/linear_model'

# Load weights & p-values
W,P,row_labels,col_labels = network_gen.load_weights(dir_name)
# Threshold weights according to weights & p-values
W_net,mask = network_gen.threshold(W,P,p_th=p_th,w_th=w_th)
# Set weights to zero if they don't satisfy threshold criteria
W_net[W_net==-1] = 0.
# Set diagonal weights to zero
np.fill_diagonal(W_net,0)

# Put everything in a dictionary
W_net_dict = {'row_labels':row_labels,'col_labels':col_labels,
              'data':W_net}

# Convert to networkx graph object
G = network_gen.import_weights_to_graph(W_net_dict)

N = len(G.nodes())

# These are the new params, derived from adjusting the proverbial knobs
G_ER = nx.erdos_renyi_graph(N,0.087)
G_WS = nx.watts_strogatz_graph(N,36,0.159)
G_BA = standard_graphs.symmetric_BA_graph(N,20,0.52)
#G_BA = nx.barabasi_albert_graph(N,19)
G_PWC = nx.powerlaw_cluster_graph(N,19,1)
print 'Generating biophysical graph...'
G_BIO,A,D = aux_random_graphs.biophysical_graph(N=426,N_edges=7804,L=1.,power=1.5,mode=0)

if plot_functions:
    
    # Here you can specify which plotting function you want to run.
    # It needs to take a single graph as input!
    plotfunction = plot_net.plot_clustering_coeff_pdf
        
    Fig, axs = plt.subplots(2,2, facecolor=[1,1,1])
    
    plotfunction(axs[0,0],G)
    #plotfunction(axs[0,1],G_PWC)
    plotfunction(axs[0,1],G_ER)
    plotfunction(axs[1,0],G_BA)
    plotfunction(axs[1,1],G_WS)
    
    titlesize=35
    labelsize=28
    ticksize=20
    axs[0,0].set_title('Allen Mouse Brain Atlas (LM)', fontsize=titlesize)
    axs[0,1].set_title('Erdos_Renyi', fontsize=titlesize)
    axs[1,0].set_title('Symmetric Barabasi-Albert', fontsize=titlesize)
    axs[1,1].set_title('Watts-Strogatz graph', fontsize=titlesize)

    
    xLims = [axs[0,0].get_xlim(), axs[0,1].get_xlim(), axs[1,0].get_xlim(), axs[1,1].get_xlim()]
    yLims = [axs[0,0].get_ylim(), axs[0,1].get_ylim(), axs[1,0].get_ylim(), axs[1,1].get_ylim()]
    
    xLims = [i for entry in xLims for i in entry]
    yLims = [i for entry in yLims for i in entry]
    
    #xLims = sorted(xLims,reverse=True)
    #yLims = sorted(yLims,reverse=True)
    
    #xLims = xLims[0:len(xLims)]
    #yLims = yLims[0:len(yLims)]
    
    xticks = np.linspace(0,max(xLims),5)
    yticks = np.linspace(0,max(yLims),5)
    
    for i in [0,1]:
        for j in [0,1]:
            xlab = ''
            ylab = ''
            
            #axs[i,j].set_title('')
            
            axs[i,j].set_xlim(min(xLims), max(xLims))
            axs[i,j].set_ylim(min(yLims), max(yLims))
            
            axs[i,j].set_xticks(xticks)
            axs[i,j].set_yticks(yticks)
            
            
            xticklabels = axs[i,j].get_xticks()
            yticklabels = axs[i,j].get_yticks()
            
            #axs[i,j].set_facecolor()
            axs[i,j].set_xlabel(xlab, fontsize=labelsize)
            axs[i,j].set_ylabel(ylab, fontsize=labelsize)
            axs[i,j].set_xticklabels(xticklabels, fontsize=ticksize)
            axs[i,j].set_yticklabels(yticklabels, fontsize=ticksize)

    myrange = np.linspace(0,0.002,50)

    plt.show()
    

if LogLogPlot:
    G_deg = G.degree()
    G_ER_deg = G_ER.degree()
    G_WS_deg = G_WS.degree()
    G_BA_deg = G_BA.degree()
    G_PWC_deg = G_PWC.degree()
    G_BIO_deg = G_BIO.degree()
    
    n_bins = 20
    Bins = np.linspace(0,150,n_bins)
    
    G_bins = np.histogram(G_deg.values(),Bins)
    G_ER_bins = np.histogram(G_ER_deg.values(),Bins)
    G_WS_bins = np.histogram(G_WS_deg.values(),Bins)
    G_BA_bins = np.histogram(G_BA_deg.values(),Bins)
    G_PWC_bins = np.histogram(G_PWC_deg.values(),Bins)
    G_BIO_bins = np.histogram(G_BIO_deg.values(),Bins)
    
    fig,ax = plt.subplots(1,1,facecolor='white')
    
    ax.plot(np.log(G_bins[1][0:n_bins-1]),np.log(G_bins[0]),lw=3,c=RGCs['Brain'])
    ax.plot(np.log(G_ER_bins[1][0:n_bins-1]),np.log(G_ER_bins[0]),lw=3,c=RGCs['ER'])
    ax.plot(np.log(G_WS_bins[1][0:n_bins-1]),np.log(G_WS_bins[0]),lw=3,c=RGCs['WS'])
    ax.plot(np.log(G_BA_bins[1][0:n_bins-1]),np.log(G_BA_bins[0]),lw=3,c=RGCs['BA'])
    ax.plot(np.log(G_PWC_bins[1][0:n_bins-1]),np.log(G_PWC_bins[0]),lw=3,c=RGCs['PWC'])
    ax.plot(np.log(G_BIO_bins[1][0:n_bins-1]),np.log(G_BIO_bins[0]),lw=3,c=RGCs['BIO'])

    ax.legend(('Mouse brain', 'ER random', 'WS small-world', 'BA scale-free',
                'Power-law clustered','Biophysical'),prop={'size':16})

    ax.set_xlabel('log[degree]')
    ax.set_ylabel('log[occurrences]')

    for item in ([ax.title, ax.xaxis.label, ax.yaxis.label] +
                ax.get_xticklabels() + ax.get_yticklabels()):
                    item.set_fontsize(FontSize)

if PLOT_HISTS:
#<<<<<<< HEAD
    FontSize = 30
#=======
#>>>>>>> upstream/master
    # Plot degree histogram overlaid w/ random graph degree histograms
    bins = np.linspace(0,150,50)
    fig,ax = plt.subplots(1,1,facecolor='w')
    #plot_net.plot_degree_distribution(ax,G,bins=bins)
    plot_net.line_hist(ax,G_ER,'degree',bins=bins,c=RGCs['ER'],lw=3)
#<<<<<<< HEAD
    #plot_net.line_hist(ax,G_WS,'degree',bins=bins,c=RGCs['WS'],lw=3)
    #plot_net.line_hist(ax,G_BA,'degree',bins=bins,c=RGCs['BA'],lw=3)
    #plot_net.line_hist(ax,G_BA_cc,'degree',bins=bins,c=RGCs['BA_cc'],lw=3)
    ax.set_xticks([0,50,100,150])
    ax.set_ylim([0,10])
    ax.set_yticks([0,50,100,150,200,250])
#=======
    plot_net.line_hist(ax,G_WS,'degree',bins=bins,c=RGCs['WS'],lw=3)
    plot_net.line_hist(ax,G_BA,'degree',bins=bins,c=RGCs['BA'],lw=3)
    plot_net.line_hist(ax,G_PWC,'degree',bins=bins,c=RGCs['PWC'],lw=3)
    plot_net.line_hist(ax,G_BIO,'degree',bins=bins,c=RGCs['BIO'],lw=3)
#>>>>>>> upstream/master
    for item in ([ax.title, ax.xaxis.label, ax.yaxis.label] +
                ax.get_xticklabels() + ax.get_yticklabels()):
                    item.set_fontsize(FontSize)
    
    # Plot clustering coeff histogram overlaid w/ random graph histograms
    bins = np.linspace(0,1,50)
    fig,ax = plt.subplots(1,1,facecolor='w')
    plot_net.plot_clustering_coeff_pdf(ax,G,bins=bins)
    plot_net.line_hist(ax,G_ER,'ccoeff',bins=bins,c=RGCs['ER'],lw=3)
    plot_net.line_hist(ax,G_WS,'ccoeff',bins=bins,c=RGCs['WS'],lw=3)
    plot_net.line_hist(ax,G_BA,'ccoeff',bins=bins,c=RGCs['BA'],lw=3)
#<<<<<<< HEAD
    plot_net.line_hist(ax,G_BA_cc,'ccoeff',bins=bins,c=RGCs['BA_cc'],lw=3)
    ax.set_xticks([0,0.25,0.5,0.75,1])
#=======
    plot_net.line_hist(ax,G_PWC,'ccoeff',bins=bins,c=RGCs['PWC'],lw=3)
    plot_net.line_hist(ax,G_BIO,'ccoeff',bins=bins,c=RGCs['BIO'],lw=3)
#>>>>>>> upstream/master
    for item in ([ax.title, ax.xaxis.label, ax.yaxis.label] +
                ax.get_xticklabels() + ax.get_yticklabels()):
                    item.set_fontsize(FontSize)
    
    # Plot node-betweenness overlaid w/ random graph histograms
    bins = np.linspace(0,.02,50)
    fig,ax = plot_net.plot_node_btwn(G,bins=bins)
    plot_net.line_hist(ax,G_ER,'node_btwn',bins=bins,c=RGCs['ER'],lw=3)
    plot_net.line_hist(ax,G_WS,'node_btwn',bins=bins,c=RGCs['WS'],lw=3)
#<<<<<<< HEAD
    #plot_net.line_hist(ax,G_BA,'node_btwn',bins=bins,c=RGCs['BA'],lw=3)
    plot_net.line_hist(ax,G_BA_cc,'node_btwn',bins=bins,c=RGCs['BA_cc'],lw=3)
#=======
    plot_net.line_hist(ax,G_BA,'node_btwn',bins=bins,c=RGCs['BA'],lw=3)
    plot_net.line_hist(ax,G_PWC,'node_btwn',bins=bins,c=RGCs['PWC'],lw=3)
    plot_net.line_hist(ax,G_BIO,'node_btwn',bins=bins,c=RGCs['BIO'],lw=3)
#>>>>>>> upstream/master
    ax.set_xlim(0,.02)
    for item in ([ax.title, ax.xaxis.label, ax.yaxis.label] +
                ax.get_xticklabels() + ax.get_yticklabels()):
                    item.set_fontsize(FontSize)
                    
if plot_twoplots:
    pass