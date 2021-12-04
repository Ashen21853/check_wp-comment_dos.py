#########################################################################################
#                                                                                       #
#    NAME : check_wp-comment_dos.py                     DATE : 02/12/2021 (EU)          #
#                                                                                       #
#    AUTHOR : Korenn Alvarez                                                            #
#             k.alvarez@mailoo.org                                                      #
#                                                                                       #
#    DESCRIPTION : This script is created to be used with the NAGIOS supervison tool.   #
#                  He will try to connect by network to a database with an SQL          #
#                  connector, and return an ERROR in case of fail.                      #
#                  When he succed to connect to the database, he will try to make tw    #
#                  request on the commentary table (one for the warning check and one   #
#                  for the critical check) and select the last N commentaries.          #
#                  If the last N commentary is older than the timelapse given in        #
#                  arguments, this mean than they are not spam on this Wordpress.       #
#                  if is newer than the timelapse, it mean they are a great ammount of  #
#                  commentaries in the time given in arguments.                         #
#                                                                                       #
#########################################################################################
