from ultralytics import YOLO
import os
import torch

class YOLODetector:
    def __init__(self, model_paths):

        self.models = {}
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        print(f" YOLO modelleri {self.device} üzerinde çalışacak")
        self.load_models(model_paths)
    
    def load_models(self, model_paths):
        """Modelleri yükle"""
        for name, path in model_paths.items():
            try:
                if os.path.exists(path):
                    model = YOLO(path)
                    model.to(self.device)  # Modeli GPU'ya taşı
                    self.models[name] = model
                    print(f" {name} modeli yüklendi ({self.device})")
                else:
                    print(f" {name} modeli bulunamadı: {path}")
            except Exception as e:
                print(f" {name} modeli yüklenemedi: {str(e)}")
    
    def detect(self, frame, confidence_threshold=0.5):
        """
        Görüntüde nesne tespiti yap
        
        Args:
            frame: İşlenecek görüntü
            confidence_threshold: Güven eşiği
            
        Returns:
            list: [(model_name, label, confidence, box), ...]
        """
        detections = []
        
        for model_name, model in self.models.items():
            try:
                results = model(frame, verbose=False)[0]  # verbose=False ile gereksiz çıktıları kapat
                for box in results.boxes:
                    confidence = float(box.conf[0])
                    if confidence >= confidence_threshold:
                        cls_id = int(box.cls[0])
                        label = model.names[cls_id]
                        x1, y1, x2, y2 = map(int, box.xyxy[0])
                        detections.append((model_name, label, confidence, (x1, y1, x2, y2)))
            except Exception as e:
                print(f" {model_name} modeli tespit hatası: {str(e)}")
                continue
        
        return detections
