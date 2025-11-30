1. User provides:
PDF file path
Either a wordlist OR brute-force generation settings

2. The program loads passwords
If wordlist → reads line by line
If brute-force → generates combinations using itertools

3. Multi-threading starts
Each thread tests a password using pikepdf
Failures are caught using exception handling

4. tqdm progress bar visually tracks all attempts

5. If a password is correct:
PDF opens successfully
Password is returned

6. If not found:
Program ends with a failure message
