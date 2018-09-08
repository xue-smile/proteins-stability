
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import csv

def saveHistogram(values, filename='histogram.png', dpi=300,  title='Histogram', xlabel='Values', ylabel='Counts', bins=20, rwidth=0.9, color='#607c8e', grid=True, ygrid=True, alpha=0.75, xlim=(0, 1)):
    commutes = pd.Series(np.array(values))

    commutes.plot.hist(grid=grid, bins=bins, rwidth=rwidth,
                    color=color)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    if ygrid:
        plt.grid(axis='y', alpha=alpha)
    plt.savefig(filename, dpi=dpi)
    plt.xlim(xlim)
    plt.close()


def saveScatterPlots(dataset, filename):
    #g = sns.PairGrid(iris, hue="species")
    #g = sns.PairGrid(dataset, hue="class", height=2.5)
    print(dataset.columns)
    genes = dataset.columns.tolist()
    
    genes.remove('class')
    print(genes)
    sns.set(style="ticks")
    #g = sns.PairGrid(dataset, hue="class", vars=genes, hue_kws={"cmap": ["Blues", "Greens", "Reds"]}) #palette="Set2",
    g = sns.pairplot(dataset, hue="class", vars=genes)#, hue_kws={"cmap": ["Blues", "Greens", "Reds"]})
    #g.map_diag(plt.scatter)
    #g = g.map_diag(sns.kdeplot)
    #g = g.map_diag(sns.kdeplot, lw=3, legend=False)
    #g = g.map_lower(plt.scatter)
    g = g.map_upper(sns.kdeplot) 
    g.savefig(filename, dpi=300)
    plt.close()

def saveHeatMap(matrix, rows_labels, cols_labels, filename, metric='correlation', xticklabels=False):
    dataset = pd.DataFrame(matrix, index=rows_labels, columns=cols_labels)

    g = sns.clustermap(dataset, metric=metric, xticklabels=xticklabels)
    g.savefig(filename, dpi=300)
    plt.close()


#todo save rank
def saveRank(scores, filename):
    #scores tuple (score, index, name)
    with open(filename, 'w') as f:
        f.write("index,name,score\n")
        for i in range(len(scores)):
            item = scores[i]
            f.write('%d,%s,%f\n' % (item[1], item[2], item[0]))   
        f.close()


def normalizeScores(scores):
    maximum = max(scores,key=lambda item:item[0])[0]
    minimum = min(scores,key=lambda item:item[0])[0]
    delta = maximum - minimum
    if delta == 0:
        return scores

    new_scores = []
    for score in scores:
        new_scores.append(((score[0]-minimum)/delta,score[1],score[2]))

    return new_scores


def getMaxNumberOfProteins(scores, maxNumberOfProteins):
    non_zeros = 0
    for score in scores:
        if score[0] > 0:
            non_zeros +=1
    return min([non_zeros,maxNumberOfProteins])

def saveMatrix(matrix, csvfilepath):
    #Assuming res is a list of lists
    with open(csvfilepath, "w") as output:
        writer = csv.writer(output, lineterminator='\n')
        writer.writerows(matrix)