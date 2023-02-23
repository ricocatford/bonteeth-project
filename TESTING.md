# Testing

## 1. Functionality
I've performed regular manual tests throughout development for the usability and performance of the App. No problems found so far.

I also tested responsive design and performance for different browsers including all OS (Windows, Mac and Linux) without any major problems found, in the following browsers:
- Chrome
- Microsoft Edge
- Firefox
- Safari

## 2. Performance
I used Lighthouse extension for Chrome developer tools for testing the performance of the website:

![Lighthouse report](static/images/testing/lighthouse-report.png)

## 3. Code validation
### HTML validator
Tested all the HTML code with [W3C markup validator](https://validator.w3.org/) and only found errors and warnings due to Jinja templating, required for Flask.


### CSS validator
Tested all my custom CSS code with [W3C jigsaw validator](https://jigsaw.w3.org/css-validator/) and no errors found, only one warning for ``@import`` on line 1:
![CSS validator report](static/images/testing/css-report.png)

### PyCharm linter
Before releasing last version of this website, all warnings and errors found in PyCharm linter for "app.py" in order to be PEP8 compliant were solved. Still, there's a few I could not fix:
![PyCharm linter report](static/images/testing/pycharm-report.png)

## 4. Bug fixes
The only thing I really needed to fix and was not a real bug, was displaying the date in a human-friendly way. Since I was using ``date.today()`` built-in Python function to store the "created_on" field for appointments and "sent_on" for messages and the syntax goes like: 2023-01-01.Then I thought it might be confusing for the user to guess what was day or month, I then decided to implement this function in order to solve this issue:
```
def format_date(datetime_string):
    formatted_datetime = datetime.strptime(datetime_string, "%Y-%m-%d")
    return formatted_datetime.strftime("%d %B, %Y")
```
This function is used inside these two other functions ``manage_appointments()`` and ``messages()`` for rendering the time to format like: 01 January, 2023.