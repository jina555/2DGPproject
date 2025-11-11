world=[[],[],[]]

collision_pairs={}

def add_object(o,depth=0):
    world[depth].append(o)

def add_objects(ol,depth=0):
    world[depth]+=ol

def remove_object(o):
    for layer in world:
        if o in layer:
            layer.remove(o)
            remove_collision_objects(o)
            del o
            return

def update():
    for layer in world:
        for o in layer.copy():
            o.update()

def render():
    for layer in world:
        for o in layer:
            o.draw()

def clear():
    global world
    for layer in world:
        layer.clear()
    collision_pairs.clear()
    world=[[],[],[]]

def collide(a,b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    return True
def add_collision_pair(group,a,b):
    if group not in collision_pairs:
        collision_pairs[group]=[[],[]]
    if a:
        collision_pairs[group][0].append(a)
    if b:
        collision_pairs[group][1].append(b)

def get_player():

    if 'player:monster' in collision_pairs and collision_pairs['player:monster'][0]:
        return collision_pairs['player:monster'][0][0]
    return None


def handle_collisions():
    for group, pairs in collision_pairs.items():

        if not pairs[0] or not pairs[1]:
            continue
        for a in pairs[0]:
            for b in pairs[1]:
                if collide(a,b):
                    a.handle_collision(group,b)
                    b.handle_collision(group,a)

def remove_collision_objects(o):
    for group, pairs in collision_pairs.items():
        if o in pairs[0]:
            pairs[0].remove(o)
        if o in pairs[1]:
            pairs[1].remove(o)