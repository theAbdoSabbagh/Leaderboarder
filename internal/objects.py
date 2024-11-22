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
        self.score_raw = score if isinstance(score, int) else int(score.replace(',', ''))

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

    def add_participant(self, participant: Participant):
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
        data = {
            "participants": [
                {
                    "rank": participant.rank,
                    "name": participant.name,
                    "major": participant.major,
                    "score": participant.score_raw
                } for participant in self.participants
            ]
        }

        return data
        
    def update_rankings(self):
        # Sort self.participants by score in descending order
        self.participants.sort(key=lambda x: x.score_raw, reverse=True)
        
        current_rank = 1
        for i, participant in enumerate(self.participants):
            participant.rank = str(current_rank)

            try:
                if participant.score_raw == self.participants[i+1].score_raw:
                    current_rank = current_rank
                else:
                    current_rank += 1
            except IndexError:
                if participant.score_raw == self.participants[i-1].score_raw:
                    current_rank = current_rank
                else:
                    current_rank += 1
            
        # Add special icons for top ranks
        if len(self.participants) > 0:
            self.participants[0].rank = '🏆'
        if len(self.participants) > 1:
            self.participants[1].rank = '🥈'
        if len(self.participants) > 2:
            self.participants[2].rank = '🥉'
        
        return self.participants
