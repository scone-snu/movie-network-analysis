import pandas as pd
import ast

# ==================================== #
#        Movie Network Generator       #
# ==================================== #


# Movie Features
#   순번 영화명 감독 제작사 수입사 배급사 개봉일 영화유형 영화형태
#   국적 전국스크린수 전국매출액 전국관객수 서울매출액 서울관객수 장르 등급 영화구분
# + 주연, 조연

def load_data():
    movies_df = pd.read_excel("./data/dataset.xlsx")
    movies = movies_df.as_matrix()
    return movies

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


def generate_actor_network(dataset, output_path):

    movie_actor_df = pd.DataFrame(columns=['vertex1', 'vertex2'], index=None)
    index = 0;
    # for i in range(len(dataset)):
    for i in range(100):
        for j in range(len(dataset[i][3])):
            for k in range(j+1, len(dataset[i][3])):
                movie_actor_df.loc[index] = [dataset[i][3][j], dataset[i][3][k]]
                index = index + 1

    # movie_actor_df.to_csv("./out/network.csv", encoding='utf-16', index=False)
    movie_actor_df.to_csv(output_path, index=False)


def generate_actor_genre_network(data, dataset, output_path):

    movie_actor_genre_df = pd.DataFrame(columns=['vertex1', 'vertex2', 'vertex3'], index=None)
    index = 0;

    # for i in range(len(dataset)):
    for i in range(100):

        # handling 1 person 2 role
        actors = set();
        for j in range(len(dataset[i][3])):
            actors.add(dataset[i][3][j])

        actors_list = list(actors)
        for j in range(len(actors_list)):
            for k in range(j+1, len(actors_list)):
                movie_actor_genre_df.loc[index] = [actors_list[j], actors_list[k], data[i][15]]
                index = index + 1


        # for j in range(len(dataset[i][3])):
        #     for k in range(j+1, len(dataset[i][3])):
        #         movie_actor_genre_df.loc[index] = [dataset[i][3][j], dataset[i][3][k], data[i][15]]
        #         index = index + 1

    # movie_actor_df.to_csv("./out/network.csv", encoding='utf-16', index=False)

    movie_actor_genre_df.to_csv(output_path, index=False)


################################################################


def generate_actor_genre_information(data, dataset, output_path):

    movie_actor_genre_df = pd.DataFrame(columns=['actor', 'genre'], index=None)
    index = 0;
    # for i in range(len(dataset)):

    for i in range(len(dataset)):
        for j in range(len(dataset[i][3])):
            movie_actor_genre_df.loc[index] = [dataset[i][3][j], data[i][15]]
            index = index + 1

    # movie_actor_df.to_csv("./out/network.csv", encoding='utf-16', index=False)
    movie_actor_genre_df.to_csv(output_path, index=False)


def generate_movie_genre_information(data, dataset, output_path):

    movie_actor_genre_df = pd.DataFrame(columns=['movie', 'genre'], index=None)
    index = 0;
    # for i in range(len(dataset)):

    for i in range(len(data)):
        movie_actor_genre_df.loc[index] = [data[i][1], data[i][15]]
        index = index + 1

    # movie_actor_df.to_csv("./out/network.csv", encoding='utf-16', index=False)
    movie_actor_genre_df.to_csv(output_path, index=False)

def calc_data(data, dataset):
    index = 0;

    sum = 0;
    for i in range(len(dataset)):
        actor_num = 0;
        for j in range(len(dataset[i][3])):
            actor_num += 1;
        print(actor_num)
        sum = sum + actor_num;
        index = index + 1

    print(sum)


def main():

    # Load dataset
    data = load_data()
    dataset = load_dataset()

    # for i in range(len(dataset)):
    #     print(dataset[i])

    output_path = "./out/network_genre_final.csv"
    # generate_actor_network(dataset, output_path)
    # generate_actor_genre_network(data, dataset, output_path)
    # generate_actor_genre_information(data, dataset, output_path)

    calc_data(data, dataset)



print("============="); print("    START    "); print("=============");
if __name__ == '__main__':
    main()
print("============="); print("    E N D    "); print("=============");
