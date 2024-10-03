from bs4 import BeautifulSoup
from internal.objects import Leaderboard, Participant

class Parser:
    def __init__(self):
        self.soup = None

    def set_soup(self, html: str):
        self.soup = BeautifulSoup(html, "html.parser")

    def parse(self):
        unfiltered_leaderboard = Leaderboard()
        rows = self.soup.find_all('tr')

        for row in rows:
            columns = row.find_all('td')
            if len(columns) == 4:  # Ensuring it's a valid row with all fields
                rank = columns[0].get_text(strip = True)
                name = columns[1].get_text(strip = True)
                major = columns[2].get_text(strip = True)
                # score = int(columns[3].get_text(strip=True).replace(',', ''))  # Remove commas and convert to int
                score = columns[3].get_text(strip = True)

                participant = Participant(rank, name, major, score)
                unfiltered_leaderboard.add_participant(participant)

        # Filtering to keep participants from the last trophy (🏆) rank onward
        filtered_leaderboard = self.filter_leaderboard(unfiltered_leaderboard)

        # Return the filtered leaderboard
        return filtered_leaderboard
    
    def filter_leaderboard(self, leaderboard: Leaderboard) -> Leaderboard:
        trophy_rank = r"🏆"
        last_trophy_index = None

        # Iterate backwards to find the last occurrence of the trophy rank
        for i in range(len(leaderboard.participants) - 1, -1, -1):
            if leaderboard.participants[i].rank == trophy_rank:
                last_trophy_index = i
                break

        # If the rank was found, slice the participants list
        if last_trophy_index is not None:
            leaderboard.participants = leaderboard.participants[last_trophy_index:]
        else:
            print("Trophy rank not found.")  # Debugging statement

        return leaderboard
