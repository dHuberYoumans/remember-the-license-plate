# Remember the license Plate!

## The Game
This is a small python script for a command-line application that trains one's memory to remember randomly generated license plates.
The combination of letters on the license plates are arbitrary, however follow they must follow the official rules for license plates in Germany:

* the first unit can be beween one and three letters
* the second unit is either one or two letters
* the third unit is a number with two to four digits
* the license plate cannot have more than eight characters or less than six

A generic license plate will thus be of the form ABC-D-1234.

Once the scirpt is started in the command-line the user is asked to first indicate how much time (in seconds) they want to have for remembering the license plate.
Once the user has chosen the time t, the license plate is displayed togehter with a countdown running from t to zero. 
If t=0 is reached, the command-line is cleared (the script runs at the moment on OSX and Windows) and the user is asked to input what they remember. 
A score is recoreded: +1 if the guess was correct, 0 otherwise.
After 10 correct guesses in a row, the user is shown two license plates simultanously, whereby the scoreing convention is the same: +1 for each correct guess, 0 for a wrong guess.
If the user fails to guess the license plate(s) correctly, they are asked whether or not they want to continue.
They can respond with 'j' (yes: continues the game), 'n' (no: quits the game), 's' (score: show the current score in the format _correct / total_) or 'h' (highscore: show the maximum conseccutive correct guesses). 

This project was sparked by a conversation with my brother, who shared his experience with a memory test: recalling a license plate after a certain period of time. 
Eager to improve, he approached me with a request to develop a command-line application to help him with his practice. 

## Ideas for the Future
* implement various game modi, such as
  * Sudden-Death: first incorrect guess ends the game
  * Training Mode: chose to train remembering either one or two license plates; continue without restriction
  * Survival Mode: each incorrect guess costs one life. One starts with three life.
* implement a GUI
* give an option to save results to file

## Improving the Code
This game is a funny little project helping me learn to write better code and handle a coding project. 
This means that there is a lot of space for improvement. 
Among others, the most important (at the moment) are
* proper documentation
* proper error handling
* poper division of files

If you have any comments, remarks or ideas, I'd be happy to hear them! 
