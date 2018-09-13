#!/usr/bin/env python

# from auth import consumer_key, consumer_secret, access_token, access_token_secret, api_key 
import auth
import os.path
import os
import csv
import re
import sys
import requests
import logging
import time
# sys.path.insert(0, '/Users/tamirgz/Documents/PythonProjects/Finance/Stocksheet/modules')
from fundamentals import Fundamentals

logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter(
        '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

URL = "https://www.finviz.com/quote.ashx?t={}"
DEFAULT_THS = 50 # percent
to_analyze = []

def update_last_analyzed(filename, idx):
	with open(filename,"w+") as f:
		f.write(str(idx))

def analyze_ticker(ticker, ongoing_print=True):
	response = requests.get(URL.format(ticker))
	if response.status_code == 200:
		try:
			fundas = Fundamentals(0.025, 0.09, ticker, logger)
			# fundas.calc_wacc()
			fundas.yahooScrapper()
			if ongoing_print:
				fundas.print_data()
			# warren.get_cf()	
			# warren.get_dcf()
			# if ongoing_print:
				# warren.print_calcs()
			# if warren.price_diff >= DEFAULT_THS:
				# to_analyze.append(ticker)
				# with open("candidates.dat", "a+") as f:
					# f.write("%s (%f, %f, %f, %f, %s, %f)\n" % 
						# (ticker, warren.price_diff, warren.price, warren.price_per_share, self.wacc, str(warren.cf_list[0]), self.TCF, str(warren.discounted_cf_list[0])))
		except ZeroDivisionError:
			print("Unable to calculate cost of debt for this stock")
	else:
		print("Ticker not found, check spelling and try again")


def main():
	ticker_list = []
	idx = 1

	if len(sys.argv) <= 1:
		print("Not enough parameters")
	else:
		action = sys.argv[1]
		
		if action == "ALL":
			filename = "ALL.dat"
			file1 = open('tickers/nasdaqlisted.txt')
			file2 = open('tickers/otherlisted.txt')
			for line in file1.readlines()[1:] + file2.readlines()[1:]:
			    stock = line.strip().split('|')[0]
			    if (re.match(r'^[A-Z]+$',stock)):
			        ticker_list.append(stock)
			file1.close()
			file2.close()

			if os.path.isfile(filename):
				with open(filename, "r") as f:
					idx = int(f.read())

			while idx < len(ticker_list):
				start = time.time()
				ticker = ticker_list[idx]
				analyze_ticker(ticker, ongoing_print=False)
				middle = time.time()
				update_last_analyzed(filename, idx-1)
				idx = idx + 1
				end = time.time()
				print "========================\t%s\t[%d / %d : %f(%f)] ========================" % (ticker, idx, len(ticker_list), end-start, end-middle)
		elif action == "NASDAQ":
			filename = "NASDAQ.dat"
			file1 = open('tickers/nasdaqlisted.txt')
			for line in file1.readlines()[1:]:
			    stock = line.strip().split('|')[0]
			    if (re.match(r'^[A-Z]+$',stock)):
			        ticker_list.append(stock)
			file1.close()

			if os.path.isfile(filename):
				with open(filename, "r") as f:
					idx = int(f.read())

			while idx < len(ticker_list):
				ticker = ticker_list[idx]
			# for ticker in ticker_list:
				# print "======================== %s [%d / %d] ========================" % (ticker, idx, len(ticker_list))
				analyze_ticker(ticker, ongoing_print=False)
				update_last_analyzed(filename, idx-1)
				idx = idx + 1
		elif action == "OTHER":
			filename = "OTHER.dat"
			file2 = open('tickers/otherlisted.txt')
			for line in file2.readlines()[1:]:
			    stock = line.strip().split('|')[0]
			    if (re.match(r'^[A-Z]+$',stock)):
			        ticker_list.append(stock)
			file2.close()

			if os.path.isfile(filename):
				with open(filename, "r") as f:
					idx = int(f.read())

			while idx < len(ticker_list):
				ticker = ticker_list[idx]
			# for ticker in ticker_list:
				# print "======================== %s [%d / %d] ========================" % (ticker, idx, len(ticker_list))
				analyze_ticker(ticker, ongoing_print=False)
				update_last_analyzed(filename, idx-1)
				idx = idx + 1
		else:
			ticker = sys.argv[1]
			# print "======================== %s ========================" % ticker
			start = time.time()
			analyze_ticker(ticker)
			end = time.time()
			logger.error("Time Elapsed: %f" % (end - start))

	print "Potential stocks:\n"
	print to_analyze
	# ticker = raw_input("Enter the ticker you would like to search for: ")
	# if response.status_code == 200:
	# # if ticker in ticker_list:
	# 	try:
	# 		warren = Warren_Buffet(0.025, 0.09, ticker)
	# 		warren.calc_wacc()
	# 		warren.get_cf()	
	# 		warren.print_data()	
	# 		warren.get_dcf()
	# 		warren.print_calcs()
	# 	except ZeroDivisionError:
	# 		print("Unable to calculate cost of debt for this stock")
	# 	# with open("Stocksheet.csv", "w") as sfile:
	# 	# 	writer = csv.writer(sfile)
	# 	# 	writer.writerow(["Ticker", ticker])
	# 	# 	for key, value in warren.SUMMARY_DATA.items():
	# 	# 		writer.writerow([key, value])
	# 	# sfile.close()
	# else:
	# 	print("Ticker not found, check spelling and try again")

if __name__ == "__main__":
	main()
