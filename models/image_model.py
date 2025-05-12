import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image
import os

class MedicalImageAnalyzer:
    """
    System for analyzing medical images using transfer learning with a pre-trained model.
    """
    def __init__(
        self,
        num_classes: int = 2,
        model_name: str = "densenet121",
        pretrained: bool = True,
        device: str = None
    ):
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")

        if model_name == "densenet121":
            self.model = models.densenet121(pretrained=pretrained)
            in_features = self.model.classifier.in_features
            self.model.classifier = nn.Linear(in_features, num_classes)
        elif model_name == "resnet50":
            self.model = models.resnet50(pretrained=pretrained)
            in_features = self.model.fc.in_features
            self.model.fc = nn.Linear(in_features, num_classes)
        else:
            raise ValueError(f"Model {model_name} not supported")

        self.model = self.model.to(self.device)
        self.model.eval()

        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.Grayscale(num_output_channels=3),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                 std=[0.229, 0.224, 0.225])
        ])

    def analyze_image(self, image_path: str) -> dict:
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"File not found: {image_path}")

        img = Image.open(image_path).convert("RGB")
        x = self.transform(img).unsqueeze(0).to(self.device)

        with torch.no_grad():
            logits = self.model(x)
            probs = torch.softmax(logits, dim=1).cpu().numpy()[0]
            pred = int(probs.argmax())

        return {
            "prediction": pred,
            "probabilities": probs.tolist()
        }

    def load_checkpoint(self, checkpoint_path: str):
        if not os.path.exists(checkpoint_path):
            raise FileNotFoundError(f"Checkpoint not found: {checkpoint_path}")
        state = torch.load(checkpoint_path, map_location=self.device)
        self.model.load_state_dict(state)

    def save_checkpoint(self, checkpoint_path: str):
        torch.save(self.model.state_dict(), checkpoint_path)