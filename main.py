import pygame
import random  # Añadir import random


pygame.init()


# crear pantalla
pantalla = pygame.display.set_mode((1000, 600))


# Titulo arriba de la ventana
pygame.display.set_caption("Tic Tac Toe con IA")


fondo = pygame.image.load('fondo_rayas.jpg')
equis = pygame.image.load('x.PNG')
circulo = pygame.image.load('o.PNG')
fuente = pygame.font.SysFont("Broadway", 30)
salir = pygame.image.load('salir.PNG')
reiniciar = pygame.image.load('reiniciar.PNG')
facil_medio_dificil = pygame.image.load('facil_medio_dificil.PNG')
pantalla_actual = "menu"  # posibles variables: menu, jugando, elegir_turno


# declarar los tamaños de las fotos
circulo = pygame.transform.scale(circulo, (125, 125))
equis = pygame.transform.scale(equis, (125, 125))


# matriz para el juego
coordenadas = [[(50, 50), (245, 50), (440, 50)],
              [(50, 240), (245, 240), (440, 240)],
              [(50, 430), (245, 430), (440, 430)]]


# tablero se almacenan las jugadas
tablero = [['', '', ''],
          ['', '', ''],
          ['', '', '']]


# turno actual
turno = 'X'  # siempre el usuario (la X) inicia
juego_terminado = False  # el juego aun no termina
ganador = None
reloj = pygame.time.Clock()  # frames por segundo que trabaja el juego


# Variables para la IA
dificultad_actual = None
jugador_humano = 'X'  # Por defecto
jugador_ia = 'O'  # Por defecto
limite_profundidad_arbol = None
#es_facil = False

# ============ ALGORITMO MINIMAX PARA IA ============

def evaluar_linea(contenido, jugador_ia, jugador_humano):
    #contar cuantas fichas tiene la ia en una línea
    fichas_ia = contenido.count(jugador_ia)
    #contar cuantas fichas tiene el humano en una línea
    fichas_humano = contenido.count(jugador_humano)

    #Descartar las lineas que ya tienen jugada de la ia y humano
    if fichas_ia > 0 and fichas_humano > 0:
        return 0

    #Asignar puntos(heuristica)
    puntos = 0
    if fichas_ia == 3:
        puntos += 3
    elif fichas_ia == 2:
        puntos += random.choice([-4,0,1])
    elif fichas_ia == 1:
        puntos += 0.2

    if fichas_humano == 3:
        puntos -= 3
    elif fichas_humano == 2:
        puntos -= random.choice([0,0.5])
    elif fichas_humano == 1:
        puntos -= 0
    return puntos
"""
    if es_facil == False:
        if fichas_ia == 3:
            puntos += 20
        elif fichas_ia == 2:
            puntos += random.choice([-1, 0, 8, 15])
        elif fichas_ia == 1:
            puntos += 5

        if fichas_humano == 3:
            puntos -= 20
        elif fichas_humano == 2:
            puntos -= random.choice([-1, 0, 8, 15])
        elif fichas_humano == 1:
            puntos -= 1
    return puntos
"""

def evaluar_heuristica_tablero(tablero_temp):
    #corazon de la heuristica
    #si pone un movimiento en una casilla, evalua el tablero con los puntajes de evaluar línea
    puntaje_total = 0

    #lista para almacenar los puntajes de las 8 líneas
    lineas_posibles = []

    #3filas
    for i in range(3):
        lineas_posibles.append([tablero_temp[i][0], tablero_temp[i][1], tablero_temp[i][2]])
    #3columnas
    for j in range(3):
        lineas_posibles.append([tablero_temp[0][j], tablero_temp[1][j], tablero_temp[2][j]])
    #2diagonales
    lineas_posibles.append([tablero_temp[0][0], tablero_temp[1][1], tablero_temp[2][2]])
    lineas_posibles.append([tablero_temp[0][2], tablero_temp[1][1], tablero_temp[2][0]])

    #cada linea se manda a evaluar_linea y obtener puntaje
    for linea in lineas_posibles:
        puntaje_total += evaluar_linea(linea, jugador_ia, jugador_humano)

    return puntaje_total

