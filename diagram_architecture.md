flowchart TD

A[User Input] --> B[Argparse Parser]

B --> C{Password Source?}
C -->|Wordlist| D[Load Passwords Generator]
C -->|Brute Force| E[Generate Passwords Generator]

D --> F[Password Stream]
E --> F[Password Stream]

F --> G[ThreadPoolExecutor]
G --> H[try_password() Function]

H -->|Success| I[Return Password]
H -->|Fail| G

I --> J[Display Result]
