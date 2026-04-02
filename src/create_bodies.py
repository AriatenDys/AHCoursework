# imports
from utils import bubble_sort
from body import Body
from vector import R2Vector
from option_box import OptionBox

def get_box(self, label):
    """function to find a specific input box for creating a body"""
    for box in self.input_boxes:
        if box.label == label:
            return box
    return None

def create_body_from_input(self):
    """create a body from input boxes, validating each numerical input separately"""
    for box in self.input_boxes:
        if hasattr(box, "clear_error"):
            box.clear_error()

    data = {box.label: box.get_value().strip() for box in self.input_boxes if hasattr(box, "get_value")}

    # validate mass
    mass_box = get_box(self, "mass")
    if not data.get("mass"):
        mass_box.error = "required"
        return
    try:
        mass = float(data["mass"])
        if mass <= 0:
            mass_box.error = "> 0 only"
            return
    except ValueError:
        mass_box.error = "number only"
        return

    # validate velocity components
    vx_box = get_box(self, "vx")
    vy_box = get_box(self, "vy")
    if not data.get("vx"):
        vx_box.error = "required"
        return
    if not data.get("vy"):
        vy_box.error = "required"
        return
    try:
        vx = float(data["vx"])
    except ValueError:
        vx_box.error = "number only"
        return
    try:
        vy = float(data["vy"])
    except ValueError:
        vy_box.error = "number only"
        return

    # validate radius with default to 5
    radius_box = get_box(self, "radius")
    if data.get("radius"):
        try:
            radius = int(data["radius"])
            if radius <= 0:
                radius_box.error = "> 0 only"
                return
        except ValueError:
            radius_box.error = "number only"
            return
    else:
        radius = 5

    # validate colour with default to white
    colour_box = next((box for box in self.input_boxes if isinstance(box, OptionBox)))

    if colour_box:
        r, g, b = colour_box.get_selected_colour()
    else:
        r, g, b = (255, 255, 255)

    # name with default to "body"   
    name = data.get("name") or "body"

    # create the body
    body = Body(
        name=name,
        mass=mass,
        position=self.new_body_pos,
        velocity=R2Vector(x=vx, y=vy),
        radius=radius,
        colour=(r, g, b)
    )

    self.physics.bodies.append(body)
    name_box = get_box(self, "name")
    try:
        self.db.insert_planet(
            name=body.name,
            mass=body.mass,
            pos=body.position,
            vel=body.velocity,
            radius=body.radius,
            colour=body.colour
        )
    except OverflowError:
        name_box.error = "Number too large to use"
        self.input_boxes.clear()

    # sort bodies and clear input boxes
    bubble_sort(self.physics.bodies)
    self.input_boxes.clear()
    self.creating_body = False
    self.paused = False
