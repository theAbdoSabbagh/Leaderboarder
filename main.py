from typing import Optional

from internal.logger import Logger
from internal.requester import Requester
from internal.jsonifier import Jsonifier
from internal.objects import Leaderboard
from internal.parser import Parser

class Leaderboarder:
    def __init__(self):
        self.logger = Logger()
        self.requester = Requester()
        self.parser = Parser()
        self.jsonifier = Jsonifier("data.json")

        self.leaderboard: Optional[Leaderboard] = None
    
    def run(self):
        response = self.requester.get()
        if response.status_code != 200:
            return self.logger.error("Failed to fetch the data.")
        
        self.logger.success("Successfully fetched the data.")
        self.parser.set_soup(response.text)
        leaderboard = self.parser.parse()
        self.logger.info("Parsed the data.")

        for participant in leaderboard.participants:
            self.logger.debug(participant)
        
        self.jsonifier.data = leaderboard.as_json()
        self.jsonifier.save_data()

        self.logger.success("Saved the data to data.json.")

        self.leaderboard = leaderboard

    def modify(self):
        while True:
            rank = self.logger.question("Enter the rank of the participant you want to modify: (0 to exit)")
            if rank == "0":
                break

            participant = self.leaderboard.get_by_rank(rank)

            if not participant:
                self.logger.error("Participant not found.")
                continue

            if isinstance(participant, list):
                self.logger.error("Multiple participants found. Please choose one.")
                for index, participant in enumerate(participant):
                    self.logger.info(f"{index + 1}. {participant}")
                
                index = self.logger.question("Enter the index of the participant you want to modify:")
                participant = participant[index - 1]
            
            self.logger.info(f"Selected participant: {participant.name}")

            while True:
                allowed_multipliers = [
                    "x2", "x4", "x8", "x16", "x32", "/2", "/4", "/8",
                ]
                self.logger.info(f"Allowed multipliers: {' | '.join(allowed_multipliers)}")
                multiplier = self.logger.question("Enter the multiplier [0 to cancel]:")

                if multiplier == "0":
                    break

                if multiplier not in allowed_multipliers:
                    self.logger.error("Invalid multiplier.")
                    continue

                if multiplier.startswith("x"):
                    new_score = int(participant.score_raw) * int(multiplier[1:])
                else:
                    new_score = int(participant.score_raw) // int(multiplier[1:])

                participant.score = f"{new_score:,}"
                participant.score_raw = new_score
                
                self.logger.success(f"Modified the score of {participant.name} to {participant.score}")

                # Update the leaderboard rankings
                self.leaderboard.update_rankings()

                # Save the data to data.json
                self.jsonifier.data = self.leaderboard.as_json()
                self.jsonifier.save_data()

                again = self.logger.question(f"Do you want to modify the score of {participant.name} again? (y/n)")
                if again.lower() != "y":
                    break

if __name__ == "__main__":
    leaderboarder = Leaderboarder()
    leaderboarder.run()
    leaderboarder.modify()

