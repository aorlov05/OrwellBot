
# Orwell Bot

Orwell is a Discord bot powered by Google's Gemini to detect and remove malicious messages from Discord servers. It uses rudamentary checks against basic types of spam (repeat messages, profanity, harmful links), and uses Gemini to parse a user customized ruleset and automatically punish users based on human-described rules.




## Smalltalk Implementation

A Smalltalk file was used to check if a specified message was harmful is some way. It contains a "MessageDetector" class, which when instantiated with a message, can check if the message is a link. The bot can call Smalltalk by injecting code to create a MessageDetector object for a message and running it.


## Authors

- Andrew Orlov <aorlov@udel.edu> [@aorlov05](https://www.github.com/aorlov05)
- Magnus Culley <magnus@udel.edu> [@magnusculley](https://github.com/magnusculley)
- Ben Wootten <bwootten@udel.edu> [@BenjaminWootten](https://github.com/BenjaminWootten)
