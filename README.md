## Question 1.  
### 3 analysis about Enron dataset

#### Analysis 1. Analyze formal CEO Kenneth Lay's email set

* I started with this analysis to get a general idea about Enron dataset, such as folder structure, email hanlding, etc.
* This also shows us Kenneth's contact relationship - which can be a start point of building a relationship network of Enron
* This analysis focus on reading all emails in Kenneth Lay's mailboxes, and substracting all recipients and senders. 
* An email might has >=0 recipient in both send-to and cc field, but there's always only one sender
* Considering the situation of subscribing to a mail-list or being bcced in an email, it is okay if Kenneth's email is not listed in the header
* I will not consider Kenneth himself as his contact

#### Analysis 2. Analyze the similar word sets in 2000 and 2011

* I was trying to loop through all emails in data-set to find some broader topics, however, due to the quantity of the emails and my pc capacity, I decided to narrow down my search range
* Accroding to the [Required Reading](http://www.investopedia.com/updates/enron-scandal-summary/), Enron started to crumble under its own weight since fall 2000, thus we might be able to get some useful information from emails in this period


#### Analysis 3. Analyze the trend of the frequency of words"fraud" and "bankrupt"

* The analyze is self-explanatory, I tried to find the frequency of these two words in all emails
* The very first step is always to narrow down the email list, looping through all emails takes about half an hourfor each word, but process the result set is simplier
* Instead of creating a function to run both a same time, I run them seperately on purpose - to at least get a result for one word

## Question 2.

#### Analysis 1. Using Archived NYT API 

* The original plan was to analyze last 20 years NYT's article number about terriosm. However, avg sive for each file takes about 17MB on disk, and in order to limit the data size, I narrowed the year span to past 3 years
* Loop through all files in 2014-2016, count the number of articles in each month and the ones about terrorism
* Compare the precentage of articles about terrorism in the past 3 years to Sep 2011

#### Analysis 2. Using Books NYT API 

* loop through 16000 files about books from nyt-history-best seller books API
* Export the data into local csv file and sort by data
* Analyze the trend between time and book type

#### Analysis 3. Using Archived NYT API 
