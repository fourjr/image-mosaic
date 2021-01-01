from glob import iglob
from PIL import Image
BOX_SIZE = (15, 15)


def get_average_color(data):
    sumr = 0
    sumg = 0
    sumb = 0
    sumall = 0

    for i in data:
        r, g, b = i[:3]
        try:
            a = i[3]
        except IndexError:
            a = 255

        if a == 255:
            sumr += r
            sumg += g
            sumb += b
            sumall += 1

    sumall = max(sumall, 1)
    return (sumr / sumall, sumg / sumall, sumb / sumall)


base = Image.open('input.jpg')

inputs = {}

print('scanning input image')

for filename in iglob('images/*'):
    if filename.lower().endswith('.jpg') or filename.lower().endswith('.jpeg') or filename.lower().endswith('.png'):
        img = Image.open(filename)
        resized = img.resize((50, 50))

        data = resized.getdata()
        inputs[filename] = get_average_color(data)
        resized.close()
        img.close()

width, height = base.size

main_image = Image.new('RGB', base.size)

print('scanning base image')

for h in range(height // BOX_SIZE[1]):
    for w in range(width // BOX_SIZE[0]):
        crop = base.crop((w * BOX_SIZE[0], h * BOX_SIZE[1], (w + 1) * BOX_SIZE[0], (h + 1) * BOX_SIZE[1]))
        color = get_average_color(crop.getdata())
        crop.close()

        mindiff = 255
        mindifffile = None
        for k, v in inputs.items():
            diff = sum(abs(color[i] - v[i]) for i in range(3))
            if diff < mindiff:
                mindiff = diff
                mindifffile = k

        img = Image.open(mindifffile)
        resized = img.resize(BOX_SIZE)
        main_image.paste(resized, ((w * BOX_SIZE[0]), (h * BOX_SIZE[1])))
        img.close()
        resized.close()

main_image.save('tm3p444.png')
