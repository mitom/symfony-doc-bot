#!/bin/bash

echo "--> Installing cloudbot"
sudo apt-get install -y git libenchant-dev libenchant1c2a

DIR=/opt/cloudbot/
sudo mkdir -p $DIR

sudo git clone https://github.com/ClouDev/CloudBot $DIR
sudo pip install -r $DIR/requirements.txt

# For some unknown reason the bot comes with a bunch of plugins added by default
# and because of that it takes pretty long to load it + has lots of functionality
# that is undesired.
echo "--> Cleaning up plugins"
plugins=( "admin" "core_misc" "core_misc" "core_sieve" "ignore" "log" "seen" "ignore" )

for file in $(ls $DIR/plugins/*.py)
do
  match=0
  for plugin in "${plugins[@]}"
  do
    if [ "$(basename $file)" == "${plugin}.py" ]
    then
      match=1
    fi
  done
  if [ $match == 0 ]
  then
    sudo rm -f $file
  fi
done

echo "--> Linking symfony plugin"
ln -s /vagrant/cloudbot/symfony.py $DIR/plugins/

echo "--> moving the default config in place"
sudo mv $DIR/config.default $DIR/config

echo "--> Fixing permissions for vagrant user"
sudo chown -R vagrant:vagrant $DIR

echo "----> DONT FORGET TO EDIT ~/cloudbot/config"