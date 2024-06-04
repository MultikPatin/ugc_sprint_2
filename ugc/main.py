import sentry_sdk

from src.app import app
from src.core.config import settings

if __name__ == "__main__":
    sentry_sdk.init(
        dsn=settings.sentry.dsn,
        traces_sample_rate=1.0,
        profiles_sample_rate=1.0,
    )
    app.run()
