from collections import deque

from kivy.clock import Clock

try:
    import android

    class ShakeDetector(object):

        def __init__(self):
            android.accelerometer_enable(True)
            Clock.schedule_interval(self.detect_motion, 0.1)
            self.last = None
            self.history = deque()
            self.shake_callback = None
            self.enabled = True

        def unlock(self, *args):
            self.enabled = True

        def lock(self, timeout):
            self.enabled = False
            Clock.schedule_once(self.unlock, timeout)

        def detect_motion(self, *args):
            if self.enabled:
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
                            self.shake_callback(rolling_average)

                self.last = accel

        def on_shake(self, callback):
            self.shake_callback = callback

except ImportError:
    class ShakeDetector(object):
        def on_shake(self, callback):
            pass
