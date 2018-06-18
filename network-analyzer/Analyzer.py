import pandas as pd
import ast

import collections
import matplotlib.pyplot as plt
import networkx as nx



# =================================== #
#        Movie Network Analyzer       #
# =================================== #

# http://www.kobis.or.kr/kobis/business/mast/mvie/searchMovieList.do

def load_dataset():
    movie_actor_df = pd.read_csv('./data/movie_actor_utf16.csv', encoding='utf-16')
    # movie_actor_df = pd.read_csv('./data/movie_actor_crawled.csv', encoding='utf-16')

    dataset = []
    main_actor_series = movie_actor_df['main_actor']
    sub_actor_series = movie_actor_df['sub_actor']
    # main_actor_series = movie_actor_df['lead_role']
    # sub_actor_series = movie_actor_df['supp_role']

    for i in range(movie_actor_df.shape[0]):
        row = []
        row.append(movie_actor_df.ix[i].values[0])
        row.append(movie_actor_df.ix[i].values[1])
        row.append(movie_actor_df.ix[i].values[2])
        row.append(ast.literal_eval(main_actor_series[i]))
        row.append(ast.literal_eval(sub_actor_series[i]))
        dataset.append(row)

    return dataset


def actors_numbers(dataset):

    actors = set()
    main_actors = set()
    sub_actors = set()

    for i in range(len(dataset)):
        for j in range(len(dataset[i][3])):
            # print(dataset[i][3][j])
            actors.add(dataset[i][3][j])
            main_actors.add(dataset[i][3][j])
        for j in range(len(dataset[i][4])):
            # print(dataset[i][4][j])
            actors.add(dataset[i][4][j])
            sub_actors.add(dataset[i][4][j])

    print(len(main_actors), len(sub_actors), len(actors))


def calc_actors_degree(dataset):
    G = nx.Graph()

    for i in range(len(dataset)):
        for j in range(len(dataset[i][3])):
            G.add_node(dataset[i][3][j])
            for k in range(j+1, len(dataset[i][3])):
                G.add_nodes_from([dataset[i][3][j],dataset[i][3][k]])

    degree_sequence = sorted([d for n, d in G.degree()], reverse=True)
    degreeCount = collections.Counter(degree_sequence)
    deg, cnt = zip(*degreeCount.items())
    fig, ax = plt.subplots()
    plt.bar(deg, cnt, width=0.80, color='b')
    plt.title("Degree Histogram")
    plt.ylabel("Count")
    plt.xlabel("Degree")
    ax.set_xticks([d + 0.4 for d in deg])
    ax.set_xticklabels(deg)
    # draw graph in inset
    plt.axes([0.4, 0.4, 0.5, 0.5])
    Gcc = sorted(nx.connected_component_subgraphs(G), key=len, reverse=True)[0]
    pos = nx.spring_layout(G)
    plt.axis('off')
    nx.draw_networkx_nodes(G, pos, node_size=20)
    nx.draw_networkx_edges(G, pos, alpha=0.4)
    plt.show()



def calc_number_of_movies(dataset):
    pass



def main():

    # Load dataset
    dataset = load_dataset()
    actors_numbers(dataset)
    calc_actors_degree(dataset)


    # for i in range(len(dataset)):
    #     print(dataset[i])



print("============="); print("    START    "); print("=============");
if __name__ == '__main__':
    main()
print("============="); print("    E N D    "); print("=============");
