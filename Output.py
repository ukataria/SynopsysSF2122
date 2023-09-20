import pygame
import pandas
from pygame.locals import *
from pygame import *
import sys

def main(df, clusterRoutes, times, clusters):
    pygame.init()
    SCALE = 10

    font = pygame.font.Font(pygame.font.get_default_font(), int(SCALE * (1.45)))
    screen = pygame.display.set_mode([SCALE*100, SCALE*90])
    screen.fill((255, 255, 255))
    colors = [(200, 0, 0), (0, 200, 0), (0, 0, 200), (0, 200, 200), (200, 200, 0), (200, 0, 200)]
    for i in range(0, clusters):
        #Draw Routes
        n = 0
        pygame.draw.line(screen, colors[i],
                         (df.iloc[clusterRoutes[i][n][0] - 1].XCord * SCALE + 2*SCALE, df.iloc[clusterRoutes[i][n][0] - 1].YCord * SCALE + 2*SCALE),
                         (df.iloc[0].XCord * SCALE + 2*SCALE, df.iloc[0].YCord * SCALE + 2*SCALE), width=int(SCALE/3))
        for n in range(1, len(clusterRoutes[i])):
            pygame.draw.line(screen, colors[i],
                             (df.iloc[clusterRoutes[i][n-1][0] - 1].XCord * SCALE + 2*SCALE, df.iloc[clusterRoutes[i][n-1][0] - 1].YCord * SCALE + 2*SCALE),
                             (df.iloc[clusterRoutes[i][n][0] - 1].XCord * SCALE + 2*SCALE, df.iloc[clusterRoutes[i][n][0] - 1].YCord * SCALE + 2*SCALE), width=int(SCALE/3))
    for i in range(0, clusters):
        #Draw Nodes
        cluster = df[df.cluster == i]

        for n in range(0, len(clusterRoutes[i])):
            if (df.iloc[clusterRoutes[i][n][0] - 1].XCord == 40 and df.iloc[clusterRoutes[i][n][0] - 1].YCord == 50):
                pygame.draw.circle(screen, (0,0,0), (df.iloc[clusterRoutes[i][n][0] - 1].XCord * SCALE + 2*SCALE, df.iloc[clusterRoutes[i][n][0] - 1].YCord * SCALE + 2*SCALE), int(SCALE*3), int(SCALE/2))
                pygame.draw.circle(screen, (255,255,255), (df.iloc[clusterRoutes[i][n][0] - 1].XCord * SCALE + 2*SCALE, df.iloc[clusterRoutes[i][n][0] - 1].YCord * SCALE + 2*SCALE), int(SCALE*2.5))
            else:
                pygame.draw.circle(screen, colors[i], (df.iloc[clusterRoutes[i][n][0] - 1].XCord * SCALE + 2*SCALE, df.iloc[clusterRoutes[i][n][0] - 1].YCord * SCALE + 2*SCALE), SCALE*1.75, int(SCALE/2))
                pygame.draw.circle(screen, (255,255,255), (df.iloc[clusterRoutes[i][n][0] - 1].XCord * SCALE + 2*SCALE, df.iloc[clusterRoutes[i][n][0] - 1].YCord * SCALE + 2*SCALE), SCALE*1.5)
                text = font.render(str(n + 1), True, (0,0,0), (255,255,255))
                textRect = text.get_rect()
                textRect.center = (df.iloc[clusterRoutes[i][n][0] - 1].XCord * SCALE + 2*SCALE, df.iloc[clusterRoutes[i][n][0] - 1].YCord * SCALE + 2*SCALE)
                screen.blit(text, textRect)
    pygame.image.save(screen, "ImprovedOutput/" + "RC101" + ".png")
    # while True:
    #     for event in pygame.event.get():
    #         if event.type == QUIT:
    #             running = False
    #     pygame.display.update()
    return screen

if __name__ == "__main__":
    main()