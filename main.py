import os

from typing import Optional

from internal.logger import Logger
from internal.requester import Requester
from internal.jsonifier import Jsonifier
from internal.objects import Leaderboard, Participant
from internal.parser import Parser

class Leaderboarder:
    def __init__(self):
        self.logger = Logger()
        self.requester = Requester()
        self.parser = Parser()
        self.jsonifier = Jsonifier("data.json")

        self.leaderboard: Optional[Leaderboard] = None
    
    def run(self):
        # Ask the user if they want to fetch the data
        if os.path.exists("data.json"):
            fetch_data = self.logger.question("Do you want to fetch the data? (y/n)")

            if fetch_data.lower() != "y":
                self.logger.info("Local data found. Loading data from \"data.json\" file.", end_new = True)
                self.jsonifier.load_data(file_name = "data.json")
                self.leaderboard = Leaderboard()

                for participant_data in self.jsonifier.data["participants"]:
                    participant = Participant(
                        participant_data["rank"],
                        participant_data["name"],
                        participant_data["major"],
                        participant_data["score"]
                    )
                    self.leaderboard.add_participant(participant)
                    self.logger.debug(participant)
                
                return self.logger.success("Successfully loaded the data from \"data.json\" file.", start_new = True, end_new = True)

        response = self.requester.get()
        if response.status_code != 200:
            return self.logger.error("Failed to fetch the data.")
        
        self.logger.success("Successfully fetched the data.")
        self.parser.set_soup(response.text)
        self.leaderboard = self.parser.parse()
        self.logger.info("Parsed the data.", end_new = True)

        for participant in self.leaderboard.participants:
            self.logger.debug(participant)
        
        save_data = self.logger.question("Do you want to save the data to a file? (y/n)", start_new = True)
        if save_data.lower() == "y":
            self.jsonifier.data = self.leaderboard.as_json()
            self.jsonifier.save_data()

            self.logger.success("Saved the data to \"data.json\" file.", end_new = True)

    def modify(self):
        rank_emojis = {
            "🏆": "1",
            "🥈": "2",
            "🥉": "3",
        }

        while True:
            rank = self.logger.question("Enter the rank of the participant you want to modify: (E to exit)")
            if rank.lower() == "e":
                break

            participants = self.leaderboard.get_by_rank(rank)

            if not participants:
                self.logger.error("Participant not found.")
                continue

            if isinstance(participants, list):
                self.logger.warning("Multiple participants found. Please choose one.", start_new = True, end_new = True)
                for participant_index, participant in enumerate(participants):
                    self.logger.info(f"{participant_index + 1}. {participant.name} | {participant.major} | {participant.score}")
                print()
                
                index = self.logger.question("Enter the index of the participant you want to modify [E to go back]:")
                if index.lower() == "e":
                    continue

                participant = participants[int(index) - 1]
            else:
                participant = participants
            
            self.logger.info(f"Selected participant: {participant.name}", start_new = True)
            self.logger.info(f"Current score: {participant.score}")
            self.logger.info(f"Current rank: {rank_emojis.get(participant.rank, participant.rank)}")

            while True:
                allowed_multipliers = [
                    "x2", "x4", "x8", "x16", "x32", "/2", "/4", "/8",
                ]
                self.logger.info(f"Allowed multipliers: {' | '.join(allowed_multipliers)}", end_new = True)
                multiplier = self.logger.question("Enter the multiplier [E to cancel]:")

                if multiplier.lower() == "e":
                    break

                if multiplier not in allowed_multipliers:
                    self.logger.error("Invalid multiplier.", start_new = True)
                    continue

                if multiplier.startswith("x"):
                    new_score = int(participant.score_raw) * int(multiplier[1:])
                else:
                    new_score = int(participant.score_raw) // int(multiplier[1:])
                
                participant.score = f"{new_score:,}"
                participant.score_raw = new_score
                self.leaderboard.update_rankings()
                participant.rank = self.leaderboard.participants[self.leaderboard.participants.index(participant)].rank

                self.logger.success(f"Modified the score of {participant.name} to {participant.score}. Rank is now {rank_emojis.get(participant.rank, participant.rank)}", end_new = True)

                self.jsonifier.data = self.leaderboard.as_json()
                self.jsonifier.save_data()

                again = self.logger.question(f"Do you want to modify the score of {participant.name} again? (y/n)")
                if again.lower() != "y":
                    break

                self.logger.info(f"Current score: {participant.score}", start_new = True)
                self.logger.info(f"Current rank: {rank_emojis.get(participant.rank, participant.rank)}")
    
    def export(self):
        export = self.logger.question("Do you want to export the leaderboard to a markdown file? (y/n)", start_new = True)
        if export.lower() != "y":
            return
        
        # Need to export as Github markdown table
        with open("leaderboard.md", "w+", encoding = "utf-8") as file:
            file.write("| Rank | Member | Major | Score |\n")
            file.write("| --- | --- | --- | --- |\n")
            participant: Participant
            for participant in self.leaderboard.participants:
                file.write(f"| {participant.rank} | {participant.name} | {participant.major} | {participant.score_raw:,} |\n")
        
        self.logger.success("Successfully exported the leaderboard to \"leaderboard.md\" file.", start_new = True)

if __name__ == "__main__":
    leaderboarder = Leaderboarder()
    leaderboarder.run()
    leaderboarder.modify()
    leaderboarder.export()

