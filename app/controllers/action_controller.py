import threading

from fastapi import APIRouter
from fastapi.responses import RedirectResponse

from app.scheduled_runner import run


router = APIRouter()

_run_lock = threading.Lock()


@router.post("/actions/run-now")
def run_now():
    """
    Trigger the Personal Executive AI workflow manually.

    Only one run may execute at a time.
    """

    if not _run_lock.acquire(blocking=False):
        return RedirectResponse(
            url="/?run_status=busy",
            status_code=303,
        )

    try:
        run()

        return RedirectResponse(
            url="/?run_status=success",
            status_code=303,
        )

    except Exception:
        return RedirectResponse(
            url="/?run_status=failed",
            status_code=303,
        )

    finally:
        _run_lock.release()