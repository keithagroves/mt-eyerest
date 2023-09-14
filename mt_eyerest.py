import sys

from PyQt6.QtCore import Qt, QTimer, QUrl
from PyQt6.QtMultimedia import QAudioOutput, QMediaPlayer
from PyQt6.QtWidgets import QApplication, QLabel, QPushButton, QWidget
import rumps


def position_changed(position):
    """Callback function for tracking audio position."""
    print(f"Position changed: {position}")


class MtEyerestStatusBarApp(rumps.App):
    """Main class for the mt. eyerest application."""
    
    def __init__(self):
        """Initialize the application."""
        super().__init__("mt. eyerest", quit_button=None)
        self.menu = ["Preferences", "Quit"]
        self.timer = rumps.Timer(self.remind_to_close_eyes, 20 * 60)
        self.timer.start()
        self.first_time = True
        self.app = QApplication.instance() or QApplication(sys.argv)
        self.player = QMediaPlayer()
        self.audio = QAudioOutput()
        self.audio.setVolume(50)
        self.audio.setMuted(False)
        self.player.setAudioOutput(self.audio)
        self.player.positionChanged.connect(position_changed)

    def play_mp3(self, filename):
        """Play an MP3 file."""
        self.player.stop()
        self.player.setPosition(0)
        self.player.play()
        self.player.setSource(QUrl.fromLocalFile(filename))
        self.player.play()

    def play_ding(self):
        """Play a bell sound."""
        self.play_mp3("bell.mp3")

    def remind_to_close_eyes(self, _):
        """Remind the user to close their eyes."""
        if self.first_time:
            self.first_time = False
            return
        self.create_overlay()

    def skip_and_close_overlay(self):
        """Close the overlay when the skip button is pressed."""
        self.skip_pressed = True

    def create_overlay(self):
        """Create and show an overlay window."""
        overlay = QWidget()
        self.skip_pressed = False
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
        close_button.clicked.connect(self.skip_and_close_overlay)
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
        """Show an alert when Preferences is clicked."""
        rumps.alert("jk! No preferences available!")

    @rumps.clicked("Quit")
    def quit_app(self, _):
        """Quit the application."""
        self.app.quit()
        rumps.quit_application()


if __name__ == "__main__":
    MtEyerestStatusBarApp().run()
