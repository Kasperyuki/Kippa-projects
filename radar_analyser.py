from PIL import Image
from datetime import datetime, timedelta

def open_image(path):
    newImage = Image.open(path)
    return newImage

# Save Image
def save_image(image, path):
    image.save(path, 'png')


# Create a new image with the given size
def create_image(i, j):
    image = Image.new("RGB", (i, j), "white")
    return image


# Get the pixel from the given image
def get_pixel(image, i, j):
    # Inside image bounds?
    width, height = image.size
    if i > width or j > height:
        return None

  # Get Pixel
    pixel = image.getpixel((i, j))
    return pixel



def rainfall(name, muoto):
    # Get size
    
    # Create new Image and a Pixel Map
    #new = create_image(width, height)
    #pixels = new.load()
    breaker = False
    name_date = name[:-4]

    #counter = 0

    attempts = 0
    rainfall = []
    #loop = True
    loops = 0
    hits = 0
    counter = 0
    next_day = datetime.strptime(name_date, "%Y%m%d%H%M") + timedelta(days=1)

    while True:
        time = datetime.strptime(name_date, "%Y%m%d%H%M")

        delta = timedelta(minutes=5)
        time = time + delta*counter
        
        time_format = f"{time.strftime('%Y%m%d%H%M')}.png"

        #if time_format == "202101041728.png":
        #    break

        #loop = True
        loops += 1
        #print(loops)
        #print(time_format)
        #if hits > 11:
        #    break
        print(next_day.day)
        print(time.day,time.hour,time.minute)
        if time.day == next_day.day:
            break

        try:   
            
            image = open_image(time_format)
            
            image = image.convert('RGB')
            pixels = image.load()
            found = True
            attempts = 0
            hits += 1
            #print(hits)

            if found:
                width, height = image.size

                if rainfall == []:
                    for i in range(width):
                        rainfall.append([])
                        for j in range(height):
                            rainfall[i].append(0)
                
                #print(len(rainfall[0]))

                # Transform to grayscale
                for i in range(width):
                    for j in range(height):
                        # Get Pixel
                        pixel = get_pixel(image, i, j)

                        # Get R, G, B values (This are int from 0 to 255)
                        red =   pixel[0]
                        green = pixel[1]
                        blue =  pixel[2]
                        color = (red,green,blue)

                        rain = False
                        snow = False

                        #8...12
                        if color == (10,155,225) or color == (40,159,212): #10,155,225  #deep blue
                            #print("löytyy")
                            dBZ = (8+12)/2
                            rain = True
                            snow = True
                        
                        #12...18
                        if color == (5,205,170) or color == (66,157,198) or color == (66,157,198):   #5,205,170  #light blue
                            #print("löytyy")
                            dBZ = (12+18)/2
                            rain = True
                            snow = True
                        
                        #18...24
                        if color == (140,230,20) or color == (147,221,57) or color == (150,219,68) or color == (148,222,41) or color == (147,223,37):  #140,230,20  #green
                            #print("löytyy")
                            dBZ = (18+24)/2
                            rain = True
                            snow = True
                        
                        #24...30
                        if color == (240,240,20) or color == (232,230,41) or color == (223,226,68) or color == (233,232,37):  #240,240,20   #yellow
                            #print("löytyy")
                            dBZ = (24+30)/2
                            rain = True
                            snow = True
                        
                        #30...34
                        if color == (255,205,20) or color == (234,201,61) or color == (234,201,43) or color == (248,151,62) or color == (244,196,48): #255,205,20 #orange
                            #print("löytyy")
                            dBZ = (30+34)/2
                            rain = True
                            snow = True
                        
                        #34...40
                        if color == (255,150,50):  #255,150,50  #dark orange
                            #print("löytyy")
                            dBZ = (34+40)/2
                            rain = True
                            snow = True
                        
                        #40...50
                        if color == (255,80,60):   #255,80,60  #red
                            #print("löytyy")
                            dBZ = (40+50)/2
                            rain = True
                            snow = True
                        
                        #> 50
                        if color == (250,120,255): #250,120,255 #purple
                            #print("löytyy")
                            dBZ = 50
                            rain = True
                            snow = True

                        #rainfall converter
                        if rain:
                            rain = 0.029185*1.16241**dBZ

                        #snowfall converter
                        if snow:
                            snow = 10**(dBZ/20)/10

                        if rain or snow:
                            # Transform to grayscale
                            #gray = (red * 0.299) + (green * 0.587) + (blue * 0.114)
                            #pixels[i, j] = (int(gray), int(gray), int(gray))
                            #adds rain to rainfall matrix
                            if muoto == "snow":
                                rainfall[i][j] += snow*(5/60)
                            else:
                                rainfall[i][j] += rain*(5/60)
                            
                            
                        #else:
                            # Set Pixel in new image
                            #pixels[i, j] = (int(red), int(green), int(blue))
                            #pass
            #print("moi")
            counter += 1
            print(time_format)
            image.close()

        except:         
            attempts += 1
            #print(attempts)
            counter += 1
            image.close()
            if attempts == 10:
                break
    print(f"{hits*5} minutes of radar imagery processed")
    print("COMPLETED!")

    new = create_image(width, height)
    pixels = new.load()

    reference = open_image("img.png")
    reference = reference.convert('RGB')
    
    #most_rain = 0
    rain_loc = []

    for i in range(width):
        for j in range(height):
            # Get Pixel
            if rainfall[i][j] != 0:
                raina = rainfall[i][j]
                rain_loc.append((raina, i, j))
                #if raina>most_rain:
                #    most_rain = raina
                #    location = (i,j)
            else:
                raina = 0
            
            pixel = get_pixel(reference, i, j)
            # Get R, G, B values (This are int from 0 to 255)
            red =   pixel[0]
            green = pixel[1]
            blue =  pixel[2]

            color = (red,green,blue)
            #light blue (222,236,254)
            #dark blue (0,0,192)

            # Set Pixel in new image
            if raina != 0:
                if raina < 2:
                    pixels[i, j] = (int(255 - raina*100), int(255 - raina*100), int(255 - raina*100))
                elif 10 > raina >= 2:
                    #pixels[i, j] = (int((raina-2)/8*255), int(255), int(0))
                    pixels[i, j] = (int(0), int(255-(raina-2)/8*220), int(0))
                elif 20 > raina >= 10:
                    pixels[i, j] = (int(255), int(255-(raina-10)/10*255), int(0))
                elif 40 > raina >= 20:
                    pixels[i, j] = (int(255), int(0), int((raina-20)/20*255))
                elif raina >= 40:
                    pixels[i, j] = (int(255-(raina-40)/80*255), int(0), int(255))
            else:
                if color == (0,0,192):
                    pixels[i, j] = (int(222), int(236), int(254))
                else:
                    pixels[i, j] = (int(red), int(green), int(blue))

    print(sorted(rain_loc, reverse=True)[1:10])
    print(f"Salo, Kärkkä: {rainfall[75][189]:.2f} mm")
    print(f"Lahti, Sopenkorpi: {rainfall[449][13]:.2f} mm ")
    print(f"Vantaa: {rainfall[340][216]:.2f} mm ")
    print(f"Espoo, Nuuksio: {rainfall[277][219]:.2f} mm ")
    print(f"Espoo, Tapiola: {rainfall[312][248]:.2f} mm ")
    print(f"Espoo, Laaksolahti: {rainfall[302][235]:.2f} mm")
    
    return new, rainfall #new, rainfall


