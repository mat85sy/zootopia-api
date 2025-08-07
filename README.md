# Animal Website Generator

This is my project for fetching animal info and making a website.

## How to get it running

1.  Get the code from here (clone the repo).
2.  Make sure you have Python.
3.  Install the stuff it needs:
    `pip install -r requirements.txt`
4.  You need an API key from https://api-ninjas.com/.
5.  Make a file called `.env` and put your key in it like this:
    `API_KEY=your_key_goes_here`

## How to use it

Run the main script:

`python animals_web_generator.py`

It will ask you for an animal name. Type one in (like "Fox") and press Enter.
It makes a file called `animals.html`. Open that in your web browser to see the info.

