gTest  
=====

_Find out where the network problem is._

Sometimes your internet connection does not work. What has happend? Where is the problem?

This script can answer the second question. Just change `accessPoints` to list of IP adresses and their names. You could find the addresses by launching command

    tracepath -n google.com

The checking ping each address. If it pongs back, it is active and the script check another point. If not, you can identify where the problem is.

The script has a nice GUI and can be used by non-geeky people. Built for my family :)
