import pygame
import pygame_advanced
import os

class APP:
    def __init__(self) -> None:
        pygame.init()
        
        self.screen = pygame_advanced.create_display((800,600))
        pygame.display.set_caption("pygame_advanced Example")

        self.clock = pygame.time.Clock()

    def run(self):
        
        rect = pygame_advanced.Rect(300,300,100,100)
        circ = pygame_advanced.Circle(100,100,50)
        poly = pygame_advanced.Polygon([(100,100), (200,200), (300,100)])
        line_multple = pygame_advanced.Line.from_points((100,100), (500,200), (300,300))

        #image = pygame_advanced.image()

        while True:
            self.screen.fill((255,255,255))
            self.clock.tick(0)
            

            
            if pygame.mouse.get_pressed()[0]:
                rect.center = pygame.mouse.get_pos()

            
            pygame.draw.rect(self.screen, (0,0,0), rect)
            circ.draw((0,0,0))
            poly.draw((0,0,0))
            line_multple.draw((250,0,0))
        

            for event in pygame.event.get():
                pygame_advanced.event(event)

                if event.type == pygame.QUIT:
                    pygame_advanced.quick_quit()   
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame_advanced.quick_quit()  
    
            pygame.display.flip()
                        
    


if __name__ == "__main__":
    os.system("cls")
    app = APP()
    app.run()
