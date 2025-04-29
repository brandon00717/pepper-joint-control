# coding=utf-8
__version__ = "1.1-threaded-py27"

import sys

import qi, math, time, threading
import stk.runner, stk.events, stk.services, stk.logging

class Joint(object):
    """
    Multijoint threaded hold service for Python 2.7 with directional speech.
    """
    APP_ID = "com.aldebaran.Joint"

    # Supported joints and user-friendly labels
    JOINTS = [
        "RShoulderPitch", "RElbowYaw", "RWristYaw",
        "LShoulderPitch", "LElbowYaw", "LWristYaw",
        "HeadYaw"
    ]
    LABELS = {
        "RShoulderPitch": "Right shoulder",
        "RElbowYaw":      "Right elbow",
        "RWristYaw":      "Right wrist",
        "LShoulderPitch": "Left shoulder",
        "LElbowYaw":      "Left elbow",
        "LWristYaw":      "Left wrist",
        "HeadYaw":        "Head"
    }

    def __init__(self, qiapp):
        self.qiapp    = qiapp
        self.services = stk.services.ServiceCache(qiapp.session)
        self.logger   = stk.logging.get_logger(qiapp.session, self.APP_ID)
        self.tts      = self.services.ALTextToSpeech
        self.motion   = self.services.ALMotion

        # Prep arms
        try:
            self.motion.wakeUp()
            for limb in ("RArm", "LArm"):
                self.motion.setBreathEnabled(limb, False)
                self.motion.setIdlePostureEnabled(limb, False)
            # self.motion.setStiffnesses(["RArm","LArm"], [1.0,1.0])
        except Exception as e:
            self.logger.warning("Arm prep failed: %s", e)

        # Initialize targets and threads
        self.targets  = {j: 0.0 for j in self.JOINTS}
        self._events  = {j: threading.Event() for j in self.JOINTS}
        self._threads = {j: None for j in self.JOINTS}

    def _hold_loop(self, joint_name):
        stop_evt = self._events[joint_name]
        while not stop_evt.is_set():
            try:
                self.motion.setAngles(joint_name,
                                      self.targets[joint_name],
                                      0.05)
            except Exception as e:
                self.logger.warning("%s hold-loop failed: %s", joint_name, e)
            time.sleep(0.1)

    def _compute_direction(self, joint_name, old_deg, new_deg):
        delta = new_deg - old_deg
        if abs(delta) < 1e-6:
            return "to %d°" % new_deg
        if "ShoulderPitch" in joint_name:
            return "raising" if delta < 0 else "lowering"
        if "ElbowYaw" in joint_name:
            return "twisting inward" if delta < 0 else "twisting outward"
        if "WristYaw" in joint_name:
            return "rotating inward" if delta < 0 else "rotating outward"
        if "HeadYaw" in joint_name:
            return "turning left" if delta > 0 else "turning right"
        return ""

    @qi.bind(returnType=qi.Void, paramsType=[qi.String, qi.Float])
    def setJoint(self, joint_name, angle_deg):
        if joint_name not in self.JOINTS:
            self.logger.warning("Unknown joint: %s", joint_name)
            return
        # compute old and clamp new
        old_deg = self.targets[joint_name] * 180.0 / math.pi
        # clamp based on joint type
        if "ShoulderPitch" in joint_name:
            lo, hi = -90.0, 90.0
        elif "ElbowYaw" in joint_name:
            lo, hi = -120.0, 120.0
        elif "WristYaw" in joint_name:
            lo, hi = -180.0, 180.0
        else:  # HeadYaw
            lo, hi = -90.0, 90.0
        deg = max(lo, min(hi, angle_deg))
        rad = deg * math.pi / 180.0
        self.targets[joint_name] = rad

        # speak direction
        direction = self._compute_direction(joint_name, old_deg, deg)
        try:
            self.tts.say("%s %s" % (self.LABELS[joint_name], direction))
        except Exception:
            pass

        # initial move
        try:
            self.motion.setAngles(joint_name, rad, 0.25)
        except Exception as e:
            self.logger.warning("Initial move %s failed: %s", joint_name, e)

        # restart hold thread
        evt = self._events[joint_name]
        evt.set()
        th = self._threads[joint_name]
        if th:
            th.join(0.5)
        new_evt = threading.Event()
        self._events[joint_name] = new_evt
        t = threading.Thread(target=self._hold_loop, args=(joint_name,))
        t.daemon = True
        t.start()
        self._threads[joint_name] = t

    @qi.bind(returnType=qi.Float, paramsType=[qi.String])
    def getJoint(self, joint_name):
        rad = self.targets.get(joint_name, 0.0)
        return rad * 180.0 / math.pi

    @qi.bind(returnType=qi.Void, paramsType=[qi.String])
    def resetJoint(self, joint_name):
        if joint_name not in self.JOINTS:
            return
        evt = self._events[joint_name]
        evt.set()
        th = self._threads[joint_name]
        if th:
            th.join(0.5)
        neutral = 80.0 if "ShoulderPitch" in joint_name else 0.0
        rad = neutral * math.pi / 180.0
        try:
            self.motion.setAngles(joint_name, rad, 0.25)
        except Exception as e:
            self.logger.warning("Reset %s failed: %s", joint_name, e)

    @qi.bind(returnType=qi.Void, paramsType=[])
    def stop(self):
        # stop all threads and reset angles
        for j in self.JOINTS:
            evt = self._events[j]
            evt.set()
            th = self._threads[j]
            if th:
                th.join(0.5)
            # reset
            neutral = 80.0 if "ShoulderPitch" in j else 0.0
            rad = neutral * math.pi / 180.0
            try:
                self.motion.setAngles(j, rad, 0.4)
            except:
                pass

        # rest and exit
        self.qiapp.quit()
    @qi.nobind
    def on_stop(self):
        # ensure complete shutdown
        self.stop()
if __name__ == "__main__":
    stk.runner.run_service(Joint)
