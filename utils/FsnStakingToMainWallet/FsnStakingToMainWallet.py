#!/usr/bin/env python3
#
import os
import time
import smtplib
import sys
import socket
import signal
from email.message import EmailMessage
import urllib.request
import json
from datetime import datetime
from eth_utils import (
    is_address,
    to_checksum_address,
)
#
from  web3fsnpy import Fsn
#
####################################################################################################################
#
# Author: Marcel Cure
# Date: 25th Sept 2019
#
# Purpose:  To continually send Fusion rewards to your main wallet and to send a daily email at midnight 
#           with the the amount sent that day.
#
# Please note: I do not accept responsibility for problems that arise from use of this programme. Use at your own peril! 
#
# You need a gmail account to use this programme.
#
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
if not is_address(pub_key_main):
    raise TypeError(
        'Error: The public address provided for the main wallet is invalid' + pub_key_main
    )
else:
    pub_key_main = to_checksum_address(pub_key_main)
#
#
def is_connected():
    try:
        # connect to the host -- tells us if the host is actually
        # reachable
        socket.create_connection(("www.google.com", 80))
        return True
    except OSError:
        pass
    return False
#
def send_fusion_email(subject, body):
    print(subject,'        ',body)
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(mail_user, mail_password)

#
    msg = EmailMessage()
    msg.set_content(body)
    
    msg['Subject'] = subject
    msg['From'] = mail_user
    msg['To'] = to
#
#
    try:
       server.send_message(msg)
       return(1)
    except:
       return(0)
#
    server.close()
#
######################################################################################################################################
#
#
# Get the private key from your staking wallet by looking under the 'Your details' tab
# in the window that you will run this programme, type:-
#
#    export FSN_PRIVATE_KEY='XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
#
private_key_sender = os.environ["FSN_PRIVATE_KEY"]  # This is the private key of your STAKING WALLET
#
linkToChain = {
    'network'     : 'mainnet',     # One of 'testnet', or 'mainnet'
    'provider'    : 'WebSocket',         # One of 'WebSocket', 'HTTP', or 'IPC'
    'gateway'     : 'default',
    'private_key' : private_key_sender,  
}
#
web3fsn = Fsn(linkToChain)  # This connects to the block chain
#
asset_name = 'FSN'
asset_Id = web3fsn.getAssetId(asset_name)
blockNo = 'latest'
#
pub_key_staking = web3fsn.acct.address
print('pub_key_staking = ',pub_key_staking)
#
if send_email:
    subject = 'Fusion Rewards for ' +  VPS_name             # email subject header
#
#
transaction = {
            "from"  : pub_key_staking,
            "to"    : pub_key_main,
            "nonce" : None,
            "value" : None,
}
#
fsn_rewards = 0
oldtime = datetime.now()
eps = 1e-4            # Use to head off floating point rounding errors and stop sending tiny transactions
#
while(1):
#   
    if is_connected():
#
#       Get the balance of the staking wallet
        bal = web3fsn.getBalance(pub_key_staking, asset_Id, blockNo)
#        
        bal = web3fsn.fromWei(int(bal),'ether')
        bal = float(bal)
        
        tm = datetime.now()
        tmstr = "%2.2u/%2.2u/%4.4u %2.2u:%2.2u:%2.2u"%(tm.day,tm.month,tm.year,tm.hour,tm.minute,tm.second)
        
        print(tmstr,'  Fusion rewards so far today = ',fsn_rewards,' FSN')
        
        if bal > min_bal + eps:
            amount_to_send = bal - min_bal
            print('Sending ',amount_to_send,' FSN to the main wallet ',pub_key_main)
            value = web3fsn.toWei(amount_to_send,'ether')
            transaction['value'] = value
            
            # Send the raw transaction. 
            while(1):
               try:
                   nonce = web3fsn.getTransactionCount(pub_key_staking) 
                   transaction['nonce'] = nonce
                   TxHash = web3fsn.sendRawTransaction(transaction, private_key_sender)
                   print('Waiting for the transaction to go through...')
                   web3fsn.waitForTransactionReceipt(TxHash, timeout=60)
                   break
               except:
                   print('Retrying')
                   time.sleep(300)
            
            print('Done')
            
            tnow = datetime.now()
            
            if tnow.day == oldtime.day:     # must not have gone past midnight yet
                fsn_rewards = fsn_rewards + amount_to_send
            else:                           # went past midnight
                if send_email:
                    # send email
                    body = 'VPS staking machine ' + VPS_name + ' sent ' +  str(fsn_rewards) + ' to the wallet ' + pub_key_main + ' yesterday'
                    if send_fusion_email(subject, body):
                        print('Email sent')
                    else:
                        print('Could not send email')                    
#
                fsn_rewards = amount_to_send
                oldtime = tnow
                
    else:   # Staking VPS cannot connect to the internet, just print message
        print('Could not connect to the internet')
#
    time.sleep(tdelay)      

