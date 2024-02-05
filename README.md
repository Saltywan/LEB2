# LEB2

This repository contains a Python script that fetches things from LEB2.

## Files

- `getQuizScore.py`: The main script that fetches and displays the quiz score.
- `LICENSE`: The license for this project.

## Requirements

- Python 3

You will be prompted to enter the URL of the quiz and the name of the output file. If it's your first time running the script, you will also need to enter your leb2_session cookies.

## License

This project is licensed under the terms of the GNU General Public License. See the [LICENSE](LICENSE) file for details.


# **Documentation**

## getQuizScore.py

This script fetches the score of a quiz from a given URL.

## How it works

1. The script first prompts the user to enter the URL of the quiz and the name of the output file. If it's the first time running the script, the user will also need to enter their leb2_session cookies.

2. The script sends a GET request to the quiz URL to fetch the student's responses.

3. The script then parses the JSON response and writes the student's score and answers to an HTML file.

## Functions

- `main`: The main function that runs the script.

## Usage

To run the script, use the following command:

```sh
python getQuizScore.py
```