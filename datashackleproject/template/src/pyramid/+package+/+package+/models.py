from p2.datashackle.core import Model, model_config


@model_config(tablename='person')
class Person(Model):
    """Our person model, which is maintained through admin UI. Point browser to http://localhost:8080/datashackle"""

@model_config(tablename='p2_media')
class Media(Model):
    """Datashackle sys table where all media files are stored."""
