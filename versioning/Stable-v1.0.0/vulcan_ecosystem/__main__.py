"""Default to Vulcan project validation."""

from .cli import validate_main


if __name__ == "__main__":
    raise SystemExit(validate_main())

