#!/bin/bash

openssl aes-256-cbc -K $encrypted_63458b5e578d_key -iv $encrypted_63458b5e578d_iv -in scripts/deploy_key.enc -out deploy_key -d
eval "$(ssh-agent -s)"
chmod 600 deploy_key
ssh-add deploy_key
ssh -oStrictHostKeyChecking=no $TUNNELUNAME@$TUNNEL "ssh $USERNAME@$AGORABACKEND /usr/bin/deploy.sh"
