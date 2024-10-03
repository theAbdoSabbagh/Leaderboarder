from typing import List, Union

class Participant:
    def __init__(
        self,
        rank: str,
        name: str,
        major: str,
        score: str
    ):
        self.rank = rank
        self.name = name
        self.major = major
        self.score = score
        self.score_raw = int(score.replace(',', ''))

    def __repr__(self):
        return f"{self.rank} | {self.name} | {self.major} | {self.score}"
    
    def __str__(self):
        return f"{self.rank} | {self.name} | {self.major} | {self.score}"
    

class Leaderboard:
    def __init__(self):
        self.participants = []

    def __repr__(self):
        return "\n".join([str(participant) for participant in self.participants])

    def __str__(self):
        return "\n".join([str(participant) for participant in self.participants])

    def add_participant(self, participant):
        self.participants.append(participant)

    def get_by_rank(self, rank: str) -> Union[List[Participant], Participant, None]:
        rank_emojis = {
            "1": "🏆",
            "2": "🥈",
            "3": "🥉"
        }

        rank = rank_emojis.get(rank, rank)

        # Use list comprehension to filter participants by rank
        participants = [participant for participant in self.participants if participant.rank == rank]

        return participants if len(participants) > 1 else participants[0] if participants else None

    def as_json(self):
        return {
            "participants": [
                {
                    "rank": participant.rank,
                    "name": participant.name,
                    "major": participant.major,
                    "score": participant.score_raw
                } for participant in self.participants
            ]
        }

    def update_rankings(self):
        # Sort participants by score in descending order
        self.participants.sort(key=lambda p: p.score_raw, reverse=True)

        # Initialize previous score and rank
        previous_score = None
        current_rank = 0

        for index, participant in enumerate(self.participants):
            # Check if the score is the same as the previous participant
            if participant.score_raw == previous_score:
                # If so, use the same rank as before
                participant.rank = str(current_rank)
            else:
                # Otherwise, assign a new rank
                current_rank = index + 1  # Ranks start from 1

                # Update the rank with an emoji for the top three participants
                if current_rank == 1:
                    participant.rank = "🏆"
                elif current_rank == 2:
                    participant.rank = "🥈"
                elif current_rank == 3:
                    participant.rank = "🥉"
                else:
                    participant.rank = str(current_rank)

            # Update previous score for the next iteration
            previous_score = participant.score_raw

        # Ensure correct ranking for ties
        for index, participant in enumerate(self.participants):
            # Check if current score matches the previous participant's score
            if index > 0 and participant.score_raw == self.participants[index - 1].score_raw:
                # If so, copy the rank from the previous participant
                participant.rank = self.participants[index - 1].rank
