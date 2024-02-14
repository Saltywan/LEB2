# LEB2

This repository contain Python scripts that fetches things from LEB2.

## Files

- `getQuizScore.py`: A script that fetches your quiz score and export it to HTML.
- `getQuizAns.py`: A script that fetches the quiz answer and export it to HTML.
- `getMember.py`: A script that fetches the member list of a class.
<!-- - `LICENSE`: The license for this project. -->

## Requirements

- Python 3

You will be prompted to enter the URL of the site and the name of the output file. If it's your first time running the script, you will also need to enter your leb2_session cookies.

## Usage

To run the script, use the following command:

```sh
python `script_name.py`
```

Get activity score
- `https://app.leb2.org/class/xxxxxx/activity/xxxxxxx/activityFilterList`

Get student submission
- `https://app.leb2.org/class/xxxxxx/activity/xxxxxxx/score/downloadAllFile`

## License

This project is licensed under the terms of the GNU General Public License. See the [LICENSE](LICENSE) file for details.
