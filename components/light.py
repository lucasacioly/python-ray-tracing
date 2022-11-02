from basic_geom import Color, Point

class Light:
    # Point light source of a certain color
    
    position : Point = None
    color : Color = None

    def __init__(self, position : Point, color : Color) -> None:
        self.position = position
        self.color = color
    
    def get_color(self):
        return self.color.vector
    
    def get_position(self):
        return self.position.vector