try:
        import os
        import pygame

except ImportError, err:
        print "Module not found: %s" % (err)
        sys.exit(2)

#Why can't I use this in one script? Shouldn't have to copy so many times
def load_png(name):
    """ Load image and return image object"""
    fullname = os.path.join('data', name)
    try:
            image = pygame.image.load(fullname)
            if image.get_alpha() is None:
                    image = image.convert()
            else:
                    image = image.convert_alpha()
    except pygame.error, message:
             print 'Cannot load image:', fullname
    return image, image.get_rect()            