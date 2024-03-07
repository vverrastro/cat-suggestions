from pydantic import BaseModel
from cat.mad_hatter.decorators import plugin

class MySettings(BaseModel):
    number_of_suggestions: int = 2

@plugin
def settings_schema():
    return MySettings.schema()