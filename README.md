# PowerPoint remote program

## Description

Programs that can control PowerPoint over the network and mirror to client the presentation note.

## Requirements

### Environments

- Python version >= 3.0
- Server
  - OS: Windows 10
  - Server must have over PowerPoint 2016
- Client
  - OS: Don't care
  - Client must support over python 3.0

### Packages

- Tkinter: To show the script(or note) to client with GUI.
- logging: To show the error message.
- pywin32(or win32com): To control the MS PowerPoint.
- pynput: To check the input with real time.
- re: To check the valid IP or port number.
- socket: To communicate the server and client.
- json: To send data in a certain format.
- optparse: To give the program options.

## How to use

First, you prepare the program which specify in "Requirements" sections.(pip must be compatible with python 3)

```text
pip install pywin32
pip install pynput
```

>...I'm still working on it