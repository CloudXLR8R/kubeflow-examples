from tempfile import mkstemp, mkdtemp


def get_tmp_dir(prefix, suffix=""):
    return mkdtemp(prefix=f"{prefix}_", suffix=suffix)


def get_tmp_filename(prefix, suffix=""):
    _, filepath = mkstemp(prefix=f"{prefix}_", suffix=suffix)
    return filepath
