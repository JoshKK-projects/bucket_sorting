RedShelf Coding Challenge
==========================

*Problem*

The RedShelf Business Intelligence Team has submitted a request for an ETL (Extract, Transform, Load) job and you 
are tasked with writing a program that will be used as part of the ETL task. The BI team needs
to take historical textbook purchase data and separate it 
into some pre-defined buckets that will make it easier for them to generate their daily reports. 

*Data Overview*

For this challenge you
have been supplied with two files: 

* `purchase_data.csv`: A comma-separated sampling of historical book purchase data. The fields in this file are as follows:
    * `order_id`: The RedShelf order number (eg. 7639) that is an unsigned 16-bit integer
    * `isbn`: The ISBN13 of the book (eg. 9786141234567) that is always thirteen characters long but may not be a
    valid ISBN13 according to the ISO standard.
    * `publisher`: The publisher of the book (eg. Pearson)
    * `school`: The school code where the purchase occurred (eg. ORD)
    * `price`: An integer representation of the price the customer paid, with a minimum of 1 and maximum of 99
    * `duration`: A string indicating how many days for which the user rented the book (eg. 1_day, 180_day, 362_day)
    * `order_datetime`: A datetime stamp indicating the purchase date (eg. 2015-06-30 12:25:12)

* `purchase_buckets.csv`: A comma-separated list of bucket definitions provided by the BI team.
 The fields in this file are as follows:
    * `publisher`
    * `price`
    * `duration`
    
*Requirements of ETL Job Program*

You must write a program which categorizes each purchase listed in `purchase_data.csv` into the most specific bucket
found in the `purchase_buckets.csv` file. It is important to note that due to Book Metadata information
coming from a variety of sources, the casings of the strings contained in either file are not guaranteed to be
consistent. Therefore, all string comparisons should be done in a case-insensitive fashion. Buckets which are defined in the
purchase_buckets.csv file but don't have any purchases associated with them should still be included in the output file with
empty lists for values.

The rules for comparing the relative specificity of two buckets are as follows:

* Any actual value (eg. Pearson) is more specific than a wildcard character
* A match on multiple criteria is more specific than a match on a single criteria (ie. A match on *,1,1_day is more specific than a match on Pearson,*,*)
* In the case of a specificity tie, `publisher` is most specific, `duration` is second most specific and `price` is least
 specific. So, for instance, if you had a purchase that had the attributes
 
        { "publisher": "Pearson", "price": "76", "duration": "2_day" }
  
 and two valid buckets with equal specificity
 for the purchase like
 
        { "publisher": "Pearson", "price": "76", "duration": "*" } 
 
 and
 
        { "publisher": "*", "price": "76", "duration": "2_day"} 
        
 then the purchase should be put in the first bucket (where "Pearson" is specified) because `publisher`
  is more specific than `price` or `duration`.

Purchase buckets are defined as combinations of attributes a purchase possesses. For instance, here are some example 
purchases that you might find in the `purchase_data.csv` file:

    7639,9781541920172,Pearson,ORD,2,1_day,2015-06-30 12:25:00
    7640,9781541920142,Pearson,ORD,1,3_day,2015-07-31 10:31:00
    7641,9781541920283,SciPub,DFW,3,5_day,2015-10-31 17:35:00
    7642,9781541920293,McGraw-Hill,DEN,2,1_day,2015-05-14 11:35:00
    7643,9781541920172,Pearson,ORD,1,1_day,2015-06-30 12:25:00
    7644,9781541920993,Macmillan,DFW,3,5_day,2015-5-15 14:25:00


And here is some example bucket data ('*' is a wildcard and indicates that any value is valid for that field):

    Pearson,*,* (all Pearson purchases)
    Pearson,2,* (all Pearson purchases with a price equal to 2)
    Pearson,1,3_day (all Pearson purchases with a price equal to 1 where a 3_day rental was purchased)
    McGraw-Hill,*,* (all McGraw-Hill purchases regardless of price or duration)

*Expected Output*

The BI team wants each purchase (identified by `order_id`) sorted into the most specific bucket possible and
only into that bucket. Purchases that do not fit into any bucket should be put into an 'uncategorized (\*,\*,*)' bucket.
The program's output should just be a JSON file that lists each bucket with the purchase data for purchases that
are in it. The data for an individual purchase should be exactly the same in your outputted file.
So for the four buckets and six purchases listed above the output of the program should be:

    [    
        {
            "bucket": "*,*,*",
            "purchases": [
                "7641,9781541920283,SciPub,DFW,3,5_day,2015-10-31 17:35:00",
                "7644,9781541920993,Macmillan,DFW,3,5_day,2015-5-15 14:25:00"
            ]
        },
        {
            "bucket": "McGraw-Hill,*,*",
            "purchases": [
                "7642,9781541920293,McGraw-Hill,DEN,2,1_day,2015-05-14 11:35:00"
            ]
        },
        {
            "bucket": "Pearson,*,*",
            "purchases": [
                "7643,9781541920172,Pearson,ORD,1,1_day,2015-06-30 12:25:00"
            ]
        },
        {
            "bucket": "Pearson,1,3_day",
            "purchases": [
                "7640,9781541920142,Pearson,ORD,1,3_day,2015-07-31 10:31:00"
            ]
        },
        {
            "bucket": "Pearson,2,*",
            "purchases": [
                "7639,9781541920172,Pearson,ORD,2,1_day,2015-06-30 12:25:00"
            ]
        }
    ]

*Additional Requirements*

* Any buckets that are repeated in the `purchase_buckets.csv` should only have purchases
in the first bucket outputted. The second should be empty
* The purchase_data.csv will always be ordered by order_id ascending
* `order_id` will always be unique, no other field is guaranteed to be unique
* The ordering of keys in the outputted JSON file doesn't matter: `bucket` can be first or `purchases`
* The output file should be ordered according the following rules:
    * buckets should be ordered by their original ordering in the `purchase_buckets.csv`
    * purchases in a bucket should be ordered by `order_id`

*How We Review*

The implementation of the solution should be in Python. If you are unsure about any criteria or requirements,
make a reasonable assumption and detail below in the `Assumptions` section. Your reviewers are interested 
in seeing how you would approach this problem in a professional role, so the shortest answer might not be the best.

The reviewers will be looking for the following qualities, in no order of importance:
* Consistent and standard code-style
* Well thought-out architecture and design
* Ease of understanding, maintaining and extending your code e.g. good comments, function names, testing, etc
* Correctness of your solution
* Performance of your solution

Please add all other documentation or notes to this README file at the bottom. If you include 
separate files for explaining your solution, please link to them from the README.


*Submission*

Please submit the following items to your hiring point-of-contact:

* Source files that make up your solution
* The JSON-formatted outputted buckets created by your solution
* The original `purchase_buckets.csv` and `purchase_data.csv` files used as the input of your solution

*Help*

If you have any questions or encounter any issues with
the problem or the data sets, please contact your hiring point-of-contact.

Thank you for your interest and good luck!

*Your Notes Below Here*

**Assumptions**

**Design**

**Other Notes**
