from math import pi, tan, sin, cos, acos, atan, sqrt
from cmath import rect, phase
f = 50
w = 2*pi*f
def impedance(Z):
    if 'j' in Z:
        return complex(Z)
    elif '<' in Z:
        mod = float(Z.split('<')[0])
        fase = float(Z.split('<')[1])
        return rect(mod,fase*pi/180)
    else:
        try:
            f = float(Z)
            return f
        except:
            return 'Introduce un valor válido de Z'
    
def c2p(a): # Imprime por pantalla un complejo en notación polar (ángulo en grados)
    return f'{abs(a):.3f}<{phase(a)*180/pi:.3f}'
def tension(V): # A partir del modulo de la tensión de línea devuelve las tensiones de fase y línea (criterio secuencia directa)
    return [rect(V/sqrt(3),90*pi/180),rect(V/sqrt(3),-30*pi/180),rect(V/sqrt(3),-150*pi/180),rect(V,120*pi/180),V,rect(V,-120*pi/180)]

# def z_equiv(serie,R,L,C):
#     Zl = w*L*1j
#     Zc_calc = lambda x: 0 if C == 0 else 1/(w*C*1j)
#     Zc = Zc_calc(C)
#     Zt_calc = lambda a,b,c: a+b+c if serie else sum([1/x for x in [a,b,c] if abs(x) > 0])**(-1)
#     Zt = Zt_calc(R,Zl,Zc)
#     return Zt

def results_ecn(V1o,V2o,V3o,Von,I1,I2,I3):
    Cur=[I1,I2,I3]
    S1=V1o*I1.conjugate()
    S2=V2o*I2.conjugate()
    S3=V3o*I3.conjugate()
    St=S1+S2+S3
    Apar=[S1,S2,S3]
    return Cur,Apar

##########################################################
# Configuraciones
##########################################################
# TRIANGULO EQUILIBRADO
##########################################################
def te(VL,Zt):   #Triángulo equilibrado
    Currs,Apars=td(VL,Zt,Zt,Zt)
    return Currs,Apars

##########################################################
# TRIANGULO DESEQUILIBRADO
##########################################################    
def td(VL,Zt1,Zt2,Zt3):   #Triángulo desequilibrado
#    print("Circuito Triángulo")
    V1N, V2N, V3N, V12, V23, V31 = tension(VL)
    I12=V12/Zt1
    I23=V23/Zt2
    I31=V31/Zt3
    I1=I12-I31
    I2=I23-I12
    I3=I31-I23
    S1=V12*I12.conjugate()
    S2=V23*I23.conjugate()
    S3=V31*I31.conjugate()
    Currs=[I1,I2,I3]
    Apars=[S1,S2,S3]
    return Currs,Apars

##########################################################
# ESTRELLA EQUILIBRADO
##########################################################        
def ee(VL,Zt):   #Estrella equilibrado
#    print("Circuito Estrella Equilibrado")
    Currs,Apars=edcn(VL,Zt,Zt,Zt)
    return Currs,Apars

##########################################################
# ESTRELLA DESEQUILIBRADO CON NEUTRO
##########################################################    
def edcn(VL,Zt1,Zt2,Zt3):   #Estrella desequilibrado con neutro
#    print("Circuito Estrella Desequilibrado CON Neutro")
    V1N, V2N, V3N, V12, V23, V31 = tension(VL)
    Von=0
    I1=V1N/Zt1
    I2=V2N/Zt2
    I3=V3N/Zt3
    #In=I1+I2+I3
    Currs,Apars=results_ecn(V1N,V2N,V3N,Von,I1,I2,I3)
    return Currs,Apars

##########################################################
# ESTRELLA DESEQUILIBRADO SIN NEUTRO
##########################################################    
def edsn(VL,Zt1,Zt2,Zt3):   #Estrella desequilibrado sin neutro
#    print("Circuito Estrella Desequilibrado SIN Neutro")
    V1N, V2N, V3N, V12, V23, V31 = tension(VL)
    Von=(V1N/Zt1+V2N/Zt2+V3N/Zt3)*(1/Zt1+1/Zt2+1/Zt3)**(-1)

    V1o=V1N-Von

    V2o=V2N-Von

    V3o=V3N-Von

    I1=(V1o)/Zt1
    I2=(V2o)/Zt2
    I3=(V3o)/Zt3
    Currs,Apars=results_ecn(V1o,V2o,V3o,Von,I1,I2,I3)
    return Currs,Apars,Von

##########################################################
# CARGA ADICIONAL
##########################################################    
def ca(VL,Za,con):   #Carga adicional
    '''Ejecución: ca(VL,Za,con)
    VL: es el módulo de la tensión de línea
    Za: es la carga (impedancia) adicional
    con: a qué está conectada la carga ("12", "23" o "31")'''
    V1N, V2N, V3N, V12, V23, V31 = tension(VL)
    I1, I2, I3 = [0, 0, 0]
    S12, S23, S31 = [0, 0, 0]
    if con == 12:
        I1 = V12/Za
        I2 = -I1
        S12 = V12*I1.conjugate()
    elif con == 23:
        I2 = V23/Za
        I3 = -I2
        S23 = V23*I2.conjugate()
    elif con == 31:
        I3 = V31/Za
        I1 = -I3
        S31 = V31*I3.conjugate()
    Currs = [I1, I2, I3]
    Apars = [S12, S23, S31]
    return Currs,Apars