


def allowed_file(filename, allowed_format):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_format