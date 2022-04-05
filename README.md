# Heni tech test
All questions have been completed as follows:
- Question 1 answers are in the Jupyter notebook: question_1.ipynb
- Question 2 answers are in the Jupyter notebook: question_2.ipynb
- Question 3 answers are stored as a Scrapy project inside the Question_3 directory. The spider is named bearspace.py
- Question 4 answers are in the Jupyter notebook: question_2.ipynb

The code in each file is well documented and should provide insight into the approach taken.

## Installation
I used python 3.8

    $ pip install requirements.txt

## Question 3
To run the scraper:

    $ cd question_3    
    $ scrapy crawl bearspace

The scraper will save the scraped data as a csv and pickled DataFrame in the question_s/question_3 directory.
