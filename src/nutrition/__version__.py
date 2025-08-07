try:
    from importlib.metadata import version
except ImportError:
    # Python < 3.8
    from importlib_metadata import version

def get_version():
    """Get version from package metadata"""
    try:
        return version("nutrition")
    except Exception:
        return "unknown"
