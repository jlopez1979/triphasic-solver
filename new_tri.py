import tri_module as tri
import streamlit as st
st.set_page_config(page_title='Triphasic solver', layout='wide',page_icon='⚡')
st.title('Resolución de circuitos trifásicos')
if st.context.theme.type == 'dark':
    f = './Images/d'
else:
    f='./Images/'
# Información en la barra lateral:
with st.sidebar:
    st.header('Información general')
    st.subheader('Circuitos soportados:')
    st.markdown(
    """
    - EE: Estrella Equilibrada
    - TE: Triángulo Equilibrado
    - EDCN: Estrella Desequilibrada Con Neutro
    - EDSN: Estrella Desequilibrada Sin Neutro
    - TD: Triángulo Desequilibrado
    - CA12: Carga adicional entre a L1 y L2
    - CA23: Carga adicional entre a L2 y L3
    - CA31: Carga adicional entre a L3 y L1
    """
    )
    st.subheader('Notaciones aceptadas para introducir impedancias:')
    st.markdown(
    """
    - '40<-20' donde el '40' es el módulo y '-20' la fase (o desfase) en grados
    - '3+1j' donde '3' es la parte real y '1j' la parte imaginaria
    """
    )
    st.caption('Autor: Jaime López')
# Cuerpo principal 2 columnas: una para la tensión, otra para el número de elementos
col1, col2 = st.columns(2)
with col1:
    Vl =st.number_input('Tensión de línea en V',value=230)
with col2:
    ncol = st.number_input("Nùmero de circuitos", min_value=1, max_value=5, value = 2)
# Columnas dinámicas en función del número de elementos
cols = st.columns(ncol)
for i, col in enumerate(cols):
    with col: # Introducción de datos de cada elemento
        st.selectbox(f"Circuito #{i+1}",['EE','TE','EDCN','EDSN','TD','CA12','CA23','CA31'],
            placeholder="Selecciona",key=f"circ_{i}")
        if st.session_state[f"circ_{i}"] == 'EE':
            st.image(f+"EE.png")
            st.text_input('Impedancia Estrella',key=f"z1_{i}")
        elif st.session_state[f"circ_{i}"]=='TE':
            st.image(f+"TE.png")
            st.text_input('Impedancia Triángulo',key=f"z1_{i}")
        elif st.session_state[f"circ_{i}"]=='EDCN':
            st.image(f+"EDCN.png")
            st.text_input('Impedancia Estrella 1: $Z_1$',key=f"z1_{i}")
            st.text_input('Impedancia Estrella 2: $Z_2$',key=f"z2_{i}")
            st.text_input('Impedancia Estrella 3: $Z_3$',key=f"z3_{i}")
        elif st.session_state[f"circ_{i}"]=='EDSN':
            st.image(f+"EDSN.png")
            st.text_input('Impedancia Estrella 1: $Z_1$',key=f"z1_{i}")
            st.text_input('Impedancia Estrella 2: $Z_2$',key=f"z2_{i}")
            st.text_input('Impedancia Estrella 3: $Z_3$',key=f"z3_{i}")
        elif st.session_state[f"circ_{i}"]=='TD':
            st.image(f+"TD.png")
            st.text_input('Impedancia Triángulo 1: $Z_1$',key=f"z1_{i}")
            st.text_input('Impedancia Triángulo 2: $Z_2$',key=f"z2_{i}")
            st.text_input('Impedancia Triángulo 3: $Z_3$',key=f"z3_{i}")
        elif st.session_state[f"circ_{i}"]=='CA12':
            st.image(f+"CA12.png")
            st.text_input('Impedancia $Z_{12}$',key=f"z1_{i}")
        elif st.session_state[f"circ_{i}"]=='CA23':
            st.image(f+"CA23.png")
            st.text_input('Impedancia $Z_{23}$',key=f"z1_{i}")
        elif st.session_state[f"circ_{i}"]=='CA31':
            st.image(f+"CA31.png")
            st.text_input('Impedancia $Z_{31}$',key=f"z1_{i}")

