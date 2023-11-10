import pygame
import random

# Initialize Pygame
pygame.init()


#INSIDE OF THE GAME LOOP
# Set up the display to be full screen
screen_width, screen_height = pygame.display.Info().current_w, pygame.display.Info().current_h
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Nephew's Adventure")

bg = pygame.image.load("bg.png")
bg = pygame.transform.scale(bg, (screen_width, screen_height))


# Load images
nephew_image = pygame.image.load("nephew.png")  
nephew_rect = nephew_image.get_rect()

toilet_image = pygame.image.load("toilet.png")  
# downscale toilet image
TOILET_SCALE_FACTOR = 10
toilet_image = pygame.transform.scale(
    toilet_image,
    (
        toilet_image.get_width() // TOILET_SCALE_FACTOR,
        toilet_image.get_height() // TOILET_SCALE_FACTOR,
    ),
)

crap_image = pygame.image.load("crap.png")  
CRAP_SCALE_FACTOR = 5
crap_image = pygame.transform.scale(
    crap_image,
    (
        crap_image.get_width() // CRAP_SCALE_FACTOR,
        crap_image.get_height() // CRAP_SCALE_FACTOR,
    ),
)

pants_image = pygame.image.load("pants.png")
PANTS_SCALE_FACTOR = 1.3
pants_image = pygame.transform.scale(
    pants_image,
    (
        pants_image.get_width() // PANTS_SCALE_FACTOR,
        pants_image.get_height() // PANTS_SCALE_FACTOR,
    ),
)


# List to hold craps and toilets
craps = []
toilets = []
pants = []

for i in range(5):  # Number of toilets
    toilets.append(
        toilet_image.get_rect(midbottom=(random.randint(0, screen_width), screen_height))
    )

for i in range(5):  # Number of toilets
    pants.append(pants_image.get_rect(midbottom=(random.randint(0, screen_width), screen_height)))


# Scoring
score = 0
font = pygame.font.Font(None, 36)

screen.blit(bg, (0, 0))
# Game loop
running = True
while running:
  # Draw the background image
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            # Create a new rect for the crap at the nephew's current position
            new_crap = crap_image.get_rect(center=nephew_rect.midbottom)
            craps.append(new_crap)

    # Get keys pressed
    keys = pygame.key.get_pressed()

    # Update nephew's position based on keys pressed
    if keys[pygame.K_LEFT]:
        nephew_rect.x -= 5  # Move left
    if keys[pygame.K_RIGHT]:
        nephew_rect.x += 5  # Move right

    # Keep nephew on screen
    nephew_rect.clamp_ip(screen.get_rect())

    # Update the position of the craps and check for collisions
    for crap in craps:
        crap.y += 2  # Move the crap down
        for toilet in toilets:
            if crap.colliderect(toilet):
                score += 1
                craps.remove(crap)
                break
        for pant in pants:
            if crap.colliderect(pant):
                score -= 1
                if crap in craps:
                    craps.remove(crap)
                break

    # Scroll toilets and respawn if they go off screen
    for toilet in toilets:
        toilet.x -= 2
        if toilet.right < 0:
            toilet.x = screen_width

    # Scroll pants and respawn if they go off screen
    for pant in pants:
        pant.x += 2
        if pant.left > screen_width:
            pant.x = 0

    screen.blit(bg, (0, 0))

    # Draw the toilets
    for toilet in toilets:
        screen.blit(toilet_image, toilet)

    # Draw the pants
    for pant in pants:
        screen.blit(pants_image, pant)

    # Draw the craps
    for crap in craps:
        screen.blit(crap_image, crap)

    # Draw the nephew at the new position
    screen.blit(nephew_image, nephew_rect)

    # Draw the score
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate to 60 frames per second
    pygame.time.Clock().tick(60)

pygame.quit()
