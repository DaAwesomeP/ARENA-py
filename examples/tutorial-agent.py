from arena import *
import random, math

arena = Arena("arena.andrew.cmu.edu", "realm", "public", "example")

model_url = "/store/users/wiselab/models/FaceCapHeadGeneric/FaceCapHeadGeneric.gltf"
avatar = GLTF(
        object_id="my_avatar",
        url=model_url,
        position=(0,1.75,-1.5),
        rotation=(0,0,0),
        scale=(10,10,10)
    )
arena.add_object(avatar)

speech = Text(
        object_id="my_text",
        text="Hello!",
        parent=avatar,
        position=(0,0.3,0),
        scale=(0.4,0.4,0.4)
    )
arena.add_object(speech)

instructions = Text(
        object_id="instructions",
        color=(100,50,75),
        text = "",
        position=(15.2,7,0),
        scale=(3,3,3)
    )

ticks = 0

code = []

cube_ready = False

def talk():
    morph = {
        "gltf-morph__0": {
            "morphtarget": "shapes.jawOpen",
            "value": str(random.randint(0,70)/100)
        },
    }
    arena.update_object(avatar, **morph)

def close_mouth():
    morph = {
        "gltf-morph__0": {
            "morphtarget": "shapes.jawOpen",
            "value": str(0.1)
        },
    }
    arena.update_object(avatar, **morph)

def update_code():
    # hack (but an allowed hack), set "align" attribute
    instructions.data.text = {
            "value": "\n\n".join(code),
            "align": "left"
        }
    arena.add_object(instructions)

@arena.run_forever(interval_ms=50)
def main():
    global ticks
    global code
    global cube_ready

    if ticks < 80:
        talk()

        if ticks == 20:
            speech.data.text = "Welcome to the ARENA!"
            arena.add_object(speech)
        if ticks == 40:
            speech.data.text = "My name is Mr. Tutorial Avatar, but you can\ncall me TA. I am here to help guide you"
            arena.add_object(speech)
        if ticks == 60:
            speech.data.text = "Follow me!"
            arena.add_object(speech)

    if ticks == 80:
        close_mouth()

    if ticks == 90:
        avatar.data.rotation.y = math.pi
        arena.update_object(avatar)

    if 90 < ticks < 160:
        avatar.data.position.z -= 0.2
        avatar.data.position.y += 0.01
        arena.update_object(avatar)

    if 160 < ticks < 180:
        avatar.data.rotation = Rotation(0,0,0)
        arena.update_object(avatar)

    if 175 < ticks < 500:
        talk()

        if ticks == 180:
            speech.data.text = "Let's write a\nPython program!"
            arena.add_object(speech)

            instructions.data.position.z = avatar.data.position.z
            arena.add_object(instructions)

        if ticks == 200:
            speech.data.text = "To my left is the Python\ncode I will have you write:"
            arena.add_object(speech)

            code += ["from arena import *"]
            update_code()

        if ticks == 220:
            speech.data.text = "Can you type the code I\nshow next to me?"
            arena.add_object(speech)

        if ticks == 250:
            speech.data.text = "Let's start by importing the\nARENA-py library and initializing it:"
            arena.add_object(speech)

        if ticks == 270:
            code += [f"arena = Arena(\"{arena.HOST}\", \"{arena.REALM}\", \"{arena.NAMESPACE}\", \"{arena.SCENE}\")"]
            update_code()

        if ticks == 300:
            speech.data.text = "Next, let's create our\nfirst Object: a cube!"
            arena.add_object(speech)

        if ticks == 320:
            code += [f"cube = Cube(object_id=\"my_cube\", position=(0,4,-2), scale=(2,2,2))"]
            update_code()

        if ticks == 340:
            speech.data.text = "Next, let's add that cube\nto the ARENA:"
            arena.add_object(speech)

        if ticks == 360:
            code += ["arena.add_object(cube)"]
            update_code()

        if ticks == 380:
            speech.data.text = "Finally, let's run the\nARENA-py event loop:"
            arena.add_object(speech)

        if ticks == 400:
            code += ["arena.run_tasks()"]
            update_code()

        if ticks == 420:
            speech.data.text = "Can you copy this code and\nexecute it? I'll wait!"
            arena.add_object(speech)

        if 420 < ticks < 460:
            avatar.data.position.z += 0.2
            avatar.data.position.y -= 0.01
            arena.update_object(avatar)

        if ticks == 480:
            close_mouth()

            def cube_made(msg):
                global cube_ready
                if "object_id" in msg:
                    cube_ready = (msg["object_id"] == "my_cube")

            arena.new_obj_callback = cube_made

    if cube_ready:
        talk()
        speech.data.text = "Congrats, you did it!"
        arena.add_object(speech)
        arena.delete_object(instructions)
        cube_ready = False

    ticks += 1

arena.run_tasks()
