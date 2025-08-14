import torch
import torch.nn as nn

# Dummy PyTorch model (replace with your own later)
class SimpleModel(nn.Module):
    def __init__(self):
        super(SimpleModel, self).__init__()
        self.linear = nn.Linear(4, 1)

    def forward(self, x):
        return self.linear(x)

# Initialize model
model = SimpleModel()

def predict(data):
    # Convert input to tensor
    tensor = torch.tensor([data], dtype=torch.float32)
    # Forward pass
    output = model(tensor)
    return output.item()
