
In order to run the scraper please provide a file 'login.xlsx' in the root directory (not src!). Structure must be as follows:

      Col 1    Col 2    Col 3
Row 1 Username Password Auth
Row 2 FILL     FILL     FILL

You MUST reset your security questions so that all their answers are the same. Sorry about that, couldn't extract the
security questions from the page as they're just images.

Dependencies:
Pandas
Selenium
chromedriver for selenium