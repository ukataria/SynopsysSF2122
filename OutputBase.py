import pygame
import pandas
from pygame.locals import *
import sys
def main(df, clusterRoutes, times, clusters):
    pygame.init()
    SCALE = 10
    screen = pygame.display.set_mode([1000, 1000])
    screen.fill((255, 255, 255))
    colors = [(200, 0, 0), (0, 200, 0), (0, 0, 200), (0, 200, 200), (200, 200, 0), (200, 0, 200)]
    for i in range(0, clusters):
        #Draw Routes
        n = 0
        pygame.draw.line(screen, colors[i],
                         (df.iloc[clusterRoutes[i][n][0] - 1].XCord * SCALE, df.iloc[clusterRoutes[i][n][0] - 1].YCord * SCALE),
                         (df.iloc[0].XCord * SCALE, df.iloc[0].YCord * SCALE), width=7)
        for n in range(1, len(clusterRoutes[i])):
            pygame.draw.line(screen, colors[i],
                             (df.iloc[clusterRoutes[i][n-1][0] - 1].XCord * SCALE, df.iloc[clusterRoutes[i][n-1][0] - 1].YCord * SCALE),
                             (df.iloc[clusterRoutes[i][n][0] - 1].XCord * SCALE, df.iloc[clusterRoutes[i][n][0] - 1].YCord * SCALE), width=7)
    for i in range(0, clusters):
        for j in range(0, len(clusterRoutes[i])):
            n = clusterRoutes[i][j][0] - 1
            if (df.iloc[n].Customer == 1):
                pygame.draw.circle(screen, (0,0,0), (df.iloc[n].XCord * SCALE, df.iloc[n].YCord * SCALE), 20)
            else:
                pygame.draw.circle(screen, colors[i], (df.iloc[n].XCord * SCALE, df.iloc[n].YCord * SCALE), 10)
    return screen

if __name__ == "__main__":
    main()