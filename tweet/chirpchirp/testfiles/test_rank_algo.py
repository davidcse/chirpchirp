import time
import math

def rank_algorithm(time_posted, likecount,retweetcount):
    elapsed_sec = time.time() - time_posted
    # decay factor
    decayfactor_time = ((9.8/10.0)** (elapsed_sec/60)) # Retains 98% of previous iteration's value every 60 seconds.
    decayfactor_like = ((9.0/10.0)** (elapsed_sec/60)) # Retains 90% of previous iteration's value every 60 seconds.
    decayfactor_retweet = ((8.5/10.0)** (elapsed_sec/60)) # Retains 85% of previous iteration's value every 60 seconds.
    # calculated scores
    likescore = 1000 * likecount * decayfactor_like
    retweetscore= 1000 * retweetcount * decayfactor_retweet
    # add-one smoothing for recency. +1 for the current second, +0.5 after 2 second. + 0.33 after 3 seconds. 
    time_priority_factor = 1.0/elapsed_sec
    timescore =  (1000 * decayfactor_time) + time_priority_factor
    print "likescore", likescore, "retweetscore", retweetscore,"timescore", timescore
    return likescore + retweetscore + timescore

now = time.time()
print "now:", now,"\n"


t = now-60
l = 4
r = 5

print "after 1 minute:"
print t, l, r
print rank_algorithm(t,l,r),"\n"

t = now-120
l = 4
r = 5
print "after 2 minute:"
print t, l, r
print rank_algorithm(t,l,r),"\n"

t = now-180
l = 4
r = 5
print "after 3 minute:"
print t, l, r
print rank_algorithm(t,l,r),"\n"

t = now-240
l = 4
r = 5
print "after 4 minute:"
print t, l, r
print rank_algorithm(t,l,r),"\n"

t = now-300
l = 4
r = 5
print "after 5 minute:"
print t, l, r
print rank_algorithm(t,l,r),"\n"

t = now-360
l = 4
r = 5
print "after 6 minute:"
print t, l, r
print rank_algorithm(t,l,r),"\n"

print "\n\n"
print("doubling time")
print "\n\n"

t = now-720
l = 4
r = 5
print "after 12 min"
print t, l, r
print rank_algorithm(t,l,r),"\n"

t = now-1440
l = 4
r = 5
print "after 24 min"
print t, l, r
print rank_algorithm(t,l,r),"\n"

t = now-2880
l = 4
r = 5
print "after 48 min"
print t, l, r
print rank_algorithm(t,l,r),"\n"

t = now-5760
l = 4
r = 5
print "after 96 min"
print t, l, r
print rank_algorithm(t,l,r),"\n"



print "--------------------------------------------------------"
print "successive posts"
print "--------------------------------------------------------"

t = now-1
l = 4
r = 5

print "after 1 sec:"
print t, l, r
print rank_algorithm(t,l,r),"\n"

t = now-2
l = 4
r = 5
print "after 2 sec:"
print t, l, r
print rank_algorithm(t,l,r),"\n"

t = now-4
l = 4
r = 5
print "after 4 sec:"
print t, l, r
print rank_algorithm(t,l,r),"\n"

t = now-8
l = 4
r = 5
print "after 8 sec:"
print t, l, r
print rank_algorithm(t,l,r),"\n"

t = now-8
l = 4
r = 5
print "after 8 sec:"
print t, l, r
print rank_algorithm(t,l,r),"\n"

t = now-16
l = 4
r = 5
print "after 16 sec:"
print t, l, r
print rank_algorithm(t,l,r),"\n"

print "\n\n"
print("doubling time")
print "\n\n"

t = now-32
l = 4
r = 5
print "after 32 sec"
print t, l, r
print rank_algorithm(t,l,r),"\n"

t = now-64
l = 4
r = 5
print "after 64 sec"
print t, l, r
print rank_algorithm(t,l,r),"\n"