def ejecutar_movimiento_heuristico():
    #prueba tooodas las posibles jugadas de la ia
    #evalua cada tablero resultante
    mejor_puntaje = -float('inf')
    mejores_movimientos = []

    # verificar si el tablero está vacío
    tablero_vacio = True
    for fila in tablero:
        for celda in fila:
            if celda != '':
                tablero_vacio = False

    # iniar random si esta vacio
    if tablero_vacio:
        i = random.randint(0, 2)
        j = random.randint(0, 2)
        tablero[i][j] = jugador_ia
        return

        # recorrer el tablero y buscar espacios vacio
    for i in range(3):
        for j in range(3):
            if tablero[i][j] == '':
                #pone una ficha en el tablero
                tablero[i][j] = jugador_ia
                #calcula el tablero resultante de esa jugada
                puntaje = minimax(tablero, 0, False)        #la quita para probar otra
                #quitar la jugada
                tablero[i][j] = ''
                #Guarda las mejores jugadas
                if puntaje > mejor_puntaje:
                    mejor_puntaje = puntaje
                    mejores_movimientos = [(i, j)]
                elif puntaje == mejor_puntaje:
                    mejores_movimientos.append((i, j))

    #Elegir random los mejores movimientos
    if mejores_movimientos:
        movimiento = random.choice(mejores_movimientos)
        tablero[movimiento[0]][movimiento[1]] = jugador_ia

def minimax(tablero_actual, profundidad_actual_del_arbol, turno_ia):
   global limite_profundidad_arbol
   if (limite_profundidad_arbol is not None and profundidad_actual_del_arbol >= limite_profundidad_arbol):
        return evaluar_heuristica_tablero(tablero_actual)
   # Verificar estado del juego
   resultado = verificar_ganador_minimax(tablero_actual)
   if resultado is not None:
       if resultado == jugador_ia:  # ia gana
           """
           el 10 es el nivel que hace ganar a la ia
           se resta 10 - profundidad actual del arbol y asi obtenemos en que nivel ganó
           """
           return 10 - profundidad_actual_del_arbol
       elif resultado == jugador_humano:  # humano gana (no ocurre)
           # como es lo peor que podria pasar, se arroja un resultado negativo
           return profundidad_actual_del_arbol - 10
       elif resultado == 'empate':  # Empate
           """
           alcanzamos el nivel 10 de profundidad sin ganadores
           es 10 porque se considero el tablero vacio como 0
           y la profundidad 1 es la 1ra jugada
           """
           return 0

   if turno_ia:
       # TURNO DE LA IA  (Maximizar puntaje)
       mejor_puntaje = -float('inf')  # es infinito para garantizar que la jugada de la ia sea la mejor
       for i in range(3):
           for j in range(3):
               # busca un espacio que este vacio para hacer su jugada
               if tablero_actual[i][j] == '':
                   tablero_actual[i][j] = jugador_ia  # guarda la jugada temporalmente para ver si es la chida
                   # cada que se baja un nivel, se le suma 1 a la profundidad
                   # RECURSIVIDAD asi recorre cada nivel
                   puntaje = minimax(tablero_actual, profundidad_actual_del_arbol + 1, False )
                   # vuelve el tablero a su estado original, para despues probar otra casilla
                   tablero_actual[i][j] = ''
                   # se guarda la casilla que tiene mejor puntaje
                   mejor_puntaje = max(puntaje, mejor_puntaje)
       return mejor_puntaje
   else:
       # TURNO DEL HUMANO (Minimizar puntaje)
       mejor_puntaje = float('inf')
       for i in range(3):
           for j in range(3):
               if tablero_actual[i][j] == '':
                   tablero_actual[i][j] = jugador_humano
                   puntaje = minimax(tablero_actual, profundidad_actual_del_arbol + 1, True)
                   tablero_actual[i][j] = ''
                   mejor_puntaje = min(puntaje, mejor_puntaje)
       return mejor_puntaje

def mejor_movimiento_facil():
    global limite_profundidad_arbol
    limite_profundidad_arbol = 3
    #es_facil = True

    ejecutar_movimiento_heuristico()

def mejor_movimiento_medio():
    global limite_profundidad_arbol
    limite_profundidad_arbol = 5
    #es_facil = False

    ejecutar_movimiento_heuristico()

def mejor_movimiento_dificil():
    global limite_profundidad_arbol
    limite_profundidad_arbol = None
    #es_facil = False

    ejecutar_movimiento_heuristico()

def verificar_ganador_minimax(tablero_actual):
   # posibles retornos: X, O, empate, None (juego continúa)

   # Verificar filas
   for i in range(3):
       if tablero_actual[i][0] == tablero_actual[i][1] == tablero_actual[i][2] != '':
           return tablero_actual[i][0]

   # Verificar columnas
   for i in range(3):
       if tablero_actual[0][i] == tablero_actual[1][i] == tablero_actual[2][i] != '':
           return tablero_actual[0][i]

   # Verificar diagonales
   if tablero_actual[0][0] == tablero_actual[1][1] == tablero_actual[2][2] != '':
       return tablero_actual[0][0]
   if tablero_actual[0][2] == tablero_actual[1][1] == tablero_actual[2][0] != '':
       return tablero_actual[0][2]

   # Verificar empate
   for i in range(3):
       for j in range(3):
           if tablero_actual[i][j] == '':
               return None  # Todavía hay movimientos

   return 'empate'  # Empate

