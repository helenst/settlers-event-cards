from collections import deque

from kivy.clock import Clock

try:
    import android

    class ShakeDetector(object):

        def __init__(self, on_shake=None):
            android.accelerometer_enable(True)
            Clock.schedule_interval(self.detect_motion, 0.1)
            self.last = None
            self.history = deque()
            self.shake_callback = on_shake
            self.locked = False

        def unlock(self, *args):
            self.locked = False

        def lock(self, timeout):
            self.locked = True
            Clock.schedule_once(self.unlock, timeout)

        def enable(self):
            android.accelerometer_enable(True)
            Clock.schedule_interval(self.detect_motion, 0.1)

        def disable(self):
            android.accelerometer_enable(False)
            Clock.unschedule(self.detect_motion)

        def detect_motion(self, *args):
            if not self.locked:
                accel = android.accelerometer_reading()
                if self.last:
                    diff = sum(accel) - sum(self.last)

                    history_size = 10
                    movement_threshold = 5
                    if len(self.history) == history_size:
                        self.history.popleft()
                    self.history.append(abs(diff))

                    if len(self.history) == history_size:
                        rolling_average = sum(self.history) / len(self.history)
                        if rolling_average > movement_threshold:
                            self.lock(2)
                            self.history.clear()
                            self.shake_callback()

                self.last = accel

        def on_shake(self, callback):
            self.shake_callback = callback

except ImportError:
    class ShakeDetector(object):
        def __init__(self, on_shake):
            pass

        def enable(self):
            pass

        def disable(self):
            pass
