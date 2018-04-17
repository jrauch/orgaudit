#!/usr/bin/env python

from github import Github, Comparison, Commit, GithubObject
import os
import json
import sys
import time
import copy
import requests
import time
import re
from jinja2 import Environment, PackageLoader, select_autoescape
from collections import OrderedDict
#from ipdb import set_trace

class ScanOrg():
	def __init__(self, user, passwd, acct=None, org=None, base_url="https://api.github.com"):
		self.github = Github(user, passwd, base_url=base_url)
		self.user_handle = None
		self.organization_handle = None
		if acct:
			self.user_handle = self.github.get_user(acct)
		if org:
			self.organization_handle = self.github.get_organization(org)

	def get_members(self):
		if self.organization_handle:
			return self.organization_handle.get_members()
		else:
			return self.user_handle.get_members()

	def get_repos(self):
		if self.organization_handle:
			return self.organization_handle.get_repos()
		else:
			return self.user_handle.get_repos()		

	def users_and_repos(self):
		userlist = OrderedDict()
		repolist = OrderedDict()
		repos = self.get_repos()
		for repo in repos:
			#set_trace()
			users = repo.get_collaborators()
			repolist[repo.full_name] = [ i.login for i in users ]
			for user in users:
				if not user.login in userlist:
					userlist[user.login] = [] 
				userlist[user.login].append(repo.full_name)
		return (userlist, repolist)

class Report():
	def __init__(self):
		self.env=Environment(loader=PackageLoader("orgaudit", "reports"),
							autoescape=select_autoescape(["html", "xml"]))

	def generate_report(self, template, results):
		tc = self.env.get_template(template)
		return tc.render(report_data=results)

if __name__ == "__main__":
	# In ~/.gitcred, place your username:accesstoken
	(user, passwd) = open(os.path.expanduser('~')+"/.gitcred").read().strip().split(":")
	org = ScanOrg(user, passwd, org=sys.argv[1])
	members = org.get_members()
	#set_trace()
	(u,r) = org.users_and_repos()
	results = OrderedDict()
	results["user"] = u
	results["repos"] = r
	reporter = Report()
	print(reporter.generate_report("template.html", results=r))
