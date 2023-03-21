from prettytable import PrettyTable
import requests
from bs4 import BeautifulSoup

def toto_check():
    url = "https://www.singaporepools.com.sg/en/product/sr/Pages/toto_results.aspx"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    jackpotPrize = int(soup.find('td', class_='jackpotPrize').text.strip().replace(",", "").replace("$", ""))
    print(f"Jackpot Prize: ${jackpotPrize}")

    draw_results = set()

    for winning_numbers in soup.find_all('td', width="16%"):
        draw_results.update(map(int, winning_numbers.text.split(',')))
    
    additional_number = soup.find('td', class_='additional').text
    draw_results.add(int(additional_number))

    print(f"\033[0;31mDraw Results: {draw_results} \033[00m")
    print()

    Group1 = []
    Group2 = []
    Group3 = []
    Group4 = []
    Group5 = []
    Group6 = []

    with open("numbers.txt", "r") as f:
        for line in f:
            ticket_numbers = set(map(int, line.strip().split(",")))
            match = draw_results.intersection(ticket_numbers)
            counter = len(match)
            if counter == 6:
                if int(additional_number) not in match:
                    Group1.append(ticket_numbers)
                else:
                    Group2.append(ticket_numbers)
            elif counter == 5:
                if int(additional_number) in match:
                    Group4.append(ticket_numbers)
                else:
                    Group3.append(ticket_numbers)
            elif counter == 4:
                if int(additional_number) in match:
                    Group6.append(ticket_numbers)
                else:
                    Group5.append(ticket_numbers)

    if Group1:
        print("\033[0;32m" + "In Group 1, your winning bets are: " + "\033[00m")
        x = PrettyTable()
        for i in range(0, len(Group1), 5):
            row = []
            for j in range(5):
                if i+j < len(Group1):
                    row.append(Group1[i+j])
                else:
                    row.append("-")
            x.add_row(row)
        print(x)
        print()
    if Group2:
        print("\033[0;32m" + "In Group 2, your winning bets are: " + "\033[00m")
        x = PrettyTable()
        for i in range(0, len(Group2), 5):
            row = []
            for j in range(5):
                if i+j < len(Group2):
                    row.append(Group2[i+j])
                else:
                    row.append("-")
            x.add_row(row)
        print(x)
        print()
    if Group3:
        print("\033[0;32m" + "In Group 3, your winning bets are: " + "\033[00m")
        x = PrettyTable()
        for i in range(0, len(Group3), 5):
            row = []
            for j in range(5):
                if i+j < len(Group3):
                    row.append(Group3[i+j])
                else:
                    row.append("-")
            x.add_row(row)
        print(x)
        print()
    if Group4:
        print("\033[0;32m" + "In Group 4, your winning bets are: " + "\033[00m")
        x = PrettyTable()
        for i in range(0, len(Group4), 5):
            row = []
            for j in range(5):
                if i+j < len(Group4):
                    row.append(Group4[i+j])
                else:
                    row.append("-")
            x.add_row(row)
        print(x)
        print()
    if Group5:
        print("\033[0;32m" + "In Group 5, your winning bets are: " + "\033[00m")
        x = PrettyTable()
        for i in range(0, len(Group5), 5):
            row = []
            for j in range(5):
                if i+j < len(Group5):
                    row.append(Group5[i+j])
                else:
                    row.append("-")
            x.add_row(row)
        print(x)
        print()
    if Group6:
        print("\033[0;32m" + "In Group 6, your winning bets are: " + "\033[00m")
        x = PrettyTable()
        for i in range(0, len(Group6), 5):
            row = []
            for j in range(5):
                if i+j < len(Group6):
                    row.append(Group6[i+j])
                else:
                    row.append("-")
            x.add_row(row)
        print(x)
        print()
toto_check()

