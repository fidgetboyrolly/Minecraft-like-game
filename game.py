import re

class FidgetInterpreter:
    def __init__(self, file_path):
        self.file_path = file_path
        self.sprites = {}
        self.objects = {}

    def parse_line(self, line):
        line = line.strip()

        if not line or line.startswith('('):  # Skip empty lines and comments
            return

        if line.startswith('<display>'):
            print("Starting display section")
        elif line.startswith('<cam'):
            sys = self.extract_attribute(line, 'sys')
            print(f"Camera system: {sys}")
        elif line.startswith('<bg'):
            colour = self.extract_attribute(line, 'colour')
            print(f"Background colour: {colour}")
        elif line.startswith('<f '):
            func_id = self.extract_attribute(line, 'id')
            csv = self.extract_attribute(line, 'csv')
            c = self.extract_attribute(line, 'c')
            s = self.extract_attribute(line, 's')
            v = self.extract_attribute(line, 'v')
            print(f"Function: {func_id}, CSV: {csv}, Change: {c}, Sprite: {s}, Variable: {v}")
        elif line.startswith('<sprite'):
            sprite_id = self.extract_attribute(line, 'id')
            attributes = self.extract_attributes(line)
            self.sprites[sprite_id] = attributes
            print(f"Sprite: {sprite_id}, Attributes: {attributes}")
        elif line.startswith('<object'):
            obj_id = self.extract_attribute(line, 'id')
            attributes = self.extract_attributes(line)
            self.objects[obj_id] = attributes
            print(f"Object: {obj_id}, Attributes: {attributes}")

    def extract_attribute(self, line, attribute):
        pattern = f'{attribute}="([^"]*)"'
        match = re.search(pattern, line)
        return match.group(1) if match else None

    def extract_attributes(self, line):
        attributes = {}
        pattern = r'(\w+)="([^"]*)"'
        matches = re.findall(pattern, line)
        for key, value in matches:
            attributes[key] = value
        return attributes

    def run(self):
        with open(self.file_path, 'r') as file:
            for line in file:
                self.parse_line(line)

# Example usage
interpreter = FidgetInterpreter('game.fidscy')
interpreter.run()