# Calcular y escribir los resultados:        
if st.button("Calcula"):
    ST,I1,I2,I3 = 0,0,0,0
    cols2 = st.columns(ncol)
    for i, col in enumerate(cols):
        with col:
            if st.session_state[f"circ_{i}"] == 'EE':
                I, S = tri.ee(float(Vl),tri.impedance(st.session_state[f"z1_{i}"]))
            elif st.session_state[f"circ_{i}"] == 'TE':
                I, S = tri.te(float(Vl),tri.impedance(st.session_state[f"z1_{i}"]))
            elif st.session_state[f"circ_{i}"] == 'EDCN':
                I, S = tri.edcn(float(Vl),tri.impedance(st.session_state[f"z1_{i}"]),tri.impedance(st.session_state[f"z2_{i}"]),tri.impedance(st.session_state[f"z3_{i}"]))
            elif st.session_state[f"circ_{i}"] == 'EDSN':
                I, S, V0N = tri.edsn(float(Vl),tri.impedance(st.session_state[f"z1_{i}"]),tri.impedance(st.session_state[f"z2_{i}"]),tri.impedance(st.session_state[f"z3_{i}"]))
            elif st.session_state[f"circ_{i}"] == 'TD':
                I, S = tri.td(float(Vl),tri.impedance(st.session_state[f"z1_{i}"]),tri.impedance(st.session_state[f"z2_{i}"]),tri.impedance(st.session_state[f"z3_{i}"]))
            elif st.session_state[f"circ_{i}"] == 'CA12':
                I, S = tri.ca(float(Vl),tri.impedance(st.session_state[f"z1_{i}"]),12)
            elif st.session_state[f"circ_{i}"] == 'CA23':
                I, S = tri.ca(float(Vl),tri.impedance(st.session_state[f"z1_{i}"]),23)
            elif st.session_state[f"circ_{i}"] == 'CA31':
                I, S = tri.ca(float(Vl),tri.impedance(st.session_state[f"z1_{i}"]),31)
            ST+=sum(S)
            I1+=I[0]
            I2+=I[1]
            I3+=I[2]
            if st.session_state[f"circ_{i}"] == 'EDSN':
                st.write(f':blue[$V_{{0N}}$ = {V0N:.3f} = {tri.c2p(V0N)}V]')
            st.write(f':red[$I_{{L1}}$ = {I[0]:.3f} = {tri.c2p(I[0])}A]')
            st.write(f':red[$I_{{L2}}$ = {I[1]:.3f} = {tri.c2p(I[1])}A]')
            st.write(f':red[$I_{{L3}}$ = {I[2]:.3f} = {tri.c2p(I[2])}A]')
            if st.session_state[f"circ_{i}"][0] != 'C':
                st.write(f':green[$S_{{Z1}}$ = {S[0]:.3f} = {tri.c2p(S[0])}VA]')
                st.write(f':green[$S_{{Z2}}$ = {S[1]:.3f} = {tri.c2p(S[0])}VA]')
                st.write(f':green[$S_{{Z3}}$ = {S[2]:.3f} = {tri.c2p(S[0])}VA]')
            st.write(f':green[$S_{{T}}$ = {sum(S):.3f} = {tri.c2p(sum(S))}VA]')
    if ncol > 1:
        st.divider()  # 
        st.header('Valores totales:')
        st.write(f':red[Corriente de la línea 1: $I_{{L1}}$ = {I1:.3f} = {tri.c2p(I1)}A]')
        st.write(f':red[Corriente de la línea 2: $I_{{L2}}$ = {I2:.3f} = {tri.c2p(I2)}A]')
        st.write(f':red[Corriente de la línea 3: $I_{{L3}}$ = {I3:.3f} = {tri.c2p(I3)}A]')
        st.write(f':green[Potencia aparente total: $S_{{T}}$ = {ST:.3f} = {tri.c2p(ST)}VA]')