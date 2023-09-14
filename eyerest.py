from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLabel
from PyQt6.QtCore import Qt, QTimer, QUrl
from PyQt6.QtMultimedia import QAudioOutput, QMediaPlayer
import rumps
import sys

def position_changed(position):
    print(f"Position changed: {position}")

class AwesomeStatusBarApp(rumps.App):
    def __init__(self):
        super().__init__("eyerest", quit_button=None)
        self.menu = ["Preferences", "Quit"]
        self.timer = rumps.Timer(self.remind_to_close_eyes, 20*60)
        self.timer.start()
        self.first_time = True
        # Initialize QApplication and QMediaPlayer
        self.app = QApplication.instance() or QApplication(sys.argv)
        self.player = QMediaPlayer()

        self.audio = QAudioOutput()
       
        self.audio.setVolume(50)
        self.audio.setMuted(False)
        self.player.setAudioOutput(self.audio)
        self.player.positionChanged.connect(position_changed)

    def play_mp3(self, filename):
        self.player.stop()  # Stop the player first (if needed)
        self.player.setPosition(0)  # Set the position to 0
        self.player.play()  # Play it again
        self.player.setSource(QUrl.fromLocalFile(filename))
        self.player.play()

    def play_ding(self):
        # rumps.notification("You can now continue working", "Reminder", "Great job resting your eyes!")
        self.play_mp3("bell.mp3")

    def remind_to_close_eyes(self, _):
        if self.first_time:
            self.first_time = False
            return
        # rumps.notification("Take a Break", "Reminder", "Close your eyes for a few seconds.")
        self.create_overlay()

    def skip_and_close_overlay(self):
        self.skip_pressed = True  # Set the flag when the skip button is pressed

    def create_overlay(self):
        overlay = QWidget()
        self.skip_pressed = False  # Add a flag to track if the skip button was pressed

        screen = self.app.primaryScreen()
        screen_geometry = screen.geometry()
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()

        overlay.setWindowOpacity(0.6)
        overlay.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.FramelessWindowHint)
        overlay.setGeometry(0, 0, screen_width, screen_height)
        overlay.setStyleSheet("background-color:black;")

        text_label = QLabel("Rest your eyes, the bell will call you back.", overlay)
        text_label.setStyleSheet("font-size: 24px; color: white;")
        text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        text_label.adjustSize()
        label_width = text_label.width()
        label_height = text_label.height()
        label_x = (screen_width - label_width) // 2
        label_y = (screen_height - label_height) // 2
        text_label.move(label_x, label_y - 50)

        close_button = QPushButton("SKIP", overlay)
        close_button.clicked.connect(self.skip_and_close_overlay)  # Modify this line
        close_button.clicked.connect(overlay.close)
        close_button.resize(200, 100)
        close_button.setStyleSheet("font-size: 24px; background-color: black; color: white;")
        center_x = (screen_width - 200) // 2
        center_y = (screen_height - 100) // 2
        close_button.move(center_x, center_y + 100)

        QTimer.singleShot(10000, lambda: [overlay.close(), self.play_ding() if not self.skip_pressed else None])
        overlay.show()
        self.app.exec()

    @rumps.clicked("Preferences")
    def prefs(self, _):
        rumps.alert("jk! No preferences available!")

    @rumps.clicked("Quit")
    def quit_app(self, _):
        self.app.quit()
        rumps.quit_application()

if __name__ == "__main__":
    AwesomeStatusBarApp().run()
