#
# cocos2d:
# http://cocos2d.org
#
# An example of how to generate a 3D scene manually
# Of course, the easiest way is to execute an Waves3D action,
# but this example is provided to show the
# 'internals' of generating a 3D effect.
#

import sys
import os

import pyglet
from pyglet.gl import *
import Box2D as box2d
from settings import fwSettings
import cocos
from cocos.actions import *
from cocos.director import director
from cocos.sprite import Sprite
from cocos.euclid import Point2,Point3
import math


class Framework(object):
    """
    The main testbed framework.
    It handles basically everything:
    * The initialization of pygame, Box2D
    * Contains the main loop
    * Handles all user input.

    You should derive your class from this one to implement your own tests.
    See test_Empty.py or any of the other tests for more information.
    """

    def __init__(self):
        name = "None"


        # COCOS INIT
        director.init()

        # enable depth test
        director.set_depth_test()

        # Box2D Initialization
        self.worldAABB=box2d.b2AABB()
        self.worldAABB.lowerBound = (-200.0, -100.0)
        self.worldAABB.upperBound = ( 200.0, 200.0)
        gravity = (0.0, -10.0)
        doSleep = True

        self.world = box2d.b2World(self.worldAABB, gravity, doSleep)

        # self.debugDraw = CairoDebugDraw()
        # self.world.SetDebugDraw(self.debugDraw)

        settings = fwSettings
        self.settings = settings
        self.flag_info = [ ('draw_shapes', settings.drawShapes,
                            box2d.b2DebugDraw.e_shapeBit),
                           ('draw_joints', settings.drawJoints,
                            box2d.b2DebugDraw.e_jointBit),
                           ('draw_controlers', settings.drawControllers,
                            box2d.b2DebugDraw.e_controllerBit),
                           ('draw_core_shapes', settings.drawCoreShapes,
                            box2d.b2DebugDraw.e_coreShapeBit),
                           ('draw_aabbs', settings.drawAABBs,
                            box2d.b2DebugDraw.e_aabbBit),
                           ('draw_obbs', settings.drawOBBs,
                            box2d.b2DebugDraw.e_obbBit),
                           ('draw_pairs', settings.drawPairs,
                            box2d.b2DebugDraw.e_pairBit),
                           ('draw_center_of_masses', settings.drawCOMs,
                            box2d.b2DebugDraw.e_centerOfMassBit),]

    def run(self):
        """
        Main loop.
        """
        s = cocos.scene.Scene()
        layer = cocos_box2d_layer()
        layer.world = self.world
        layer.settings = self.settings
        s.add(layer)
        director.run( s )


class cocos_box2d_layer( cocos.layer.Layer ):
    world = None
    settings = None
    zoom = 10

    def __init__( self ):

        super(cocos_box2d_layer,self).__init__()

        # load the image
        self.image = pyglet.resource.image('grossini.png')

        # get image size
        x,y = 200, 200 # self.image.width, self.image.height

        self.schedule(self.step)


    def on_enter(self):
        super(cocos_box2d_layer,self).on_enter()

        director.push_handlers(self.on_resize)

        # sprite3.do(MoveTo((620,300)))

        # the layer is on "stage"
        self.elapsed = 0


    def on_resize( self, width, height ):
        # change the 2D projection to 3D
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(90, 1.0*width/height, 0.1, 400.0)
        glMatrixMode(GL_MODELVIEW)

    def draw( self ):
        super(cocos_box2d_layer,self).draw()

        glLoadIdentity()

        bodies = self.world.GetBodyList()
        i = 0
        for b in bodies:
            sprite = b.GetUserData()
            if not sprite:
                sprite = Sprite(self.image)
                self.add(sprite)
                b.SetUserData(sprite)

            sprite.position = (b.position.x * self.zoom), (b.position.y * self.zoom)
            degrees = (b.GetAngle() * 180) / math.pi
            sprite.rotation = degrees

        # center the image
        glTranslatef(-320, -240, -320.0)


    def step( self, dt ):

        self.elapsed += dt
        amplitud = 32
        self.world.Step(dt,
                        self.settings.velocityIterations,
                        self.settings.positionIterations)



def main(test_class):
    """
    Loads the test class and executes it.
    """
    print "Loading %s..." % test_class.name
    test = test_class()
    if fwSettings.onlyInit:
        return
    test.run()

if __name__=="__main__":
    from test_empty import Empty
    main(Empty)
