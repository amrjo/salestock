#!/usr/bin/python3

import argparse
from datetime import datetime

def initialization():
	user_preference_path = 'user_preference.txt'
	product_score_path = 'product.txt'
	output_file = 'recommendation_rank.txt'
	f = open(user_preference_path, 'r')
	user_preference_data = f.read()
	f.close()
	
	# convert to list of list and convert to float or int
	user_preference_data = [[float(i) if "." in i else int(i) for i in user_preference.split("\t")] for user_preference in user_preference_data.split('\n')]

	f = open(product_score_path, 'r')
	product_score_data 	= f.read()
	f.close()

	# convert list to dictionary and convert keys and values to int
	product_score_data	= dict([int(v) for v in product_score.split('\t')] for product_score in product_score_data.split('\n'))
	for user_preference in user_preference_data:
		
		# find interval between timestamp to now
		days_differ	 = datetime.fromtimestamp(user_preference[3]) - datetime.utcnow()
		# calculate the effective score, round it and append it to user_preference
		user_preference.append(float("{0:.4f}".format(user_preference[2] * 0.95 ** abs(days_differ.days))))
	recommendation = {}

	# calculate the recommendation score for products if product in user preference
	for user, product, interest_score, timestamp, effective_score in user_preference_data:
		if user not in recommendation:
			recommendation[user] = {}
		if product not in  recommendation[user]:
			recommendation[user][product] = 0
		recommendation[user][product] = (product_score_data[product]*effective_score)+product_score_data[product]

	# for products that are not in the user_preference
	for user in recommendation:
		for product in product_score_data:
			if product not in recommendation[user]:
				recommendation[user][product] = product_score_data[product]
				
	# make a list of user and top n from the recommendation score
	recommendation = [[user]+sorted(recommendation[user], key=lambda product:recommendation[user][product], reverse=True)[:5] for user in recommendation]
	# return(top_recommendation[uid-1][1:])
	
	with open(output_file, 'w+') as f:
		f.write('\n'.join('\t'.join(map(str, user_recommendation))for user_recommendation in recommendation))
		f.close()
	return 	"""+=================================================================================================+
| Computation  Process Done, the calculation results are stored in "recommendation_rank.txt" file |
| To check recommended products for specified users, use -u, --uid [uid] instead                  |
+=================================================================================================+"""

def find_recommended_products(uid):
	try:
		f = open('recommendation_rank.txt', 'r')
	except FileNotFoundError:
		print('Recommendation Score File Not Detected, doing precomputating calculation...\n')
		initialization()
		print('+=================================================================================================+')
		print('| Computation  Process Done, the calculation results are stored in "recommendation_rank.txt" file |')
		print('+=================================================================================================+\n')
		f = open('recommendation_rank.txt', 'r')
	recommendation_score_data = [recommendation.split('\t') for recommendation in f.read().split('\n')]
	f.close()

	recommendation = [x[1:] for x in recommendation_score_data if x[0] == str(uid)][0]
	print('Top 5 product for user {}: '.format(uid))  
	return recommendation

parser = argparse.ArgumentParser(description="Calculating and show the recommendation score products for specified user. Specify no arguments for doing precomputing calculation")
parser.add_argument('-u', '--uid', type=int, metavar='', help="ID of the user, to find recommended products for specified user")
args = parser.parse_args()

if(args.uid != None):
	print(*find_recommended_products(args.uid), sep='\n')
else:
	print(initialization())