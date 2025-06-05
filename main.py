from BinPackingEnv import BinPackingEnv
from BCPolicy import BCPolicy
import pygame
import pygame.gfxdraw
import torch
import torch.nn as nn
import random
import math
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset

pygame.init()
pygame.display.set_caption("2d Bin Circle Packing Simulation")
clock = pygame.time.Clock()
screen = pygame.display.set_mode((1560, 900))


def run_ppo():
    pass


def h_generate_data(packing_bin, num_samples = 500):
    data, state = list(), list()
    for n in range(num_samples):
        sample = BinPackingEnv(random.sample(packing_bin.circle_radii, packing_bin.num_circles))
        placed = []
        current_x, current_y = 0, 0
        max_row_height = 0

        for r in sample.circle_radii:
            print(sample.circles, sample.index)
            if current_x + 2*r > 1400:
                current_x = 0
                current_y += max_row_height
                max_row_height = 0
            x = current_x + r
            y = current_y + r

            state = (placed.copy(), r)
            action = (x, y)
            data.append((state, action))

            current_x += 2*r
            placed.append((x, y, r))
            max_row_height = max(max_row_height, 2*r)

    return data


def is_valid():
    pass


def preprocess(state, max_circles):
    placed, current_radius = state
    flat = []
    for x, y, r in placed:
        flat.extend([x, y, r])
    flat += [0] * (3 * (max_circles - len(placed)))
    flat.append(current_radius)

    return torch.tensor(flat, dtype=torch.float32)


def train_bc_model(data, max_circles, epochs=10, batch_size=64):
    input_size = 3 * max_circles + 1  # x, y, r for each circle + current radius
    model = BCPolicy(input_size)
    optimizer = optim.Adam(model.parameters(), lr=1e-3)
    loss_fn = nn.MSELoss()

    # Preprocess dataset
    X = []
    Y = []
    for state, action in data:
        X.append(preprocess(state, max_circles))
        Y.append(torch.tensor(action, dtype=torch.float32))

    dataset = TensorDataset(torch.stack(X), torch.stack(Y))
    loader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

    for epoch in range(epochs):
        total_loss = 0
        for x_batch, y_batch in loader:
            pred = model(x_batch)
            loss = loss_fn(pred, y_batch)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
        #print(f"Epoch {epoch+1}: loss = {total_loss / len(loader):.4f}")

    return model


def update_display(screen, circles, index=-1):  # regular display updater
    screen.fill((0, 0, 0))
    for x, y, r in circles[:]:
        pygame.gfxdraw.circle(screen, 75+int(x), 800-int(y), r, (255, 255, 255))

    return None


# active variables
circle_radii = [random.randint(10, 70) for i in range(60)]
packing_bin = BinPackingEnv(circle_radii)
started = False  # status of running the simulation
placed = []

# main loop
update_display(screen, placed)
running = True
while running:

    if started:
        num_circles = packing_bin.num_circles

        print("Generating expert data...")
        data = h_generate_data(packing_bin, num_samples=800)

        print("Training behavior cloning model...")
        bc_model = train_bc_model(data, num_circles, epochs=20)

        for i, r in enumerate(packing_bin.circle_radii):
            # 1. Build current state
            state = (placed.copy(), r)  # ([(x1, y1, r1), ...], current_r)

            # 2. Preprocess for the model
            x_input = preprocess(state, max_circles=packing_bin.num_circles).unsqueeze(0)  # batch size = 1

            # 3. Predict (x, y)
            with torch.no_grad():
                x, y = bc_model(x_input).squeeze().numpy()

            print(f"Predicted position for circle {i + 1} (r = {r}): ({x:.2f}, {y:.2f})")

            # 4. Store the placed circle for the next step
            placed.append((x, y, r))
        print(placed)

        started = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and not started:
            pass

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:  # quit program
                running = False

            elif event.key == pygame.K_DELETE or event.key == pygame.K_c:  # clear graph
                pass
                started = False
            
            elif (event.key == pygame.K_RETURN or event.key == pygame.K_s) and not started:  # start simulation
                started = True

            elif event.key == pygame.K_t:  # for testing
                print("test started")

    update_display(screen, placed)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()

