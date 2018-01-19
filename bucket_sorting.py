import bucketsorter as bucketer
import json
import sys #testing


# wrapped int his function just to more easily swap in various files
def purchase_data_into_buckets(purchase_csv,buckets_csv,output_name):
	# [[purchase line one],[purchase line 2],etc...]
	purchase_data = bucketer.getPurchaseRecords(purchase_csv)

	# {1:bucket1,2:bucket2,etc...}
	buckets = bucketer.getBuckets(buckets_csv)

	# {publisher1:{bucket data + index}, publisher2:{bucket data + index}, etc...}
	sorted_buckets = bucketer.sortBuckets(buckets)

	# trim out the internal index, dont need it anymore, used for sort
	buckets = [buckets[b][0:4] for b in buckets] 

	# puts together the json
	for purchase in purchase_data:
		index = bucketer.possibleMatches(purchase,sorted_buckets)
		purchase_string = ",".join(p for p in purchase)
		buckets[index][3]["purchases"].append(purchase_string)

	json_data = []
	for bucket in buckets:
		json_data.append( {"bucket": ','.join(bucket[:3]), "purchases":[bucket[3]['purchases']]} )

	with open(output_name, 'w') as outfile:
		json.dump(json_data, outfile)
	# print json.dumps(json_data)



purchase_data_into_buckets('purchase_data.csv','purchase_buckets.csv','output.txt')
purchase_data_into_buckets('test_purchase.csv','test_buckets.csv','test_output.txt')

