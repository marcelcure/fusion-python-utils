# FsnStakingToMainWallet

A simple python utility to continuously send staking rewards from your Fusion mining machine back to your secure main Fusion wallet.

# Quick Start

Install some dependencies (you will need > python3.6) :-

#> sudo apt install python3 python3-pip   (if you don't already have these)

#> sudo pip3 install web3fsnpy  (or pip3 install web3fsnpy --user if you want to install a username only copy)

#> git clone https://github.com/marcelcure/fusion-python-utils.git


You need to change the data fields in the file FsnStakingToMainWallet.py using your favourite editor (e.g. nano) :-

####################################################################################################################
#
#  START OF USER CONFIGURABLE SECTION
#
tdelay = 30     # Time in seconds between checking for rewards
#
# Minimum balance to leave in the staking wallet
min_bal = 0.15  # The number of FSN to leave in the staking wallet
#
#
pub_key_main = '0x0000000000000000000000000000000000000000'    # Your Fusion public key for your main wallet 
#
# Do you want to get an email each midnight showing the rewards for that day?
send_email = True    # set to False to stop emails
#
if send_email:
# Name of this staking VPS machine (to be used in the email - any string will do)
    VPS_name = 'XXXXXXXXXX'
#
    mail_user = 'mymail@gmail.com'       # Put your gmail address here
#
#  You must create a Google app password. Go to https://myaccount.google.com/ then select 'Security',
#  then 'App Passwords' Generate a password and use it below.
#
    mail_password = 'xxxxxxxxxxxxxxxx'        # Create a simple app password from your Google account. Put it here
#
    sent_from = ' '  
    to = ['mymail@gmail.com',]           # email address that you want to send alert to
#
#
#  THE END OF USER CONFIGURABLE SECTION
#
######################################################################################################################
#

You can run the code on your VPS now. A good way to do this is to use the 'screen' utility, or you can run it in the background using &

