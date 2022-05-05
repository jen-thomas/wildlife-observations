def field_or_empty_string(model, field_name):
    if model is None:
        return ''
    else:
        return getattr(model, field_name)