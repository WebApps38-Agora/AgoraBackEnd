#!/bin/bash

openssl aes-256-cbc -K $encrypted_02ff0cf6ea60_key -iv $encrypted_02ff0cf6ea60_iv -in scripts/deploy_key.enc -out deploy_key
eval "$(ssh-agent -s)"
chmod 600 deploy_key
ssh-add deploy_key
ssh $USERNAME@$AGORABACKEND "/usr/bin/deploy.sh"
