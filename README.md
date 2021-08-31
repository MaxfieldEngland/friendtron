# friendtron
A conversation bot for Discord, with additional entertainment utility.

Friendtron generates responses to user input, using the gpt-2-simple API created by Max Woolf (https://github.com/minimaxir/gpt-2-simple), trained by our own cleaned Discord data. Features are written first and foremost by request, but generally serve a purpose of text entertainment and utility.

# Features: 
## Autonomous:
* Randomly responds to text messages, at pre-determined constant rates; higher in direct message channels and in the designated chat channel, and lower elsewhere. If mentioned, the bot will respond. 
* Responds via voice, using voice recognition and speech synthesis while present in a voice call. NOTE: due to Discord library limitations, the bot CANNOT listen to the entire call. Instead, they can only listen to a designed local microphone, using Google speech recognition.
* Randomly reacts to text messages; Friendtron may react with a random custom emoji it has access to, or react with an emoji if message text matches one such emoji.

## Commands:
* !friendtronhelp : Lists implemented commands to be viewed in Discord.
* !dni / !DNI :  "Do Not Interact", ignores the entirety of the message body. Friendtron will not respond or add reactions. 
* !pick <option1>, <option2>, or <option3>, <option...> : The bot randomly selects one item in a list of arbitrary length. Options MUST be separated by a comma and space or the sequence ", or ". These can be used interchangeably; i.e. "!pick a, or b, c, or d" will work the same as "!pick a, b, c, d".
* !fmk <option1>, <option2>, or <option3>, <option...> : Friendtron plays F***, Marry, Kill with a list of AT LEAST three names. Same rules as !pick.
* !roll <max> : Friendtron rolls for a random number, like a die. I.e. !roll 20 means the bot will roll a 20 sided die, and report the result.
* !name <OPTIONAL amount> : Friendtron outputs a random name Give a numeric amount to retrieve multiple names at once.
* !nametown <OPTIONAL amount> Friendtron comes up with a random town name, using common town affixes to my known names. Give a numeric amount to retrieve multiple names at once.
* !joinvoice: Friendtron joins the voice channel that the caller is in, and attempt to listen to the system microphone designated in the script. Friendtron will continue listening, and make synthesized voice responses. Until Discord.py incorporates voice channel listening, this is the best the bot can do.

### Rock, Paper, Scissors:
  Friendtron can play Rock, Paper, Scissors via commands. Make your selection, and Friendtron will randomly make their own, and then compare. Friendtron records all scores to a file so that they persist even after being shut down. 

* !rock : play Rock
* !paper : play Paper
* !scissors : play Scissors
* !score : Friendtron lists all recorded scores of players, including their own.
