# check_wp-comment_dos.py

# What is this
This script is created to be used with the NAGIOS supervison tool.
He will check if a given ammount of comments was posted on a given timelapse.

# Installation
Get the script from github and make it executable.

    wget https://github.com/tempname790/check_wp-comment_dos.py/raw/main/check_wp-comment_dos.py
    chmod +x check_wp-comment_dos.py

# How to use
You can manually run this script or use it with Nagios or other supervisation tool based on script execution
    
    check_wp-comment_dos.py   [-h]
                            IP WARN CRIT USER PASS DATABASE PREFIX
                            
    -h / --help : Display help
    IP          : The IP address or the FQDN of the server who host the database 
    WARN        : A couple of two value, number of comments and time in seconds, in the form of NB,TIME
    CRIT        : A couple of two value, number of comments and time in seconds, in the form of NB,TIME
    USER        : The username of an account who as the right to make a request
    PASS        : The password for this user
    DATABASE    : The name of the database
    PREFIX      : The prefix defined at the Wordpress installation (usually wptab)


# AUTHOR : Korenn Alvarez 
Contact :   k.alvarez@mailoo.org

# How it's work
He will try to connect by network to a database with an MySQL          
connector. When he succed to connect to the database, he will try to make two    
requests on the comments table (one for the warning check and one
for the critical check) and select the last N comments.
If the last N comment is older than the timelapse given in
arguments, this mean than they are not spam on this Wordpress.
if is newer than the timelapse, it mean they are a great amount of
comments in the time given in arguments.
