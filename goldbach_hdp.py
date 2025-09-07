import gmpy2
import os

# Archivos de progreso y alertas
PROGRESO_FILE = "ultimo_numero.txt"
ALERT_FILE = "alertas_goldbach.txt"

LIMITE_CRIBA = 10**6  # primos pequeños precalculados

# Generar primos pequeños con cribado
def generar_primos_criba(limite):
    sieve = [True] * (limite + 1)
    sieve[0:2] = [False, False]
    for i in range(2, int(limite**0.5) + 1):
        if sieve[i]:
            for j in range(i*i, limite + 1, i):
                sieve[j] = False
    return [i for i, es in enumerate(sieve) if es]

primos_pequenos = generar_primos_criba(LIMITE_CRIBA)

# Cargar progreso
if os.path.exists(PROGRESO_FILE):
    with open(PROGRESO_FILE, "r") as f:
        try:
            inicio = int(f.read())
            if inicio % 2 != 0:
                inicio += 1
        except ValueError:
            inicio = 4
else:
    inicio = 4

def goldbach_ultra(n):
    """
    Encuentra un par de primos que sumen n rápidamente:
    1. Primero prueba primos pequeños.
    2. Luego intenta n-p con p = n//2, n//2 -1, n//2 +1, n//2 -3,... 
       hasta encontrar un par.
    """
    # Probar primos pequeños
    for p in primos_pequenos:
        if p > n // 2:
            break
        q = n - p
        if gmpy2.is_prime(q):
            return p, q

    # Probar primos cercanos a n/2
    delta = 0
    max_delta = 10**6  # buscar alrededor de n/2 hasta este margen
    while delta <= max_delta:
        for p in [n//2 - delta, n//2 + delta]:
            if p < 2:
                continue
            if gmpy2.is_prime(p):
                q = n - p
                if gmpy2.is_prime(q):
                    return p, q
        delta += 1
    return None

def recorrer_pares_ultra(inicio):
    num = inicio
    try:
        while True:
            pares = goldbach_ultra(num)
            if pares:
                print(f"{num} = {pares[0]} + {pares[1]}")
            else:
                print("\n" + "="*60)
                print(f"⚠️ ALERTA: {num} NO PUDO SER EXPRESADO COMO SUMA DE DOS PRIMOS ⚠️")
                print("="*60 + "\n")
                
                # Guardar número problemático en alertas_goldbach.txt sin sobrescribir
                with open(ALERT_FILE, "a") as f:
                    f.write(f"{num}\n")
                
                break

            num += 2

            # Guardar progreso cada 100 pares
            if num % 100 == 0:
                with open(PROGRESO_FILE, "w") as f:
                    f.write(str(num))

    except KeyboardInterrupt:
        with open(PROGRESO_FILE, "w") as f:
            f.write(str(num))
        print("\nProceso detenido por el usuario.")

if __name__ == "__main__":
    recorrer_pares_ultra(inicio)
