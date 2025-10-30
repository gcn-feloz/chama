import torch
import ultralytics.nn.tasks

def setup_torch():
    """
    Configura o PyTorch para carregar modelos YOLO corretamente
    """
    try:
        # Registra as classes necessárias como seguras
        torch.serialization.add_classes_to_set([ultralytics.nn.tasks.PoseModel])
        
        # Desativa a restrição de weights_only para permitir carregar o modelo
        def load_override(*args, **kwargs):
            if 'weights_only' not in kwargs:
                kwargs['weights_only'] = False
            return torch._load_original(*args, **kwargs)
            
        if not hasattr(torch, '_load_original'):
            torch._load_original = torch.load
            torch.load = load_override
            
    except Exception as e:
        print(f"AVISO: Erro ao configurar PyTorch: {e}")
        print("O carregamento do modelo pode falhar. Tente usar uma versão mais antiga do PyTorch.")