def ia_juega():
   if (dificultad_actual == 'facil'):
       mejor_movimiento_facil()
   elif (dificultad_actual == 'medio'):
       mejor_movimiento_medio()
   elif (dificultad_actual == 'dificil'):
       mejor_movimiento_dificil()

   # Verificar si la IA
   fin_juego = verificar_ganador()
   if fin_juego:
       global juego_terminado, ganador
       juego_terminado = True
       ganador = jugador_ia
       return True

   # Verificar empate
   empate = verificar_empate()
   if empate:
       juego_terminado = True
       ganador = 'empate'
       return True

   return False

# ============FUNCIONES QUE NO TIENEN QUE VER CON IA============

def pantalla_menu():
   pantalla.fill((0, 0, 0))
   pantalla.blit(facil_medio_dificil, (300, 100))

def pantalla_elegir_turno():
   pantalla.fill((0, 0, 0))
   # frase "¿Qué turno eliges?"
   txtTurno = fuente.render("¿Qué turno eliges?", True, (255, 255, 255))
   pantalla.blit(txtTurno, (350, 200))


   # imagen de X
   pantalla.blit(equis, (350, 300))


   # imagen de O
   pantalla.blit(circulo, (525, 300))

def graficar_tablero():
   pantalla.fill((0, 0, 0))
   pantalla.blit(fondo, (0, 0))
   # for anidado
   for fila in range(3):
       for columna in range(3):
           # logica de verificación de elementos
           if tablero[fila][columna] == 'X':
               dibujar_x(fila, columna)
           elif tablero[fila][columna] == 'O':
               dibujar_o(fila, columna)

def dibujar_x(fila, columna):
   pantalla.blit(equis, coordenadas[fila][columna])

def dibujar_o(fila, columna):
   pantalla.blit(circulo, coordenadas[fila][columna])

def verificar_ganador():
   # se necesitan 3 jugadas para verificar un ganador
   for i in range(3):
       # verifica si alguien ganó horizontal y verticalmente
       if tablero[i][0] == tablero[i][1] == tablero[i][2] != '':
           return True
       if tablero[0][i] == tablero[1][i] == tablero[2][i] != '':
           return True
   # verifica si alguien ganó diagonalmente
   if tablero[0][0] == tablero[1][1] == tablero[2][2] != '':
       return True
   if tablero[0][2] == tablero[1][1] == tablero[2][0] != '':
       return True


   return False

def verificar_empate():
   # verifica si todas las casillas están llenas y no hay ganador
   for fila in range(3):
       for columna in range(3):
           if tablero[fila][columna] == '':
               return False  # todavía hay casillas vacías
   return True  # todas las casillas están llenas

def pantalla_ganador_sinclick():
   txtEl_jugador = fuente.render("El jugador:", True, (255, 255, 255))
   txtEs_el_ganador = fuente.render("es el ganador", True, (255, 255, 255))

   if (ganador == 'X'):
       pantalla.blit(equis, (750, 150))
   else:
       pantalla.blit(circulo, (750, 150))

   pantalla.blit(txtEl_jugador, (720, 100))
   pantalla.blit(txtEs_el_ganador, (705, 300))
   pantalla.blit(salir, (650, 400))
   pantalla.blit(reiniciar, (850, 400))

def pantalla_empate_sinclick():
   txtEmpate = fuente.render("¡Empate!", True, (255, 255, 255))
   txtNadie_gano = fuente.render("Nadie ganó", True, (255, 255, 255))


   pantalla.blit(txtEmpate, (735, 100))
   pantalla.blit(txtNadie_gano, (720, 200))
   pantalla.blit(salir, (650, 400))
   pantalla.blit(reiniciar, (850, 400))

def pantalla_ganador_conclick(mouseX, mouseY):
   global tablero, turno, juego_terminado, ganador, pantalla_actual


   # boton de salir
   if ((mouseX >= 650 and mouseX <= 775) and (mouseY >= 400 and mouseY <= 525)):
       pantalla_actual = 'menu'
       tablero = [['', '', ''],
                  ['', '', ''],
                  ['', '', '']]
       turno = 'X'
       juego_terminado = False
       ganador = None


   # boton de reiniciar
   if ((mouseX >= 850 and mouseX <= 975) and (mouseY >= 400 and mouseY <= 525)):
       tablero = [['', '', ''],
                  ['', '', ''],
                  ['', '', '']]
       turno = 'X'
       juego_terminado = False
       ganador = None


       # si el jugador es 'O', la IA debe jugar primero
       if jugador_humano == 'O':
           ia_juega()
           turno = 'O'  # Ahora le toca al jugador

