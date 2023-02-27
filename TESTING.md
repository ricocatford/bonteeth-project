# Testing

## Table of Contents
- [Testing](#testing)
  - [Table of Contents](#table-of-contents)
  - [1. Functionality](#1-functionality)
  - [2. Performance](#2-performance)
  - [3. Code validation](#3-code-validation)
    - [HTML validator](#html-validator)
    - [CSS validator](#css-validator)
    - [PyCharm linter](#pycharm-linter)
  - [4. Bug fixes](#4-bug-fixes)


## 1. Functionality
I've performed regular manual tests throughout development for the usability and performance. Below you can find all tests performed to the different elements and features of the App. All tests were carried out in Chrome browser which is my preferred one and is still the most used nowadays.

### Navbar

| **Element / Feature**        | **Test performed** | **Result**                                               | **Pass / Fail** |
|:-----------------------------|:------------------:|:---------------------------------------------------------|:---------------:|
| **Brand logo**               |      Clicked       | Goes to Home page                                        |    **Pass**     |
| **Contact us link**          |      Clicked       | Goes to Contact Us page                                  |    **Pass**     |
| **Log In link**              |      Clicked       | Goes to Log In page                                      |    **Pass**     |
| **Book Appointment link**    |      Clicked       | Goes to Book an Appointment page                         |    **Pass**     |
| **Manage Appointments link** |      Clicked       | Goes to Manage Appointments page                         |    **Pass**     |
| **Messages link**            |      Clicked       | Goes to Messages page                                    |    **Pass**     |
| **Profile link**             |      Clicked       | Goes to Profile page                                     |    **Pass**     |
| **Log Out link**             |      Clicked       | Removes user from session cookie and goes to Log In page |    **Pass**     |

### Side Navbar
When viewport screen is 992px or smaller, Navbar element is replaced by this 'Side Navbar' appearing from the right of the screen when clicking 3-bars icon.

| **Element / Feature**        | **Test performed** | **Result**                                               | **Pass / Fail** |
|:-----------------------------|:------------------:|:---------------------------------------------------------|:---------------:|
| **Brand logo**               |      Clicked       | Goes to Home page                                        |    **Pass**     |
| **Contact us link**          |      Clicked       | Goes to Contact Us page                                  |    **Pass**     |
| **Log In link**              |      Clicked       | Goes to Log In page                                      |    **Pass**     |
| **Book Appointment link**    |      Clicked       | Goes to Book an Appointment page                         |    **Pass**     |
| **Manage Appointments link** |      Clicked       | Goes to Manage Appointments page                         |    **Pass**     |
| **Messages link**            |      Clicked       | Goes to Messages page                                    |    **Pass**     |
| **Profile link**             |      Clicked       | Goes to Profile page                                     |    **Pass**     |
| **Log Out link**             |      Clicked       | Removes user from session cookie and goes to Log In page |    **Pass**     |


### Footer

| **Element / Feature**        | **Test performed** | **Result**                                      | **Pass / Fail** |
|:-----------------------------|:------------------:|:------------------------------------------------|:---------------:|
| **Contact us link**          |      Clicked       | Goes to Contact Us page                         |    **Pass**     |
| **Register link**            |      Clicked       | Goes to Register page                           |    **Pass**     |
| **Book Appointment link**    |      Clicked       | Goes to Book an Appointment page                |    **Pass**     |
| **Manage Appointments link** |      Clicked       | Goes to Manage Appointments page                |    **Pass**     |
| **Twitter link**             |      Clicked       | Opens up Twitter website in a new browser tab   |    **Pass**     |
| **Instagram link**           |      Clicked       | Opens up Instagram website in a new browser tab |    **Pass**     |
| **Facebook link**            |      Clicked       | Opens up Facebook website in a new browser tab  |    **Pass**     |

### Home page

| **Element / Feature**    |         **Test performed**          | **Result**             | **Pass / Fail** |
|:-------------------------|:-----------------------------------:|:-----------------------|:---------------:|
| **Hero section heading** |   Resized screen less than 600px    | Not showing anymore    |    **Pass**     |
| **Register form**        | Filled up with new user credentials | Creates new user in DB |    **Pass**     |

### Home page while in User session

| **Element / Feature**       | **Test performed** | **Result**           | **Pass / Fail** |
|:----------------------------|:------------------:|:---------------------|:---------------:|
| **Hero section subheading** |    Visited page    | Changes text content |    **Pass**     |
| **Register form**           |    Visited page    | Not showing anymore  |    **Pass**     |

### Contact Us page

| **Element / Feature** | **Test performed** | **Result**            | **Pass / Fail** |
|:----------------------|:------------------:|:----------------------|:---------------:|
| **Paragraph**         |    Visited page    | Changes text content  |    **Pass**     |
| **Sign In link**      |      Clicked       | Goes to Log In page   |    **Pass**     |
| **Register link**     |      Clicked       | Goes to Register page |    **Pass**     |

### Contact Us page while in User session

| **Element / Feature** | **Test performed**  | **Result**                                         | **Pass / Fail** |
|:----------------------|:-------------------:|:---------------------------------------------------|:---------------:|
| **Form**              |   Sent empty form   | Does not allow it                                  |    **Pass**     |
| **Form**              | Sent filled up form | Creates new message in DB and goes to Profile page |    **Pass**     |

### Book Appointment page



I also tested responsive design and performance for different browsers including all OS (Windows, Mac and Linux) without any major problems found, in these other browsers:
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
The only thing I really needed to fix and was not a real bug, was displaying the date in a human-friendly way. Since I was using ``date.today()``, built-in Python function to store the "created_on" field for appointments and "sent_on" for messages and the format goes like: 2023-01-01. Then I thought it might be confusing for the user to guess what was day or month, therefore I decided to implement this function in order to solve this issue:
```
def format_date(datetime_string):
    formatted_datetime = datetime.strptime(datetime_string, "%Y-%m-%d")
    return formatted_datetime.strftime("%d %B, %Y")
```
This function is used inside these two other functions ``manage_appointments()`` and ``messages()`` for rendering the time to a format like: 01 January, 2023.