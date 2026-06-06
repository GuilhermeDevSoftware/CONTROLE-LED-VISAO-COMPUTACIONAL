import time

import cv2
import mediapipe as mp
import serial


# ==================================================
# CONFIGURAÇÕES
# ==================================================

PORTA_ESP32 = "COM3"
VELOCIDADE_SERIAL = 115200

# Quantidade de quadros consecutivos necessária
# para confirmar um gesto.
QUADROS_CONFIRMACAO = 5


# ==================================================
# COMUNICAÇÃO COM O ESP32
# ==================================================

try:
    esp32 = serial.Serial(
        port=PORTA_ESP32,
        baudrate=VELOCIDADE_SERIAL,
        timeout=1
    )

    # O ESP32 pode reiniciar quando a porta serial é aberta.
    time.sleep(2)

    print(f"ESP32 conectado na porta {PORTA_ESP32}")

except serial.SerialException as erro:
    print("Não foi possível conectar ao ESP32.")
    print(erro)
    raise SystemExit


# ==================================================
# MEDIAPIPE
# ==================================================

mp_maos = mp.solutions.hands
mp_desenho = mp.solutions.drawing_utils

detector_maos = mp_maos.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)


# ==================================================
# FUNÇÕES
# ==================================================

def verificar_dedos(pontos):
    """
    Retorna o estado dos quatro dedos principais.

    True  = dedo levantado
    False = dedo abaixado

    O polegar não é utilizado porque sua posição depende
    da mão detectada e da orientação da palma.
    """

    dedos = {
        "indicador": pontos[8].y < pontos[6].y,
        "medio": pontos[12].y < pontos[10].y,
        "anelar": pontos[16].y < pontos[14].y,
        "mindinho": pontos[20].y < pontos[18].y
    }

    return dedos


def identificar_gesto(dedos):
    """
    Identifica apenas os dois gestos necessários.
    """

    dois_dedos = (
        dedos["indicador"]
        and dedos["medio"]
        and not dedos["anelar"]
        and not dedos["mindinho"]
    )

    mao_fechada = not any(dedos.values())

    if dois_dedos:
        return "LIGAR"

    if mao_fechada:
        return "DESLIGAR"

    return "NEUTRO"


def enviar_comando(comando):
    """
    Envia um caractere ao ESP32.
    """

    if comando == "LIGAR":
        esp32.write(b"L")
        print("Comando enviado: ligar LED")

    elif comando == "DESLIGAR":
        esp32.write(b"D")
        print("Comando enviado: desligar LED")


# ==================================================
# CÂMERA
# ==================================================

camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("Não foi possível abrir a webcam.")
    esp32.close()
    raise SystemExit


ultimo_comando = None
gesto_anterior = "NEUTRO"
contador_gesto = 0


try:
    while True:
        sucesso, frame = camera.read()

        if not sucesso:
            print("Não foi possível capturar a imagem.")
            break

        # Espelha a imagem para funcionar como um espelho.
        frame = cv2.flip(frame, 1)

        # O OpenCV utiliza BGR e o MediaPipe utiliza RGB.
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        resultado = detector_maos.process(frame_rgb)

        gesto_atual = "NEUTRO"

        if resultado.multi_hand_landmarks:
            mao = resultado.multi_hand_landmarks[0]

            mp_desenho.draw_landmarks(
                frame,
                mao,
                mp_maos.HAND_CONNECTIONS
            )

            dedos = verificar_dedos(mao.landmark)
            gesto_atual = identificar_gesto(dedos)

        # Confirma se o gesto permaneceu por vários quadros.
        if gesto_atual == gesto_anterior and gesto_atual != "NEUTRO":
            contador_gesto += 1
        else:
            contador_gesto = 0
            gesto_anterior = gesto_atual

        # Só envia quando o gesto estiver estável e representar
        # uma mudança no estado anterior.
        if contador_gesto >= QUADROS_CONFIRMACAO:
            if gesto_atual != ultimo_comando:
                enviar_comando(gesto_atual)
                ultimo_comando = gesto_atual

            contador_gesto = 0

        # Texto mostrado na tela.
        if gesto_atual == "LIGAR":
            texto = "DOIS DEDOS - LIGAR LED"

        elif gesto_atual == "DESLIGAR":
            texto = "MAO FECHADA - DESLIGAR LED"

        else:
            texto = "GESTO NEUTRO"

        cv2.putText(
            frame,
            texto,
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )

        cv2.putText(
            frame,
            "Pressione Q para sair",
            (20, frame.shape[0] - 20),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            2
        )

        cv2.imshow("Controle do ESP32 por gestos", frame)

        tecla = cv2.waitKey(1) & 0xFF

        if tecla == ord("q"):
            break

finally:
    camera.release()
    cv2.destroyAllWindows()
    detector_maos.close()
    esp32.close()

    print("Programa encerrado.")