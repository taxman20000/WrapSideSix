# WrapSideSix/tasks/thread_runner.py

from PySide6.QtCore import QObject, Signal, Slot, QRunnable, QThreadPool
import logging
import traceback

# Logger Configuration
logger = logging.getLogger(__name__)

class _WorkerSignals(QObject):
    finished = Signal(object)
    error = Signal(tuple)  # (exception, traceback)
    progress = Signal(float)
    started = Signal()

class _Worker(QRunnable):
    def __init__(self, fn, *args, on_finish=None, on_error=None, on_progress=None, on_start=None,  **kwargs):
        super().__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = _WorkerSignals()

        if on_finish:
            self.signals.finished.connect(on_finish)
        if on_error:
            self.signals.error.connect(on_error)
        if on_progress:
            self.signals.progress.connect(on_progress)
        if on_start:
            self.signals.started.connect(on_start)

        # Add progress callback if function supports it
        if 'progress_callback' not in kwargs:
            self.kwargs['progress_callback'] = self.signals.progress.emit

    @Slot()
    def run(self):
        self.signals.started.emit()
        try:
            result = self.fn(*self.args, **self.kwargs)
            self.signals.finished.emit(result)
        except Exception as e:
            logger.error(f"Error in worker thread: {str(e)}")
            self.signals.error.emit((e, traceback.format_exc()))

def run_in_thread(fn, *args, on_finish=None, on_error=None, on_progress=None, on_start=None,
                 parent=None, **kwargs):
    """
    Runs `fn(*args, **kwargs)` in a background thread using QThreadPool.

    Args:
        fn: Function to execute
        *args: Arguments to pass to the function
        on_finish: Callback for successful completion
        on_error: Callback for errors
        on_progress: Callback for progress updates
        on_start: Callback when the thread begins execution
        parent: Parent object to prevent worker garbage collection
        **kwargs: Keyword arguments to pass to the function

    Returns:
        The worker instance
    """
    worker = _Worker(fn, *args, on_finish=on_finish, on_error=on_error,
                    on_progress=on_progress, on_start=on_start, **kwargs)

    # Store worker reference to prevent garbage collection
    if parent is not None:
        # Use a more appropriate attribute name without underscore
        if not hasattr(parent, "active_workers"):
            parent.active_workers = []
        parent.active_workers.append(worker)

        # Auto-remove on finish/error to prevent memory leak
        def _cleanup(_):
            try:
                if hasattr(parent, "active_workers") and worker in parent.active_workers:
                    parent.active_workers.remove(worker)
            except (ValueError, RuntimeError):
                pass

        worker.signals.finished.connect(_cleanup)
        worker.signals.error.connect(lambda _: _cleanup(None))

    # Set auto-delete and start the worker
    worker.setAutoDelete(True)
    QThreadPool.globalInstance().start(worker)

    return worker
