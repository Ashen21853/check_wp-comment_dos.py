#!/usr/bin/python3.7


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




#########################################################################################
###########################     IMPORT DECLARATIONS     #################################
#########################################################################################

import mysql.connector
import datetime
import argparse
import sys



##########################################################################################
############################     VARIABLES DECLARATIONS    ###############################
##########################################################################################

# RETURN VALUE
STATE_OK        =   0
STATE_WARNING   =   1
STATE_CRITICAL  =   2
STATE_UNKNOW    =   3

# DESCRIPTION USED TO GENERATE HELP
DESC            =   "This Script is used with the database used by Wordpress. It will check if a given number of commentary in a given lapse of time has been posted."




###########################################################################################
######################      FUNCTIONS DECLARATIONS     ####################################
###########################################################################################

# DESCRIPTION :     Build and return a String request to select the <n> last commentaries on the tables <prefix>_comments
# ARGUMENTS :
#       prefix      :   Prefix used in the database by Wordpress (definded at the Wordpress installation)
#       n           :   the number of commentaries to check
#
def build_request ( prefix, n ) :
    return "SELECT " +prefix+ "_comments.comment_date FROM " +prefix+ "_comments ORDER BY " +prefix+ "_comments.comment_date DESC LIMIT " +n+ ";"




# DESCRIPTION   :   Print an error message and exit program
# ARGUMENTS     :
#       msg         :   Error message to display
#       argParser   :   Object needed to display help
#
def fatal ( msg, argParser ) :
    print ( "\n[!] FATAL ERROR :", msg, "\n\n" )
    argParser.print_help ()
    return_state ( STATE_CRITICAL )




# DESCRIPTION :     Check the data base. Execute the request and check if the <nb> older commentarie is older than the time requested.
#                   If the timestamp of the commentarie is inferior to the timestamp given by the argument <time>, return True.
# ARGUMENTS :
#       cursor      :   Cursor open previously by an SQL connector
#       prefix      :   prefix used in the database by Wordpress
#       nb          :   The number of commentaries to check
#       time        :   The time in seconds to check the older commentaries
#
def check_db ( cursor, prefix, nb, time ) :
    cursor.execute ( build_request ( prefix, nb ) )
    result = cursor.fetchall ()
    
    d = result[-1]
    d = datetime.datetime.today() - d[0]
    b = datetime.timedelta ( seconds = time )
    if d < b :
        return True
    return False




# DESCRIPTION :     Return a value and print the status
# ARGUMENTS :
#       state       :   The state to return
#       msg         :   A message to print after the status
#
def return_state ( state, msg = "" ) :
    if state == STATE_OK :
        print ( "OK", msg )
        sys.exit(STATE_OK)
    elif state == STATE_WARNING :
        print ( "WARNING", msg )
        sys.exit ( STATE_WARNING )
    elif state == STATE_CRITICAL :
        print ( "CRITICAL", msg )
        sys.exit ( STATE_CRITICAL )
    else :
        print ( "UNKNOW", msg )
        sys.exit ( STATE_UNKNOW )
    




################################################################################################
###################################        MAIN       ##########################################
################################################################################################

################      Argument Gestion
parser = argparse.ArgumentParser(description=DESC)
# Register all arguments
parser.add_argument ( 'IP', help='IP address or FQDN of the database')
parser.add_argument ( "WARN", help='<nb>,<time> : NB = number of commentary, TIME = timelapse in seconds' )
parser.add_argument ( 'CRIT', help='<nb>,<time> : NB = number of commentary, TIME = timelapse in seconds' )
parser.add_argument ( 'USER', help="username used to connect to the database" )
parser.add_argument ( 'PASS', help="password used to connect to the database" )
parser.add_argument ( 'DATABASE', help="the name of the database" )
parser.add_argument ( 'PREFIX', help="the prefix used by the database" )

args = parser.parse_args ()

# Separate couple nb,time in two variables. Exit with error if cannot split
try :
    warn =      args.WARN.split ( "," )
    warn_n =    warn[0]
    warn_t =    int ( warn[1] )

    crit =      args.CRIT.split ( "," )
    crit_n =    crit[0]
    crit_t =    int ( crit[1] )

except IndexError :
    fatal("Bad arguments", parser)
except :
    fatal("", parser)

###################    End Arguments Gestion



###################    SQL Connection 
try :

    # Connect to the database and set cursor
    db =    mysql.connector.connect (   host = args.IP,                     \
                                        user = args.USER,                   \
                                        password = args.PASS,               \
                                        database = args.DATABASE )
    cursor = db.cursor ()

    # Check Warning state
    if check_db ( cursor, args.PREFIX, crit_n, crit_t ) :
        return_state ( STATE_WARNING )

    # Check Critical state
    if check_db ( cursor, args.PREFIX, warn_n, warn_t ) :
        return_state ( STATE_WARNING )

except Exception as x:
    fatal ( x, parser )
##################    End SQL Connection


# if all check is return 0, and they are no exception, return STATE_OK
return_state ( STATE_OK )
