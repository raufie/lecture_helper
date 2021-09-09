from Ui_MainWindow import Ui_MainWindow
import time
import json
from render_automation_data import get_frames_by_ffmpeg
import numpy as np
import subprocess
import os
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


# os.system("pyuic5 Ui_MainWindow.ui -o Ui_MainWindow.py")
class Dialog(QDialog):
    def __init__(self, parent=None):
        super(Dialog, self).__init__(parent)
        self.label = QLabel("START RECORDING FIRST DUMBASS!!!!!")
        layout = QVBoxLayout()
        ok_btn = QDialogButtonBox.Ok
        self.buttonBox = QDialogButtonBox(ok_btn)
        self.buttonBox.accepted.connect(self.accept)
        layout.addWidget(self.label)
        layout.addWidget(self.buttonBox)
        self.setWindowTitle("Error : )")
        self.setLayout(layout)


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        # button connections
        self.recording_btn.clicked.connect(
            self.start_recording
        )
        self.folder_btn.clicked.connect(
            self.get_folder
        )
        self.ffmpeg_btn.clicked.connect(
            self.run_ffmpeg_script
        )
        self.render_video_btn.clicked.connect(
            self.render_video
        )
        self.render_video_btn.pressed.connect(
            self.rendering

        )
        self.low_btn.toggled.connect(
            lambda: self.handle_render_quality(self.low_btn))
        self.high_btn.toggled.connect(
            lambda: self.handle_render_quality(self.high_btn))

        self.medium_btn.toggled.connect(
            lambda: self.handle_render_quality(self.medium_btn))

        # important initializations
        self.render_quality = "m"

    def handle_render_quality(self, s):
        if s.isChecked():
            if s.text() == "Low":
                self.render_quality = "l"
            elif s.text() == "Medium":
                self.render_quality = "m"
            else:
                self.render_quality = "h"
            print(self.render_quality)

    def rendering(self):
        self.script_info_2.setText("Rendering 🔃")
        self.script_info_2.setStyleSheet("color: darkblue")
        try:
            f = open(f"{self.folder}/file_data.dat", "r")
            anim_name = f.read()
            self.anim_name = anim_name
        except Exception as e:
            print("error fetching anim or something.. details below")
            print(e)

    def run_ffmpeg_script(self):
        # solve this when you come back
        # get the animation name from the animation file... make it give you
        # we also need to get the animation name
        try:
            f = open(f"{self.folder}/file_data.dat", "r")
            anim_name = f.read()
            self.anim_name = anim_name
            # f1 = f"{self.folder}/media/videos/lecture/480p15/{anim_name}.mp4"
            subprocess.call(
                f'start /wait python render_automation_data.py "{self.folder}" {anim_name} -y', shell=True)
            self.script_info.setText("Script run ✅")
            self.script_info.setStyleSheet("color: green")
            self.initialize_state()

        except Exception as e:
            print("no shit")
            print(e)

    def render_video(self):

        try:

            os.system(
                f"manim {self.folder}/lecture.py {self.anim_name} -p -q{self.render_quality} ")
            media = "720p30"
            if self.render_quality == "m":
                media = "720p30"
            elif self.render_quality == "l":
                media = "480p15"
            else:
                media = "1080p60"

            os.system(

                f"explorer E:\\Udemy\\Management\\lecture_helper\\media\\videos\\lecture\\{media}")
            self.script_info_2.setText("Rendered ✅")
            self.script_info_2.setStyleSheet("color: green")
        except Exception as e:
            print(e)
            self.script_info_2.setText("Rendering Failed ❌")
            self.script_info_2.setStyleSheet("color: red")

    def initialize_state(self):
        self.automation_data = self.load_automation_data()
        self.wait_times = []
        self.wait_limit = self.get_wait_limit()

        self.populate_slides()
        self.current_slide = 0

        self.lcd_seconds.display(1)

        # set current. prev . next images
        self.set_image(self.current_image, f"{self.folder}/slides/slide0")
        self.set_image(self.prev_image, "no_slide.jpg")
        self.set_image(self.next_image, f"{self.folder}/slides/slide1")

    def get_folder(self):
        self.folder = str(QFileDialog.getExistingDirectory(
            self, "Select Your Manim Code Folder"))
        self.folder_label.setText(self.folder+" ✅")
        self.folder_label.setStyleSheet("color:black")
        try:
            self.initialize_state()
        except:
            print(
                "Not correct manim configuration, please choose the right folder with manim animation code.")
            dlg = Dialog()
            dlg.label.setText(
                "Not correct manim configuration, please choose the right folder with manim animation code.")
            dlg.exec()

    def start_recording(self):
        self.initiate_start_time()
        self.automation_data = self.load_automation_data()
        self.wait_times = []
        self.current_status_value.setText("0.0")
        self.recording_status.setText("Recording")
        self.recording_status.setStyleSheet("color:green")
        # reset slides
        self.current_slide = 0
        self.lcd_seconds.display(1)

        self.set_image(self.current_image, f"{self.folder}/slides/slide0")
        self.set_image(self.prev_image, "no_slide.jpg")
        self.set_image(self.next_image, f"{self.folder}/slides/slide1")
        self.initialize_script()
        self.textBrowser.setText(self.script[self.current_slide])
