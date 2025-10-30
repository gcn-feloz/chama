import cv2
from stream_capture import StreamCapture

def main():
    # Inicializa a captura
    stream = StreamCapture()
    
    try:
        while True:
            # Captura frame
            frame = stream.get_frame()
            
            if frame is None:
                print("Erro ao capturar frame")
                break
            
            # Mostra o frame
            cv2.imshow('Test Stream', frame)
            
            # Espera por tecla 'q' para sair
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
    finally:
        # Limpa recursos
        stream.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()