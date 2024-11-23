# Leaderboarder
A tool I made for automatically updating the tech titans leaderboard of the AURAK coding club.

## Setup
1. Clone the repository using `git clone https://github.com/theAbdoSabbagh/Leaderboarder.git`
2. Install the required packages using `pip install -r requirements.txt`
3. Run the script using `python main.py`

## How it works
1. The script will automatically fetch the latest leaderboard from the AURAK Coding club Github.
   - Alternatively, it will load the local data if it exists and the user chooses to do so.
2. The leaderboard data will be displayed on the terminal
3. The user will be prompted to enter the rank of the participant they want to update the score for.
    - If there is multiple participants with the same rank, the user will be prompted to enter the index of the participant they want to update, from a menu that will be displayed.
4. The user will be prompted to enter the multiplier to be applied to the score of the participant.
5. Until they enter E to exit the modification mode, the user can continue updating scores.
6. Once the user exits the modification mode, the user will be asked if they want to save the updated leaderboard to a local file.
    - If the user chooses to save the file, the updated leaderboard will be saved to a file called `leaderboard.md` in the same directory as the script.

## Why
I made this tool to automate the process of updating the leaderboard of the AURAK coding club. The leaderboard is hosted on the club's Github repository, and it must be updated manually. This tool fetches the latest leaderboard, displays it to the user, and allows them to automatically update the scores of the participants. This way, the leaderboard can be updated quickly and efficiently.

## License
This project is licensed under the MIT License - see the [LICENSE](https://github.com/theAbdoSabbagh/Leaderboarder/blob/main/LICENSE) file for details.

## Acknowledgements
- [AURAK Coding Club](https://github.com/AURAK-Coding-Club)