# Main
if __name__ == "__main__":
    # Load Image (JPEG/JPG needs libjpeg to load)
    #filename = '202101072102.png'
    #filename = '202101041633.png'
    #filename = '202101100955.png'
    paiva = input("Mikä päivä (YYYYMMDDHHMM): ")
    muoto = input("Sateen muoto (snow tai muu): ")
    

    filename = f"{paiva}.png"

    #name_date = filename[:-4]
    time = datetime.strptime(paiva, "%Y%m%d%H%M")
    delta = timedelta(minutes=1)
    #time += delta
    time_format = f"{time.strftime('%Y%m%d%H%M')}.png"
    original = open_image(time_format)
    original = original.convert('RGB')

    #print(rainfall(filename))
    #try:
    #    original = open_image(filename)
    #    original = original.convert('RGB')
    #    print("ON")
    #except:
    #    print("EI")

    # Example Pixel Color
    #print('Color: ' + str(get_pixel(original, 0, 0)))
    #pixels = []
    #width, height = original.size
    #for i in range(width):
    #    for j in range(height):
    #        pixels.append(str(get_pixel(original, i, j)))

    #print(pixels)

    #print(original.getpixel((0,0)))

    # Convert to Grayscale and save
    new = rainfall(filename, muoto)[0]
    #save_image(new, 'EDITED7_1.png')
    if muoto == "snow":
        save_image(new, f"{time_format[:-8]}_PR_S.png")
    else:
        save_image(new, f"{time_format[:-8]}_PR.png")
