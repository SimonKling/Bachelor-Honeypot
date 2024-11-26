Bachelor's thesis: Attacks on the Cloud: Unveiling Cyber Assaults on Cloud Infrastructure Through Honeypot Analysis

This repsitory contains all code  that was developed and used for the thesis.


To view the data in the ELK stack, install T-Pot via https://github.com/telekom-security/tpotce

Reboot the system

sudo systemctl stop tpot

Afterwards mv docker-compose-data-extraction.yaml ~/tpotce/docker-compose.yaml,

And move the data from the instance you want to inspect inside the ~/tpotce directory 

Finally execute sudo systemctl start tpot 

NOTE: Some data might be corrupted.