def procesar_click_menu(mouseX, mouseY):
   global pantalla_actual, dificultad_actual, limite_profundidad_arbol, es_facil
   # ==============JUGAR EN MODO FÁCIL==============
   if (mouseX >= 352 and mouseX <= 645) and (mouseY >= 110 and mouseY <= 230):
       dificultad_actual = 'facil'
       #es_facil = True
       limite_profundidad_arbol = 3
       pantalla_actual = 'elegir_turno'
   # ==============JUGAR EN MODO MEDIO==============
   if (mouseX >= 352 and mouseX <= 645) and (mouseY >= 238 and mouseY <= 358):
       dificultad_actual = 'medio'
       #es_facil = False
       limite_profundidad_arbol = 3
       pantalla_actual = 'elegir_turno'
   # ==============JUGAR EN MODO DIFICIL==============
   if (mouseX >= 352 and mouseX <= 645) and (mouseY >= 366 and mouseY <= 486):
       dificultad_actual = 'dificil'
       #es_facil = False
       limite_profundidad_arbol = None
       pantalla_actual = 'elegir_turno'

def procesar_click_elegir_turno(mouseX, mouseY):
   global pantalla_actual, turno, jugador_humano, jugador_ia


   # Si el jugador elige X (empieza el jugador)
   if ((mouseX >= 350 and mouseX <= 475) and (mouseY >= 300 and mouseY <= 425)):
       jugador_humano = 'X'
       jugador_ia = 'O'
       turno = 'X'  # Jugador empieza
       pantalla_actual = 'jugando'
       reiniciar_juego()


   # Si el jugador elige O (empieza la IA)
   if ((mouseX >= 525 and mouseX <= 650) and (mouseY >= 300 and mouseY <= 425)):
       jugador_humano = 'O'
       jugador_ia = 'X'
       turno = 'X'  # La IA empieza (pero con 'X')
       pantalla_actual = 'jugando'
       reiniciar_juego()
       # La IA juega primero
       ia_juega()
       turno = 'O'  # Ahora le toca al jugador

def reiniciar_juego():
   global tablero, juego_terminado, ganador
   tablero = [['', '', ''],
              ['', '', ''],
              ['', '', '']]
   juego_terminado = False
   ganador = None

# =================bucle del juego===================
mostrar_pantalla = True
while mostrar_pantalla:
   reloj.tick(30)
   for evento in pygame.event.get():

       # ===================cerrar la ventana cuando le damos cerrar===================
       if evento.type == pygame.QUIT:
           mostrar_pantalla = False

       # ===================procesar clicks===================
       elif evento.type == pygame.MOUSEBUTTONDOWN:
           mouseX, mouseY = evento.pos

           if pantalla_actual == "menu":
               procesar_click_menu(mouseX, mouseY)

           elif pantalla_actual == "elegir_turno":
               procesar_click_elegir_turno(mouseX, mouseY)

           elif pantalla_actual == "jugando":
               if juego_terminado:
                   pantalla_ganador_conclick(mouseX, mouseY)
                   # evitar procesar clicks como jugadas normales cuando juego_terminado es True
                   continue

               # solo procesar clicks si es turno del jugador humano
               if turno == jugador_humano:
                   if (mouseX >= 20 and mouseX <= 590) and (mouseY >= 20 and mouseY <= 590):
                       fila = (mouseY - 20) // 190
                       columna = (mouseX - 20) // 190
                       # guardar el turno de nuestra matriz
                       if tablero[fila][columna] == '':
                           tablero[fila][columna] = turno
                           # verificar si con la jugada alguien ya ganó
                           fin_juego = verificar_ganador()
                           if (fin_juego == True):
                               juego_terminado = True
                               ganador = turno  # guardamos quién ganó
                           # si no hay ganador, verificar empate
                           else:
                               empate = verificar_empate()
                               if empate:
                                   juego_terminado = True
                                   ganador = 'empate'  # marcamos que fue empate
                               else:
                                   # cambiar turno a la IA
                                   turno = jugador_ia
                                   # ia juega su movimiento
                                   if not juego_terminado:
                                       ia_juega()
                                       # cambiar el turno al humano
                                       if not juego_terminado:
                                           turno = jugador_humano

   # Dibujar la pantalla correspondiente
   if pantalla_actual == "menu":
       pantalla_menu()
   elif pantalla_actual == "elegir_turno":
       pantalla_elegir_turno()
   elif pantalla_actual == "jugando":
       graficar_tablero()
       if juego_terminado:
           if ganador == 'empate':
               pantalla_empate_sinclick()
           else:
               pantalla_ganador_sinclick()

   pygame.display.update()