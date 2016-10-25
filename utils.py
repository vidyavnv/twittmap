from config import FILTERS

def get_category(tweet):
	final_cat = []
	for category in FILTERS:
		if category in tweet:
			final_cat.append(category)
	return final_cat


