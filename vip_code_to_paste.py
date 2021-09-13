from manim import *
import json


class BasicLecture(Scene):
    def construct(self):
        # VIP RENDER CONSTRAINTS
        self.counter = 0
        self.automation_data = []
        self.loaded_waiting_time = self.get_waiting_time()
        # VIP CONSTRAINTS ABOVE -- WRITE CODE BELOW
        # Write animation code below
        # MAKE SURE TO FOLLOW SOME COnVention or nothing will work
        #there are only 2 rules

        # 1: instead of calling self.wait(time) always call self.wait_and_count() 'dont pass any time as that's wht u set during rec time'
        # 2: every animation must have run_time and give run_time by calling a function like ...
        # 2... self.play(SomeAnim, runtime = self.get_runtime() )
# -----------------------


# -----------------------
#   only write animation above
        self.write_automation_data()

    def wait_and_count(self, t=2):
        # get wait time from list
        if self.loaded_waiting_time != []:
            t = self.loaded_waiting_time.pop(0)
            self.automation_data.append([t, "wait_time"])
            return self.wait(t)

        self.automation_data.append([t, "wait_time"])
        return self.wait(t)

    def get_runtime(self, t=1):
        self.automation_data.append([t, "animation_time"])
        return t

    def get_waiting_time(self):
        # check for the input file.. if it doesnt exist.. initialize empty
        try:
            f = open("loaded_times.dat")
            js = json.loads(f.read())
            return js

        except Exception as e:
            print(e)
            return []

    def write_automation_data(self):
        try:
            f = open("initial_automation_data.dat", "w")
            f.write(json.dumps(self.automation_data))
            f = open("file_data.dat", "w")
            f.write(type(self).__name__)
            f.close()
        except Exception as e:
            print(e)
            print("error occured while writing automation data")
