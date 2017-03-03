# Models

Initial cloud models experiment

# Dependencies

## Python (2.7)

pip install bokeh
pip install requests

## R

install.packages("topmodel")
install.packages("ismev")
install.packages("plumber")

# To run the microservices:

$ ./modelcloud &
$ Starting server to listen on port 8000

$ ./ismevcloud &
$ Starting server to listen on port 8010

# To run the demo app:

$ bokeh serve demo_app.py --show --args Huagrahuma.json

