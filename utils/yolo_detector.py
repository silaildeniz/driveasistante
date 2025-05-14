from ultralytics import YOLO

class YOLODetector:
    def __init__(self, model_paths):
        self.models = {
            path.split("/")[-1].split(".")[0]: YOLO(path).half()  # FP16 hızlandırma
            for path in model_paths
        }

    def detect(self, frame):
        results = []
        for model_name, model in self.models.items():
            # Model ile tahmin yap
            pred = model(frame)
            for *box, conf, cls in pred.xywh[0]:
                label = model.names[int(cls)]
                confidence = float(conf)
                if confidence >= 0.4:  # Güven eşiği
                    results.append((label, tuple(map(int, box))))
        return results
