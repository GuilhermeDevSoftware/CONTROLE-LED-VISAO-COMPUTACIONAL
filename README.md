# Controle de LED com Gestos usando ESP32 e Python

Projeto de visão computacional que permite controlar um LED conectado ao ESP32 através de gestos realizados em frente à webcam.

O reconhecimento da mão é feito em Python utilizando OpenCV e MediaPipe. Após identificar o gesto, o computador envia um comando pela comunicação serial USB para o ESP32.

## Funcionamento

O sistema reconhece dois gestos:

* Dois dedos levantados: liga o LED.
* Mão fechada: desliga o LED.

Fluxo do projeto:

```text
Webcam → Python → MediaPipe → Comunicação Serial → ESP32 → LED
```

## Tecnologias utilizadas

* Python
* OpenCV
* MediaPipe
* PySerial
* ESP32
* Arduino IDE
* Comunicação Serial USB

## Componentes

* ESP32
* Cabo USB
* LED
* Resistor de 220 Ω ou 330 Ω
* Protoboard
* Jumpers
* Computador ou notebook com webcam

## Ligação do LED

```text
GPIO 2 do ESP32 → Resistor → Perna longa do LED
Perna curta do LED → GND
```

Também pode ser utilizado o LED interno do ESP32, dependendo do modelo da placa.

## Estrutura do projeto

```text
PROJETO-5-VISAO-COMPUTACIONAL/
│
├── CODIGO-ESP32/
│   └── controle_led.ino
│
├── CODIGO-PYTHON-VISAO/
│   ├── controle_gestos.py
│   └── venv/
│
└── README.md
```

A pasta `venv` não precisa ser enviada para o GitHub.

## Instalação das bibliotecas

Crie um ambiente virtual:

```bash
python -m venv venv
```

Ative o ambiente virtual no Windows:

```bash
venv\Scripts\activate
```

Instale as bibliotecas:

```bash
python -m pip install opencv-python mediapipe==0.10.21 pyserial
```

## Configuração da porta serial

No arquivo Python, altere a porta conforme a porta utilizada pelo ESP32:

```python
PORTA_ESP32 = "COM3"
```

A porta pode ser verificada na Arduino IDE em:

```text
Ferramentas → Porta
```

## Execução

Primeiro, envie o código para o ESP32 utilizando a Arduino IDE.

Depois, feche o Monitor Serial da Arduino IDE, pois a porta serial não pode ser utilizada simultaneamente pelo Python e pela Arduino IDE.

Execute o programa Python:

```bash
python controle_gestos.py
```

A webcam será aberta e mostrará os pontos de referência detectados na mão.

## Comandos reconhecidos

```text
Dois dedos levantados → LED ligado
Mão fechada → LED desligado
```

Para encerrar o programa, pressione:

```text
Q
```

## Comunicação entre Python e ESP32

O Python envia caracteres pela porta serial:

```text
L → Liga o LED
D → Desliga o LED
```

O ESP32 recebe o comando e altera o estado do GPIO conectado ao LED.

## Possíveis erros

### Porta serial ocupada

Caso apareça uma mensagem de acesso negado à porta COM, feche:

* Monitor Serial da Arduino IDE;
* Plotter Serial;
* outros programas Python;
* qualquer programa que esteja utilizando a mesma porta.

### Webcam não abre

Altere o índice da câmera:

```python
camera = cv2.VideoCapture(1)
```

Ou utilize:

```python
camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
```

### MediaPipe sem o atributo `solutions`

Instale a versão compatível:

```bash
python -m pip uninstall mediapipe -y
python -m pip install mediapipe==0.10.21
```

## Resultado

O projeto permite controlar um dispositivo físico sem contato, utilizando apenas gestos reconhecidos pela webcam.

Ele demonstra a integração entre:

* visão computacional;
* sistemas embarcados;
* comunicação serial;
* processamento de imagens;
* hardware e software.

## Autor

Guilherme Costa

Estudante de Engenharia da Computação.
