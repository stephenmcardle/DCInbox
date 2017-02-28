# DCInbox
A repository for code used with the DCInbox project.
These scripts are very specific to the DCInbox project, though they might help to show some uses of Python.
For more information on the DCInbox project, please visit www.dcinbox.com

## Email Parser
Converts a directory of .eml files into a single .json file.
More information on the email_parser.py script can be found at: https://github.com/NickMonzillo/EmailParser, where the original script can be found.

## Term References
Using a .json file of emails, this script creates a .csv file of references for a keyword based on user input.
It grabs the entire paragraph in which the word is found for each occurence.

## Congress Mentions
Using a .json file of emails, this script creates a .csv file which contains information about every time one congressman mentions another.
