from PIL import Image, ImageDraw


text = "some text"

new = Image.new('RGB', (300, 300), color=(242, 234, 225))

draw = ImageDraw.Draw.(new)

draw.text((100,100), text, fill=(255, 255, 255))

new.save()
