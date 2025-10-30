# CHAMA - Captura e Detecção de Objetos em Streams de Vídeo

![CHAMA]

## Descrição

O **CHAMA** é um projeto Python voltado para captura e análise de streams de vídeo ao vivo (YouTube, HLS, etc.).
Ele combina **extração de vídeo com yt-dlp** e **detecção de objetos em tempo real** utilizando **YOLOv8** e **OpenCV**.

O objetivo do projeto é fornecer uma **pipeline completa**, desde a captura do stream até a detecção e classificação de objetos, permitindo análises automatizadas e integração com projetos de visão computacional.

Para atuar em bares e restaurantes, para auxiliar garçons e atendentes, a identificar e sinalizar a urgencia para meses que o cliente está precisando de atendimento ao levantar o braço.

---

## Funcionalidades

* Captura de streams de vídeo ao vivo via URL (YouTube ou HLS).
* Suporte a múltiplos formatos e resoluções.
* Detecção de objetos em tempo real usando **YOLOv8**.
* Interface simples com OpenCV para visualização dos frames.
* Configuração de pastas e ambiente isolado com `venv`.
* Logging e debug das etapas de captura e detecção.
* Estrutura modular: `stream_capture.py` e `detection.py` podem ser usados de forma independente.

---

## Pré-requisitos

* Python 3.10 ou superior
* Pip atualizado (`pip install --upgrade pip`)
* ffmpeg instalado no sistema
* Git

**Bibliotecas Python necessárias** (instaladas via `requirements.txt`):

* torch
* torchvision
* opencv-python
* ultralytics
* numpy
* Pillow
* polars
* psutil
* requests
* scipy

---

## Estrutura de Pastas

```text
chama/
├── venv/                  # Ambiente virtual
├── src/
│   ├── stream_capture.py  # Captura de stream
│   └── detection.py       # Detecção de objetos
├── requirements.txt       # Dependências Python
├── README.md
└── .gitignore
```

---

## Instalação

1. Clone o repositório:

```bash
git clone https://github.com/gcn-feloz/chama.git
cd chama
```

2. Crie o ambiente virtual:

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
# ou
venv\Scripts\activate     # Windows
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

4. Certifique-se de que `ffmpeg` está instalado no sistema:

```bash
ffmpeg -version
```

---

## Uso

### Captura de Stream

```bash
python src/stream_capture.py
```

* O script solicita uma URL de stream (YouTube, HLS, etc.).
* Pressione `q` para encerrar a captura.
* Os frames do vídeo são exibidos em uma janela do OpenCV.

### Detecção de Objetos

```bash
python src/detection.py
```

* Realiza detecção de objetos usando YOLOv8.
* Mostra os frames com bounding boxes em tempo real.
* Pressione `q` para encerrar a detecção.

**Nota:** O `detection.py` pode ser executado **independentemente** do `stream_capture.py`, desde que a URL do stream esteja correta.

---

## Configurações Avançadas

* Para alterar parâmetros de execução (resolução, FPS, modelos YOLO), edite diretamente as variáveis em `detection.py`.
* Os arquivos de configuração do YOLOv8 podem ser visualizados em:

```bash
~/.config/Ultralytics/settings.json
```

---

## Git & Versionamento

* O ambiente virtual `venv/` está no `.gitignore`.
* Para push via HTTPS no GitHub, use **Personal Access Token (PAT)** como senha.
* Alternativamente, é recomendado configurar **SSH keys** para autenticação sem senha.

---

## Contribuição

1. Faça fork do repositório.
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`).
3. Commit suas alterações (`git commit -m "Descrição da mudança"`).
4. Push para sua branch (`git push origin feature/nova-feature`).
5. Abra um Pull Request no repositório principal.

---

## Licença

 2025 [gcn-feloz]© (https://github.com/gcn-feloz)

---

## Contato

* GitHub: [https://github.com/gcn-feloz](https://github.com/gcn-feloz)
