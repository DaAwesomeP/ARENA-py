from arena import *

scene = Scene(host="arenaxr.org", realm="realm", scene="example")

@scene.run_once
def make_box():
    scene.add_object(Box())

scene.run_tasks()
