from tkinter import *
import datetime
import collections
import aiml
from runSpotify import Spotify
from weather import Weather
kernel = aiml.Kernel()
kernel.learn('C:\\others\\anaconda\\Lib\\site-packages\\aiml\\botdata\\standard\\startup.xml')
kernel.respond("LOAD AIML B")


class ChatWindow:
    def __init__(self, master, my_nick=None, timestamp=None, ai_nick=None):
        master.title("CHATTING ROOM")
        self.master = master
        self._timestamp = timestamp
        self._line_num = 0
        self.font = ("Times", 16)

        top_frame = Frame(self.master)
        top_frame.pack(expand=True, fill=BOTH)

        self._text = Text(top_frame, state=DISABLED, bg='black', fg='green', font=self.font)
        self._vsb = Scrollbar(top_frame, takefocus=0, command=self._text.yview)
        self._vsb.pack(side=RIGHT, fill=Y)
        self._text.pack(side=RIGHT, expand=YES, fill=BOTH)
        self._text["yscrollcommand"] = self._vsb.set

        entry_frame = Frame(self.master)
        entry_frame.pack(fill=X, anchor=N)

        self._entry_label = Label(entry_frame)
        self._entry = Entry(entry_frame, bg='black', fg='green', font=self.font, insertbackground='green')

        self._entry.pack(side=LEFT, expand=YES, fill=X)
        self._entry.bind("<Return>", self._send_message)
        self._entry.focus()

        self.set_nick(my_nick)
        self._ai_nick = ai_nick

        self._switch = 1

        self.spotify_initial()

        self.weather_initial()

        self.send(self._ai_nick, "What can I do for you, {}".format(self._my_nick))

    def spotify_initial(self):
        # put spotify api details
        username = ''  # placeholder value here
        client_id = ''  # placeholder value here
        client_secret = ''  # placeholder value here
        redirect_uri = ''
        scope = 'user-read-playback-state, user-read-currently-playing, user-modify-playback-state'
        self.spotify_client = Spotify.Spotify(username, client_id, client_secret, redirect_uri, scope)
        print("Successfully initialize Spotify")

    def weather_initial(self):
        # put mysql login detail
        host = ''
        user = ''
        passwd = ''
        db = ''
        port = 3306
        self.weather_client = Weather.Weather(host=host, user=user, passwd=passwd, db=db, port=port)

        print("Successfully initialize weather database")



    def set_nick(self, my_nick):
        self._my_nick = my_nick
        if my_nick:
            self._entry_label["text"] = my_nick
            self._entry_label.pack(side=LEFT, padx=(2, 2), before=self._entry)
            self._entry_label.config(bg='black', fg='green', font=self.font)
        else:
            self._entry_label.pack_forget()

    def _send_message(self, event):
        message = self._entry.get()
        self._entry.delete(0, END)
        if message.strip() == "":
            return
        else:
            message = message.strip()
            self.send(self._my_nick, message)
            tmp = message.lower().split(' ')
            if len(tmp) > 1 and tmp[0] == 'play':
                self.send(self._ai_nick, self.spotify_client.search_and_play(tmp))
            elif tmp[0] == 'stop' or tmp[0] == 'pause':
                self.send(self._ai_nick, self.spotify_client.pause())
            elif tmp[0] == 'continue' or tmp[0] == 'resume':
                self.send(self._ai_nick, self.spotify_client.resume())
            elif tmp[0] == 'next':
                self.send(self._ai_nick, self.spotify_client.next_song())
            elif tmp[0] == 'previous':
                self.send(self._ai_nick, self.spotify_client.previous_song())
            elif len(tmp) > 1 and tmp[0] == 'volume' and tmp[1] == 'up':
                self.send(self._ai_nick, self.spotify_client.volume_up())
            elif len(tmp) > 1 and tmp[0] == 'volume' and tmp[1] == 'down':
                self.send(self._ai_nick, self.spotify_client.volume_down())
            elif tmp[0] == 'repeat':
                self.send(self._ai_nick, self.spotify_client.repeat())
            elif tmp[0] == 'shuffle':
                self.send(self._ai_nick, self.spotify_client.shuffle())
            elif 'weather' in tmp:
                self.send(self._ai_nick, self.weather_client.select_data(tmp))
            else:
                self.send(self._ai_nick, kernel.respond(message))

    def send(self, nick, content):
        nick = nick + ":"
        if self._timestamp is None:
            self._show_message(nick, content)
        else:
            timestamp = "[" + datetime.datetime.now().strftime(self._timestamp) + "]"
            self._show_message(timestamp, nick, content)

    def _show_message(self, *args):
        vsb_position = self._vsb.get()[1]
        self._text.config(state=NORMAL)

        if self._line_num > 0:
            self._text.insert(END, '\n')
        self._line_num += 1

        text = ""
        for arg in args:
            text = text + arg + " "
        self._text.insert(END, text)

        if self._switch == 1:
            # only change 1 line color
            self._change_text(tag_name="other user", lineno=self._line_num, length=len(text), fg_color='red',
                              position='left')

        self._switch *= -1
        self._text.config(state=DISABLED)

        if vsb_position == 1:
            self._text.yview_moveto(1)

    def _change_text(self, tag_name, lineno, length, fg_color, position):
        self._text.tag_add(tag_name, f'{lineno}.{0}', f'{lineno}.{length}')
        self._text.tag_config(tag_name, foreground=fg_color)
        # self._text.tag_config(tag_name, justify=position)