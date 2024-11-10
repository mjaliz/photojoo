from loguru import logger
import torch
from transformers import CLIPProcessor, CLIPModel, CLIPTokenizer


class CLIP:
    def __init__(self):
        self._device = "cuda" if torch.cuda.is_available() else "cpu"
        # self._device = "cpu"
        logger.info(f"device :{self._device}")
        self._model_id = "openai/clip-vit-base-patch32"
        self._model = CLIPModel.from_pretrained(self._model_id).to(self._device)
        self._processor = CLIPProcessor.from_pretrained(self._model_id)
        self._tokenizer = CLIPTokenizer.from_pretrained(self._model_id)

    def text_embedding(self, text: str) -> list[float]:
        inputs = self._tokenizer(text, return_tensors="pt").to(self._device)
        text_embeddings = self._model.get_text_features(**inputs)
        return text_embeddings.cpu().detach().numpy().tolist()[0]

    def image_embedding(self, img) -> list[float]:
        image = self._processor(text=None, images=img, return_tensors="pt")[
            "pixel_values"
        ].to(self._device)
        embedding = self._model.get_image_features(image)
        return embedding.cpu().detach().numpy().tolist()[0]
