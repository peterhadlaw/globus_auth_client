#!/usr/bin/expect -f
spawn ssh-add .travis_deploy_key.pem
expect "Enter passphrase for .travis_deploy_key.pem:"
send "\n";
interact