# call the record.py as subprocess
        # subprocess.Popen('start /wait python record.py', shell=True)

    def initialize_script(self):
        try:
            f = open(f"{self.folder}/script.dat", "r")
            t = json.loads(f.read())
            self.script = t
            return t
        except:
            t = np.repeat("Error Loading Slides", self.wait_limit)
            self.script = t
            return t

    def get_wait_limit(self):
        n = 0
        for i in self.automation_data:
            if i[1] == 'wait_time':
                n += 1
        return n

    def keyPressEvent(self, event):
        if type(event) == QKeyEvent:
            # 65, 68 = (a,d)
            # print(event.key())
            if event.key() == 68 and len(self.wait_times) < self.wait_limit:
                try:
                    t = self.get_end_time()
                    self.current_status_value.setText(str(t))
                    # self.initiate_start_time()
                    self.update_wait_time(t)
                    if len(self.wait_times) >= self.wait_limit:
                        self.current_status_value.setText("All Done")
                        self.current_status_value.setStyleSheet("color: red")
                        self.recording_status.setText("RECORDING ✅")
                        self.save_times_locally()
                        print(self.wait_times)
                    # get next slide
                except:

                    dlg = Dialog(self)
                    dlg.exec()

            event.accept()
        else:
            event.ignore()

    def initiate_start_time(self):
        self.start_time = time.time()

    def get_end_time(self):
        end = time.time()
        return end - self.start_time

    def load_automation_data(self):
        try:
            f = open(f"{self.folder}/initial_automation_data.dat")
            data = json.loads(f.read())
            return data
        except:
            return None

    def update_wait_time(self, wait_time):
        init_time = self.get_init_times_before_wait()
        if wait_time < init_time:
            self.current_status_value.setText(
                "wait time is bigger than animation time")
            # show on pyqt
        else:
            # add wait time
            self.wait_times.append(wait_time - init_time)
            # pop [anim, anim...->wait]
            self.pop_times_till_first_wait()
            # update slide
            self.get_next_slide()
            self.initiate_start_time()
        # if wait time is less than init time.. its bad.
        # pop all init times before wait

        # pop wait time..
        pass

    def pop_times_till_first_wait(self):
        new_automation_data = self.automation_data.copy()
        for i in self.automation_data:
            if i[1] != 'animation_time':
                new_automation_data.pop(0)
                self.automation_data = new_automation_data.copy()
                return True
            else:
                new_automation_data.pop(0)
        return False

    def get_next_slide(self):
        if (self.current_slide == self.wait_limit - 1):
            # no next slide
            pass
        else:
            self.set_image(self.current_image,
                           self.slides[self.current_slide+1])
            # prev
            if self.current_slide >= 0:
                self.set_image(self.prev_image,
                               self.slides[self.current_slide])
            else:
                self.set_image(self.prev_image, "no_slide.jpg")
            # next
            if self.current_slide + 2 < self.wait_limit:
                self.set_image(self.next_image,
                               self.slides[self.current_slide+2])
            else:
                self.set_image(self.next_image, "no_slide.jpg")

            self.lcd_seconds.display(self.current_slide+2)
            self.current_slide += 1
        self.textBrowser.setText(self.script[self.current_slide])

    def get_init_times_before_wait(self):
        init_time = 0
        for i in self.automation_data:
            if i[1] == 'animation_time':
                init_time += i[0]
            else:
                return init_time
        return init_time

    def save_times_locally(self):
        try:
            f = open(f"{self.folder}/loaded_times.dat", "w")
            f.write(json.dumps(self.wait_times))
            f.close()
            # for rendering purposes loaded_times will be created in the code folder
            f = open(f"loaded_times.dat", "w")
            f.write(json.dumps(self.wait_times))
            f.close()
            self.current_status_value("Wait times saved")

        except Exception as e:
            print(e)

# slides
    def set_image(self, label, image):
        image_profile = QImage(image).scaled(label.width(), label.height(),
                                             Qt.KeepAspectRatio)
        label.setPixmap(QPixmap.fromImage(image_profile))

    def populate_slides(self):
        self.slides = []
        for i in range(self.wait_limit):
            self.slides.append(f"{self.folder}/slides/slide{str(i)}.jpg")
        print(self.slides)


app = QApplication([])
window = MainWindow()
window.show()
app.exec()
