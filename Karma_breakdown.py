#!/usr/bin/env python

"""
Program Docstring
"""

import operator
import sys

import reddit
import urllib2

def sort_and_cut(dic, limit):
    return sorted(dic.iteritems(), key=operator.itemgetter(1), 
                  reverse=True)[:limit]

def term_print(karma_by_subreddit):
    """Print the information about where a redditor got his karma in
       a nicely formatted table"""
    width= 25
    align = (">","<")
    titel = ("Subreddit", "Karma")
    print "{titel[0]:{align[0]}{width}} | {titel[1]:{align[1]}{width}}" \
        .format(titel = titel, align = align, width = width)
    print "{0:^{width}}".format("-"*width, width=width*2+1)
    for (subreddit, karma) in karma_by_subreddit:
        print "{subreddit:{align[0]}{width}} | {karma:{align[1]} {width}}" \
            .format(subreddit = subreddit, karma = karma, 
                   width = width, align = align)
    print

def main(user, thing_type="submissions"):
   """Find out in which subreddits a redditor got his karma"""
   karma_by_subreddit = {}
   thing_limit = None
   user = r.get_redditor(user)
   gen = user.get_comments(limit=thing_limit) if thing_type == "comments" else \
         user.get_submitted(limit=thing_limit)
   for thing in gen:
       subreddit = thing.subreddit.display_name
       karma_by_subreddit[subreddit] = (karma_by_subreddit.get(subreddit, 0)                                                                           + thing.ups - thing.downs)
   return karma_by_subreddit

if __name__ == "__main__":
    user_agent = "Python API tutorial 1.0 by /u/_Daimon_"
    limit = 10
    r = reddit.Reddit(user_agent=user_agent)
    if len(sys.argv) == 1:
        comment_karma = main("_Daimon_", thing_type="comments")
        comment_karma = sort_and_cut(comment_karma, limit)
        print "Comment karma for _Daimon_"
        term_print(comment_karma)
    for user in sys.argv[1:]:
        try:
            for thing_type in ("comments", "submissions"):
                karma = main(user, thing_type=thing_type)
                karma = sort_and_cut(karma, limit)
                print "{0} karma for {1}".format(thing_type, user)
                term_print(karma)
        except urllib2.HTTPError:
            print "The user {0} does not exist!!".format(user)
        except Exception, e:
            print e
            sys.exit(-1)
