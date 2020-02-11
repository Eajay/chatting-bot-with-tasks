# chatting-bot-with-tasks
This chatting machine can talk with users and complete some basic tasks like Alexa and Google Home. 

There are three major parts: 
  - Get real time weather information by Scrapy and store the data into Mysql
  - Use Spotify api to control desktop Spotify application
  - Chatting with the machine with either aiml or seq2seq model

# Part 1: Weather
Weather information comes from www.weather.com. Based on user ip address, the program can obtain computer location and convert into US zip code. Attach the zip code behind the weather then Scrapy can get whole html file. Using regular expression to extract useful information and connect to local Mysql database.

# Part 2: Spotify
Install package spotify first, a package offers all kinds spotify api. The program packs some of the api, including:

  - Searching playlist
  - Stop and continue the song
  - Next and previous song
  - Shuffle and repeat mode
  - Volumn up and down

Before running the program, make sure get your spotify account information. Including:username, client_id, client_secret, redirect_uri.

# Part 3: Chatting with the machine
The code in this program using Aiml as chatting kernel. The essence of Aiml is searching tag. If you are interested in text generation, my seq2seq model with glove embedding is available at: https://github.com/Eajay/seq2seq-chatting-bot-with-keras. However, since the size of training data set is too small, the result is not satisfied.

The program uses key word searching to let machine know whether the input is normal chatting sentence or a request to complete first two parts tasks. The better solution is to combine this into aiml or using machine learning technique to find corresponding response.

### Installation

There are several packages, run the requirements.txt to install them:

```sh
$ pip3 install -r requirements.txt
```

### Running

Run main.py file directly.

### video
<a href="http://www.youtube.com/watch?feature=player_embedded&v=CI7m7vXpev4" target="_blank"><img src="http://img.youtube.com/vi/CI7m7vXpev4/0.jpg" alt="IMAGE ALT TEXT HERE" width="1000" height="600" border="10" /></a>


License
----

MIT
