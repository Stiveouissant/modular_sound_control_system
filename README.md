# Modular Sound Control System
Hi everyone! This is my little project that I wrote back at the university in 2020. It's basically a sound recognition system that allows to control a computer with different sounds. There is an executable for Windows available here on GitHub, so if you want, you can just download it and try it out. The program works fully offline.

Program is currently using 3 sound recognition techniques: speech recognition with *SpeechRecognition* library, tap recognition with basic python calculations and pitch recognition using different python math libraries like *scipy* or *numpy*. To execute actions program is using *pyautogui* library, which allows for:
- Moving the mouse and clicking or typing in other applications
- Sending simulated keystrokes to the application
- Taking screenshots
- Moving, resizing, maximizing, minimizing or closing applications
- Displaying a message box for user interaction during script execution

I believe that the project still needs some work, so I'll be updating it when I have the time. First planned change is to use the new Vosk speech recognition instead of the pocketsphinx, which will allow for different languages than english to be used.
