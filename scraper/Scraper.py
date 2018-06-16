
'''
Author: Jiho Choi

Requirements:
    - python3, selenium
    - Chrome WebDriver
    - # BeautifulSoup
    - # PhantomJS

References:
    - https://youtu.be/eDrFWRi13DY
    - https://beomi.github.io/2017/02/27/HowToMakeWebCrawler-With-Selenium/

Notes:
    Selenium (Web Testing Tool) is used instead of BeautifulSoup (and Request) to feed the inputs.
'''

from selenium import webdriver

import sys
import csv
import re

import pandas as pd

import codecs # For Korean

# =================================== #
# Korean Movie Data Scraper (Crawler) #
# =================================== #


def load_data(filepath):
    data = []
    reader = csv.reader(open(filepath, 'r'), delimiter=',')
    try:
        for entry in reader:
            data.append(entry)
    except:
        print("Error: loading data")
    return data


def main():

    # Chrome WebDriver
    chrome_driver_path = "/Users/Jiho/Desktop/movie-network-analysis/scraper/chromedriver"
    driver = webdriver.Chrome(chrome_driver_path)
    # Load drivers
    driver.implicitly_wait(3)

    # Visit the web page
    driver.get("http://www.kobis.or.kr/kobis/business/mast/mvie/searchMovieList.do")


    input_path = "./data/movie_title_director.csv" # Relative Path
    # output_path = "./data/movie_actor.csv"

    movies = load_data(input_path)
    # ouput_file = open(output_path, 'wb')
    # ouput_file = codecs.open(output_path, 'w', 'utf-8')

    movie_actor_df = pd.DataFrame(columns=['index', 'movie', 'director', 'lead_role', 'supp_role'], index=None)

    index = 0;
    for movie in movies:
        index = index + 1;
        print("------------------------------------")
        print(index, " ", movie[1], " ", movie[2])
        print("------------------------------------")

        movie_title = movie[1]
        director_name = movie[2]

        # Insert the keywords
        driver.find_elements_by_name('sMovName')[1].send_keys(movie_title);
        driver.find_element_by_name('sDirector').send_keys(director_name);

        # Click the search button
        driver.find_elements_by_xpath("//button[@class='btn_type03']")[0].click()
        driver.find_element_by_link_text(movie_title).click()

        # Casting
        sections = driver.find_elements_by_xpath("//*[@class='peopContTable']")

        print("-------------------------")

        # Casting
        lead_role = []
        supp_role = []

        for cell in sections[0].find_elements_by_tag_name("a"):
            name = cell.text
            name = re.sub(r'\([^)]*\)', '', name)
            name = name.replace(" ", "")
            name = name.replace(")", "")
            lead_role.append(name)
            print(cell.text, " -> ", name)

        print(lead_role)

        print("-------------------------")
        # Casting : supporting role
        for cell in sections[1].find_elements_by_tag_name("a"):
            name = cell.text
            name = re.sub(r'\([^)]*\)', '', name)
            name = name.replace(" ", "")
            name = name.replace(")", "")
            supp_role.append(name)
            print(cell.text, " -> ", name)

        print(supp_role)

        print("-------------------------")

        # Write to file
        # row_output = str(index) + ', ' + movie[1] + ', ' + movie[2] + ', ' + str(lead_role) + ', ' + str(supp_role) + '\n'
        # print(output_string)
        # output_string = output_string.encode("utf-8")
        # ouput_file.write(output_string)

        movie[1].replace(" ", "")
        movie[1].replace(",", "")

        # Pandas
        row_output = [index, movie[1], movie[2], lead_role, supp_role]
        movie_actor_df.loc[index] = row_output

        # Close the current window
        driver.find_elements_by_xpath("//img[@alt='레이어 팝업 닫기']")[0].click()
        driver.find_elements_by_name('sMovName')[1].clear();
        driver.find_element_by_name('sDirector').clear();

        # if index == 2:
        #     break;

    movie_actor_df.to_csv('./data/movie_actor.csv',encoding='utf-16',index =False)
    # ouput_file.close();


print("============="); print("    START    "); print("=============");
if __name__ == '__main__':
    main()
    # print(re.sub(r'\([^)]*\)', '', "최민식(이순신 )"))
    # print(re.sub(r'\([^)]*\)', '', "최민식"))
    # print("최민식(이순신 )")
print("============="); print("    E N D    "); print("=============");







