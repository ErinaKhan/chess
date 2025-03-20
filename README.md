# Enigma Chess Engine  [![wakatime](https://wakatime.com/badge/user/86f08dc1-5098-42c2-b193-5a05699baa48/project/7239718c-4401-49ae-bf30-3c767e433e10.svg)](https://wakatime.com/badge/user/86f08dc1-5098-42c2-b193-5a05699baa48/project/7239718c-4401-49ae-bf30-3c767e433e10)
***Developed by Jack Milner***
\
\
[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://buymeacoffee.com/jackmilner)

## Currently supported platforms
- [x] Windows
- [x] Mac
- [ ] Linux
## Background

This chess engine was originally created as a console application in **python** however has now been transferred to use the **pygame** framework. This engines intended use now is to be a pygame application however the **original console application** can still be accessed if the user chooses.

## prerequisites

To be able to run this project you may need to install two libraries onto your pc if you don't have these already. These being the pygame module and the keyboard module.
\
\
To install, navigate to your termal in your chosen IDE and type the following:
###
`pip3 install pygame`
###
then...
###
`pip3 install keyboard`
###
This should now run successfully. If it doesnt restart your IDE and try again. 
## How to access console version?
To access the console application:

1. Go the the `Settings` folder in the project
2. Open `PROJECT_SETTINGS`
###
Change

```Python
IS_CONSOLE_APPLICATION = False
```
To

```Python
IS_CONSOLE_APPLICATION = True
```

###
The console application **doesn't contain** any **tutorial section** or **settings** however it does provide an option not seen within the pygame application which is to load games based on [**FEN strings**](https://en.wikipedia.org/wiki/Forsyth%E2%80%93Edwards_Notation).
###
> [!TIP]
> To make FEN strings to load into the engine I would recommend using [this website](https://www.redhotpawn.com/chess/chess-fen-viewer.php) for creating custom boards and use [this](http://bernd.bplaced.net/fengenerator/fengenerator.html) for generating random boards. (these websites are not created by me)
###
## Pygame example 
![Alt Text](https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExejVtMTd5emtuODR0MDV5azUzZHFvYTJsdWIyN3FvcmozYzN4YjRqNyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/qdGhRLpWaQPRXpnHuV/giphy.gif)
###
The colours used for the board are the same as the colours used by [Lichess.org](https://lichess.org/). However the user can change the colours of the board if they wish in the options menu. Currently the AI is not very advance only searching to a depth of 1 however future ambitions for the project include being able to search to much deeper depths. 
## Tutorial section
The tutorial section of the project currently contains 14 lessons on the basics of chess. These tutorials contains text for the user to read as well as a practice section where the user can move around the pieces and test out what they've learned.
###
Here is an example of the tutorial selection page and an example of a lesson:

![tutorial select](https://imgur.com/jDEHvUQ.png)
###
![example tutorial](https://imgur.com/eAAVFeV.png)

## How to add your own tutorial sections

adding to the tutorial section is currently very simple. 
### 
How to find the file

1. First navigate to the `Tutorial` folder in the project
2. Go into the `Dialogue.txt` file
###

How the file works

* Each line of the text file is a seperate section of tutorial

* Each field of tutorial should be split by the ':' character

* the fields are: `title of the section;Text to show user when clicked;FEN string that is loaded when practicing what you've learned;`

* Example: `Lesson 18 - Test;This is a test;rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1;`
###
Now you can simply add a new line satisfying these conditions to add a new section to the tutorial

## Future ambitions

In terms of the future of this project I plan on the following

1. Adding a better AI to the program that can search to much deeper depths
2. Expanding the tutorial module to allow for much more comprehensive teaching rather then simple text and gameplay
3. Adding a hosted multiplayer feature (players can host lobbies on their devices that others can join)

