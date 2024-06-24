!IMPORTANT
Need to create a .env file with login details, following the format:
role_username=
role_password=
personal_username=
personal_password=

Setup chromium stuff on Ubuntu wsl:

https://saisuman.org/blog/chromium-in-wsl2

If the systemd doesnt work even though the file is correct, update wsl. (Might need --webdownload arg)

If get 127 error when running, go to where chromedriver is installed (its like in .cache and then a bit on)
then run chromedriver using ./chromedriver and might see error like this:

./chromedriver: error while loading shared libraries: libnss3.so: cannot open shared object file: No such file or directory

To solve this error, simply run: sudo apt-get install libnss3.

DOCKER 
Also need to create the .env file within the docker folder, then run:

sudo docker-compose build
sudo docker-compose up