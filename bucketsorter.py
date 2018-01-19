import csv
import operator 
#converts a csv of bucket data into dictionary with key=index, value=bucket
def getBuckets(bucket_csv):
    buckets = {}
    with open(bucket_csv, 'rb') as buckets_file:
        bucket_file_reader = csv.reader(buckets_file)
        for index,row in enumerate(bucket_file_reader):
            row = row + [{"purchases":[]}]
            buckets[index] = row
        return buckets

#takes in dictionary of buckets and sorts them into a dictionary(assoc array my php says...)by publisher, including *. 
#this should allow me to only check buckets that a record could possibly fit in and ignore ones with 0X matches.
#thought about doing the same for all three col's in bucket data but including * in publisher achieves the same
#discrimantory power with less code complexity
def sortBuckets(buckets):
    bucket_by_publisher = {}
    # sort the buckets by publisher, price and duration for easier lookup later
    for row in buckets:
        if buckets[row][0].lower() not in bucket_by_publisher:
            buckets[row].append(row)
            bucket_with_index = buckets[row]
            bucket_by_publisher[buckets[row][0].lower()] = [bucket_with_index]#add the index for the bucket so we can asign purchases by index later
        else:
            buckets[row].append(row)
            bucket_with_index = buckets[row]
            bucket_by_publisher[buckets[row][0].lower()].append(bucket_with_index)
    return bucket_by_publisher

#converts a csv of purchase data into a list for easier parsing
def getPurchaseRecords(purchase_records):
    purchase_data = []
    with open(purchase_records, 'rb') as purchase_file:
        purchase_file_reader = csv.reader(purchase_file)
        for row in purchase_file_reader:
            purchase_data.append(row)
    return purchase_data

# takes dictionary of buckets sorted by sortBuckets and a 
# purchase row, finds all possible buckets it could go in
def possibleMatches(row,sorted_buckets):
    # relevant classification columns
    # and order of tie breakers
    publisher = row[2].lower() # 0 - row order in bucket priority
    duration = row[5] #2
    price = row[4] # 1
    # get all buckets that have at least a 1X match
    buckets_to_check = sorted_buckets["*"]
    if publisher.lower() in sorted_buckets:
        buckets_to_check = sorted_buckets[publisher.lower()] + buckets_to_check
    # buckets_to_check = [publisher,price,duration,index]
    possible_matches = {"1":[],"2":[]}
    for bucket in buckets_to_check:
        #already checking where publisher matches or is * so only need to check on duration and price
        if publisher == bucket[0].lower() and duration == bucket[2] and price == bucket[1]: #full match, just return
            return bucket[4]
        # 2X matches
        if publisher == bucket[0].lower() and duration == bucket[2] and bucket[1] == "*":
            possible_matches["2"].append(bucket)

        if publisher == bucket[0].lower() and  bucket[2] == "*" and price == bucket[1]:
            possible_matches["2"].append(bucket)

        if bucket[0].lower() == "*" and duration == bucket[2] and price == bucket[1]:
            possible_matches["2"].append(bucket)
        # 1X matches
        if bucket[0].lower() == "*" and duration == bucket[2] and bucket[1] == "*":
            possible_matches["1"].append(bucket)

        if bucket[0].lower() == "*" and bucket[2] == "*" and price == bucket[1]:
            possible_matches["1"].append(bucket)

        if publisher == bucket[0].lower() and bucket[2] == "*" and bucket[1] == "*":
            possible_matches["1"].append(bucket)
    # print '___'
    # print row
    # print possible_matches
    # no possible matches found
    if len(possible_matches["1"]+possible_matches["2"])==0:
        return 1 #index of undefined bucket
    # more than one possible bucket
    elif (len(possible_matches["1"]+possible_matches["2"])>1):
        # if only one 2X match, just use that one
        if len(possible_matches["2"]) == 1:
            return possible_matches["1"][0][4] 
        elif len(possible_matches["2"]) > 1:#else tiebreak
            return tieBreaker(possible_matches["2"])
        else:#so must be multipel 1X matches, tiebreak
            return tieBreaker(possible_matches["1"])
    else: #one possible bucket
        if len(possible_matches["1"]) > 0: #a 1X match  
            return possible_matches["1"][0][4] #from 1X bin, first item in it since only one, 4th index for bucket index
        else:
            return possible_matches["2"][0][4] 

# takes all possible buckets a row could go in,
# returns the index of the best bucket match
def tieBreaker(matches):
    # sorts matches by index 0,2,1 in that priority, coresponding to publisher, duration, price
    # if the amount of fields needed to compare was greater, using indexes to find them could be confusing,
    # might be worth turning them from a list to a dictionary with labeled fields
    matches.sort(key=operator.itemgetter(0,2,1),reverse=True)
    return matches[0][4]
