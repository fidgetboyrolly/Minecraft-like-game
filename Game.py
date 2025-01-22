import xml.etree.ElementTree as ET
import re

def parse_fidget_script(xml_string):
    xml_string = re.sub(r'<!DOCTYPE FIDGET>', '<docfidget>', xml_string)
    xml_string += '</docfidget>'

    try:
        root = ET.fromstring(xml_string)
    except ET.ParseError as e:
        return f"ParseError: {e}"
    
    output = []
    
    display = root.find("display")
    if display is not None:
        output.append("Display:")
        for child in display:
            if child.tag == "ren":
                output.append(f"  Render in: {child.attrib.get('3D', '2D')}")
            elif child.tag == "object":
                output.append(f"  Object: url={child.attrib['url']}, pos={child.attrib['pos']}, "
                              f"scale={child.attrib['scale']}, rotation={child.attrib['rotation']}, "
                              f"shape={child.attrib['shape']}")
                for subchild in child:
                    if subchild.tag == "material":
                        output.append(f"    Material: type={subchild.attrib['type']}, src={subchild.attrib.get('src', '')}, "
                                      f"value={subchild.attrib.get('value', '')}")
            elif child.tag == "camera":
                output.append(f"  Camera: pos={child.attrib['pos']}, rotation={child.attrib.get('rotation', 'N/A')}")
            elif child.tag == "light":
                output.append(f"  Light: type={child.attrib['type']}, intensity={child.attrib['intensity']}, "
                              f"pos={child.attrib['pos']}, color={child.attrib['color']}")
            elif child.tag == "bg":
                output.append(f"  Background: type={child.attrib['type']}, src={child.attrib.get('src', '')}, "
                              f"value={child.attrib.get('value', '')}")
    
    inter_board = root.find("inter")
    if inter_board is not None:
        output.append("Interactive Board:")
        for child in inter_board:
            if child.tag == "board":
                for button in child:
                    if button.tag == "button":
                        output.append(f"  Button: button={button.attrib['button']}, function={button.attrib['function']}")
    
    functions = root.find("functions")
    if functions is not None:
        output.append("Functions:")
        for child in functions:
            if child.tag == "box":
                output.append(f"  Box id={child.attrib.get('id', 'N/A')}")
                for subchild in child:
                    if subchild.tag == "f":
                        output.append(f"    Function: id={subchild.attrib['id']}, type={subchild.attrib['type']}, "
                                      f"direction={subchild.attrib.get('direction', 'N/A')}, distance={subchild.attrib.get('distance', 'N/A')}, "
                                      f"target={subchild.attrib.get('target', 'N/A')}")
    
    ent_list = root.find("ent")
    if ent_list is not None:
        for subchild in ent_list:
            if subchild.tag == "list":
                output.append("Entity List:")
                for child in subchild:
                    if child.tag == "sprite":
                        output.append(f"  Sprite: id={child.attrib['id']}, startpos={child.attrib['startpos']}, vb={child.attrib['vb']}, player={child.attrib.get('player', 'N/A')}")
                    elif child.tag == "object":
                        output.append(f"  Object: id={child.attrib['id']}, state={child.attrib['state']}, shape={child.attrib['shape']}, pos={child.attrib['pos']}")
    
    return "\n".join(output)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run_fidget')
def run_fidget():
    xml_string = """
    <!DOCTYPE FIDGET>
    <docfidget>
    <display>
      <ren="3D"></ren>
      <object url="textures/block.png" pos="0,0,0" scale="1,1,1" rotation="0,0,0" shape="cube">
        <material type="texture" src="textures/block.png"></material>
      </object>
      <object url="textures/grass.png" pos="0,-1,0" scale="1,1,1" rotation="0,0,0" shape="cube">
        <material type="texture" src="textures/grass.png"></material>
      </object>
      <object url="textures/wood.png" pos="1,0,0" scale="1,1,1" rotation="0,0,0" shape="cube">
        <material type="texture" src="textures/wood.png"></material>
      </object>
      <camera pos="0,5,10" rotation="30,0,0"></camera>
      <light type="directional" intensity="1.0" pos="10,10,10" color="#ffffff"></light>
      <bg type="color" value="#87CEEB"></bg>
    </display>
    <inter>
      <board>
        <button button="w" function="moveForward"></button>
        <button button="s" function="moveBackward"></button>
        <button button="a" function="moveLeft"></button>
        <button button="d" function="moveRight"></button>
        <button button="space" function="jump"></button>
        <button button="b" function="placeBlock"></button>
        <button button="n" function="removeBlock"></button>
      </board>
    </inter>
    <functions>
      <box id="move">
        <f id="moveForward" type="-move-" direction="z" distance="1"></f>
        <f id="moveBackward" type="-move-" direction="z" distance="-1"></f>
        <f id="moveLeft" type="-move-" direction="x" distance="-1"></f>
        <f id="moveRight" type="-move-" direction="x" distance="1"></f>
        <f id="jump" type="-move-" direction="y" distance="1"></f>
      </box>
      <box id="build">
        <f id="placeBlock" type="-create-" target="block" pos="2,0,0"></f>
        <f id="removeBlock" type="-destroy-" target="block"></f>
      </box>
    </functions>
    <ent>
      <list>
        <sprite id="player" player="true" startpos="0,1,0" shape="1,2,1" vb="move"></sprite>
        <object id="ground" state="solid" shape="20,1,20" pos="0,-1,0"></object>
        <object id="block" state="solid" shape="1,1,1" pos="2,0,0"></object>
      </list>
    </ent>
    </docfidget>
    """
    result = parse_fidget_script(xml_string)
    return result

if __name__ == '__main__':
    app.run(debug=True)
