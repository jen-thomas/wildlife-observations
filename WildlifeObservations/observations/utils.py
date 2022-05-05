def field_or_na(model, field_name):
    if model is None:
        return ''
    else:
        return getattr(model, field_name)