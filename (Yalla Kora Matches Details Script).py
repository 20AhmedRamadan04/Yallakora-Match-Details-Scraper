import requests
from bs4 import BeautifulSoup as BS
import csv

date = input("Please Enter The Needed Date For Scraping In The Following Format mm/dd/yy: ")
page = requests.get(f"https://www.yallakora.com/match-center/مركز-المباريات?date={date}")

def main(page):
    src = page.content
    soup = BS(src, "lxml")
    matches_details = []
    championships = soup.find_all("div", {"class": "matchCard"})

    def get_match_info(championship):
        championship_title = championship.find("h2").text.strip()
        all_matches = championship.find_all("div", {"class": "item finish liItem"})
        number_of_matches = len(all_matches)

        for i in range(number_of_matches):
            # Teams Names
            team_A = all_matches[i].find("div", {"class": "teamA"}).text.strip()
            team_B = all_matches[i].find("div", {"class": "teamB"}).text.strip()

            # Match Scores
            match_score = all_matches[i].find("div", {"class": "MResult"}).find_all("span", {"class": "score"})
            score = f"{match_score[0].text.strip()} - {match_score[1].text.strip()}"  # Correctly format score
            str(score)

            # Match Time
            match_time = all_matches[i].find("div", {"class": "MResult"}).find("span", {"class": "time"}).text.strip()

            # Add Details To Match Details List
            matches_details.append({"نوع البطوله": championship_title, "الفريق الأول": team_A, "الفريق الثاني": team_B, "موعد المباراة": match_time, "نتيجة المباراة": score})

    for championship in championships:
        get_match_info(championship)

    keys = matches_details[0].keys()
    with open(f"matches_details_{date.replace('/', '-')}.csv", "w", newline='', encoding='utf-8-sig') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(matches_details)
        print("File Created")

main(page)