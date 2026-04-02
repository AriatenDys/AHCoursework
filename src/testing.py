import os
import sys

def test_database():
    from sql_commands import PlanetDB

    db = PlanetDB()
    print("Database opened:", db)
    db.close_db()
    print("Database closed:", db)


def test_vector():
    from vector import R2Vector

    v1 = R2Vector(x=2, y=3)
    v2 = R2Vector(x=-3, y=18)

    print("v1:", v1) # vector 1
    print("v2:", v2) # vector 2
    print("v1 repr:", v1.__repr__()) # vector repr 
    print("v1 str:", v1.__str__()) # vector str
    print("v1 class name:", v1.__class__.__name__) # vector class

    # arithmetic tests
    print("v1 * v2 =", v1 * v2) # dot product
    print("v1 + v2 =", v1 + v2) # addition
    print("v1 - v2 =", v1 - v2) # subtraction

    # comparison tests
    print("v1 > v2 ?", v1 > v2) # greater than
    print("v1 < v2 ?", v1 < v2) # less than


def test_physics_and_body():
    from vector import R2Vector
    from body import Body
    from physics import PhysicsSystem

    # test data
    sun = Body("sun", 50000, R2Vector(x=0,y=0), R2Vector(x=0,y=0), 15, (255,255,0))
    testbody = Body("testbody", 10, R2Vector(x=200,y=0), R2Vector(x=0,y=5), 5, (0,255,255))
    bodies = [sun, testbody]
    physics = PhysicsSystem(bodies)

    steps = 10
    for i in range(steps): # at somepoint ill do like a trace table to test this data
        physics.integrate()
        print(f"Step {i}")
        for b in bodies:
            print(b)
        print("-"*30)


def test_start_menu():
    try:
        import pygame
    except ImportError:
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pygame"])
        import pygame

    from infomenu import StartMenu
    from settings import WINDOW_HEIGHT, WINDOW_WIDTH, FONT_PATH

    pygame.init()
    display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    font_path = os.path.join(FONT_PATH, 'runescape_uf.ttf')
    font = pygame.font.Font(font_path, 24)

    menu = StartMenu()
    print("StartMenu created successfully.")

    menu.open()
    frame = 0

    running = True
    # simulate a few frames without user input
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            menu.handle_event(event)
        frame += 1
        menu.draw(display_surface)
        pygame.display.flip()
        print(f"Frame {frame} drawn successfully")

    pygame.quit()

def test_bubble():
    from body import Body
    from sql_commands import PlanetDB
    from settings import DATABASE_PATH
    from utils import bubble_sort
    db = PlanetDB(db_path=DATABASE_PATH)
    bodies = []

    for pdata in db.get_all_planets(): # sets up the bodies array using database data
        body = Body(name=pdata["name"], mass=pdata["mass"], position=pdata["position"], 
                    velocity=pdata["velocity"], radius=pdata["radius"], colour=pdata["colour"])
        bodies.append(body)
    print("before sort")
    for body in bodies:
        print(body.get_pos(), "mass:", body.mass)
    bubble_sort(bodies)
    print("after sort")
    for body in bodies:
        print(body.get_pos(), "mass:", body.mass)

def test_body():
    from body import Body
    from vector import R2Vector
    sun = Body("sun", 50000, R2Vector(x=0,y=0), R2Vector(x=0,y=0), 15, (255,255,0))
    testbody = Body("testbody", 10, R2Vector(x=200,y=0), R2Vector(x=0,y=5), 5, (0,255,255))

    bodies = [sun, testbody]
    print(bodies)

def run_all_tests():
    test_bubble()
    test_database()
    test_vector()
    test_physics_and_body()
    test_start_menu()
    test_body()


if __name__ == "__main__":
    run_all_tests()