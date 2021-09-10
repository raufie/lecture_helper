from manim import *
import os
import json
import sys
import pathlib


def get_frames_by_ffmpeg(folder, anim):

    try:
        pathlib.Path(f"{folder}/slides/").mkdir(parents=True, exist_ok=True)
    except:
        print("biatch")
    mp4_path = f"{folder}\\media\\videos\\lecture\\720p30\\{anim}.mp4"
    try:
        os.mkdir("slides")
    except:
        pass
    bash_script = "e:\\"
    times = []
    for i, t in enumerate(get_slide_times(folder)):
        secs = str(int(t - t//60 * 60 + t//60//60 * 60)).zfill(2)
        mins = str(int(t//60)).zfill(2)
        hours = str(int(t//60//60)).zfill(2)
        mili = str(int((t-int(t))*1000))
        time = hours+":"+mins+":"+secs+"."+mili
        times.append(time)
        out_path = f"{folder}/slides/slide{i}.jpg"
        command = f"ffmpeg -ss {time} -i {mp4_path} -vframes 1 -q:v 2 {out_path}  -y"
        bash_script += command+"\n"
        os.system('{}'.format(command))
    times.append(folder)
    make_log(times)


def get_slide_times(folder):
    times = []
    try:
        f = open(f"{folder}/initial_automation_data.dat", "r")
        loaded_initial_times = json.loads(f.read())
        # get cummulative up to the wait times
        cum = 0
        for i in loaded_initial_times:
            if i[1] == "wait_time":
                times.append(i[0]/2+cum)
            cum += i[0]

# enable slides to be made at miliseconds precision when using ffmpeg
        print(times)
        return times
    except Exception as e:
        print(e)
        return None


def make_log(t):

    f = open("log.txt", "w")
    f.write(json.dumps(t))

    f.close()


try:

    get_frames_by_ffmpeg(sys.argv[1], sys.argv[2])
    exit()
except Exception as e:
    print("THERE IS AN ERROR, ignore this if you see this for the first time")
    print(e)
    pass
