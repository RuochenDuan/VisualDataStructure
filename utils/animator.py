# utils/animator.py
from PyQt6.QtCore import QObject, QTimer, pyqtSignal


class Animator(QObject):
    req_step_played = pyqtSignal(object, int, int)  # (step, index, total)
    req_finished = pyqtSignal()
    req_started = pyqtSignal()

    def __init__(self, interval_ms=500):
        super().__init__()
        self._steps = []
        self._cur_index = 0
        self._interval = interval_ms
        self._timer = QTimer()
        self._timer.timeout.connect(self._play_next_step)

    def load_steps(self, steps):
        self.stop()
        self._steps = steps
        self._cur_index = 0

    def start(self):
        if self.is_running() or not self._steps:
            return
        self.req_started.emit()
        self._timer.start(self._interval)

    def pause(self):
        self._timer.stop()

    def resume(self):
        if self._cur_index < len(self._steps) and not self.is_running():
            self._timer.start(self._interval)

    def stop(self):
        """停止并重置索引"""
        self._timer.stop()
        self._cur_index = 0

    def is_running(self) -> bool:
        return self._timer.isActive()

    def _play_next_step(self):
        if self._cur_index >= len(self._steps):
            self._timer.stop()
            self.req_finished.emit()
            return

        step = self._steps[self._cur_index]
        self.req_step_played.emit(step, self._cur_index, len(self._steps))
        self._cur_index += 1
