# pygame_advanced

A high-level wrapper for Pygame designed to streamline game development by providing automatic element scaling, simplified syntax, and enhanced boilerplate management.

## 🚀 Features

- **Auto-Scaling Displays**: Create responsive windows where elements scale automatically.
- **Simplified Shapes**: Object-oriented approach to drawing shapes (`Rect`, `Circle`, `Polygon`, `Line`).
- **Shorter Commands**: Reduced boilerplate for display initialization and event handling.
- **Quick Quit**: Integrated event handling to exit applications gracefully with fewer lines of code.

## 🛠 Installation

Ensure you have Pygame installed:

```bash
pip install pygame
```

*(Note: Once published, users can install your library via pip)*

## 💻 Quick Start

Here is a basic example of how to use `pygame_advanced`:

```python
import pygame
import pygame_advanced

class APP:
    def __init__(self) -> None:
        pygame.init()
        # Simplified display creation
        self.screen = pygame_advanced.create_display((800, 600))
        self.clock = pygame.time.Clock()

    def run(self):
        # High-level shape objects
        rect = pygame_advanced.Rect(300, 300, 100, 100)
        
        while True:
            self.screen.fill((255, 255, 255))
            
            # Draw directly from the object
            rect.draw((0, 0, 0))

            for event in pygame.event.get():
                pygame_advanced.event(event) # Handle internal scaling events
                if event.type == pygame.QUIT:
                    pygame_advanced.quick_quit()
            
            pygame.display.flip()
            self.clock.tick(60)
```

## 📄 License
MIT