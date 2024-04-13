from . import AbstractGameFSM
from utils import vec, magnitude, EPSILON, scale, RESOLUTION
import time

from statemachine import State


class MovementFSM(AbstractGameFSM):

    def __init__(self, obj):
        super().__init__(obj)

    def update(self, seconds):
        super().update(seconds)

        pass  # Add out of bounds checks here


class EnemyFSM(MovementFSM):
    """Axis-based acceleration with gradual stopping."""
    #not_moving = State(initial=True)

    walking = State(initial=True)
    waiting = State()
    chasing = State()

    #stalemate = State()
    stopWalking = walking.to(waiting)
    stopWaiting = waiting.to(walking)
    gochasing = walking.to(chasing) | waiting.to(chasing)
    backing = chasing.to(walking)
    '''
    decrease = not_moving.to(negative) | positive.to(
        stalemate) | negative.to.itself(internal=True)

    increase = not_moving.to(positive) | negative.to(
        stalemate) | positive.to.itself(internal=True)

    stop_decrease = negative.to(not_moving) | stalemate.to(
        positive) | not_moving.to.itself(internal=True)

    stop_increase = positive.to(not_moving) | stalemate.to(
        negative) | not_moving.to.itself(internal=True)

    stop_all = not_moving.to.itself(internal=True) | negative.to(not_moving) | \
        positive.to(not_moving) | stalemate.to(not_moving)'''

    def __init__(self, obj, twoPoints=None):
        self.range = twoPoints
        self.nthTarget = 0
        self.target = twoPoints[0]
        self.waitLimit = 2
        self.waitTimer = 0
        ##self.LastTime = time.perf_counter()
        super().__init__(obj)

    def update(self, map, kirbyPosition=vec(-15, -15), seconds=0):
        '''
        if self == "positive":
            self.obj.velocity += self.direction * self.accel * seconds
        elif self == "negative":
            self.obj.velocity -= self.direction * self.accel * seconds

        elif self == "stalemate":
            pass
        else:
            if self.obj.velocity[self.axis] > self.accel * seconds:
                self.obj.velocity[self.axis] -= self.accel * seconds
            elif self.obj.velocity[self.axis] < -self.accel * seconds:
                self.obj.velocity[self.axis] += self.accel * seconds
            else:
                self.obj.velocity[self.axis] = 0
            '''

        # print(self.current_state.id)
        if self == "waiting":
            ##print(self.waitTimer, seconds)
            self.obj.velocity = vec(0, 0)
            # timeDiff=self.currentTime-self.LastTime

            self.waitTimer += seconds
            if self.waitTimer >= self.waitLimit:
                # print("stuck?")
                self.stopWaiting()
                self.waitTimer = 0
                self.nthTarget += 1
                self.target = self.range[self.nthTarget % len(self.range)]
                ##print("you are aiming for", self.target)
            if self.obj.see(map, kirbyPosition) == 1:
                ##print("go chasing while in waiting")
                self.gochasing()

        elif self == "walking":
            towards = scale(self.target-self.obj.position, 10)
            ##print("target:", self.target-self.obj.position)
            ##print("vel", self.obj.velocity, "pos", self.obj.position)
            self.obj.velocity = towards
            ##print(towards, "tow")

            if magnitude(self.obj.position-self.target) < 8:  # a veloctiy, a range, absolute
                self.stopWalking()

            if self.obj.see(map, kirbyPosition) == 1:
                ##print("go chasing while in walking")
                self.gochasing()

        elif self == "chasing":
            chasingObject = kirbyPosition  # sth, change later, which also chanegs
            towards = scale(chasingObject-self.obj.position, 20)
            self.obj.velocity = towards
            # if cannot see, go back
            if (self.obj.see(map, kirbyPosition) == 0):
                print("backing")
                self.backing()

        super().update(seconds)
