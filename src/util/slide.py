from win32com.client import Dispatch
import logging


class Slide:
    SHAPE_EXIST = -1
    SHAPE_NOT_EXIST = 0

    ppSlideShowBlackScreen = 3  # Black screen
    ppSlideShowDone = 5  # Done
    ppSlideShowPaused = 2  # Paused
    ppSlideShowRunning = 1  # Running
    ppSlideShowWhiteScreen = 4  # White screen

    def __init__(self):
        self.__app = Dispatch('Powerpoint.Application')

    def show_on(self):
        if self.__app.SlideShowWindows.Count > 0:
            self.show_off()
        self.__app.ActivePresentation.SlideShowSettings.Run()

    def next(self):
        if self.is_open():
            permission = [self.ppSlideShowRunning]
            if self.__app.SlideShowWindows(1).View.State in permission:
                self.__app.SlideShowWindows(1).View.Next()
        else:
            raise EnvironmentError

    def prev(self):
        if self.is_open():
            permission = [self.ppSlideShowRunning, self.ppSlideShowDone]
            if self.__app.SlideShowWindows(1).View.State in permission:
                self.__app.SlideShowWindows(1).View.Previous()
        else:
            raise EnvironmentError

    def get_note_shapes(self):
        result = ""
        if self.is_open():
            permission = [self.ppSlideShowRunning]
            if not (self.__app.SlideShowWindows(1).View.State in permission):
                return result
            note_page = self.__app.SlideShowWindows(1).View.Slide.NotesPage
            shapes = note_page.Shapes
            for shape in shapes:
                if shape.HasTextFrame == self.SHAPE_EXIST:
                    result = result + " " + shape.TextFrame.TextRange.Text
        return result
    
    def is_open(self):
        return (self.__app.SlideShowWindows.Count > 0)

    def show_off(self):
        if self.is_open():
            self.__app.SlideShowWindows(1).View.Exit()
