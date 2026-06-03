# -*- coding: utf-8 -*-
"""
Created on Mon Jun  1 17:07:14 2026

@author: thezu
"""

# -*- coding: utf-8 -*-

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import pandas as pd
import streamlit.components.v1 as components

# Verificación de Google
st.markdown("""
    <meta name="google-site-verification" content="TU_CODIGO_COPIADO_AQUI" />
""", unsafe_allow_html=True)

# --- CORRECCIÓN CRÍTICA: Inicializar el estado ANTES de usarlo ---
if 'M_carga' not in st.session_state:
    st.session_state.M_carga = np.array([[45.0, 30.0, 15.0], [60.0, 40.0, 20.0], [80.0, 50.0, 35.0]])

# ... aquí sigue el resto de tu código original ...

# 1. ESTA TIENE QUE SER LA PRIMERA LÍNEA DE STREAMLIT EN TODO EL SCRIPT
st.set_page_config(
    page_title="NAVIX-LOADICATOR Enterprise Edition", 
    page_icon="⚓", 
    layout="wide"
)

# Estilo CSS Avanzado
st.markdown("""
    <style>
    .main { background-color: #0B132B; color: #F4F5F6; }
    h1, h2, h3 { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    .stAlert { border-radius: 6px; }
    div[data-testid="stSidebarUserContent"] { background-color: #1C2541; }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# BARRA LATERAL: CONTROL DE SISTEMA
# ==========================================
st.sidebar.image("https://img.icons8.com/external-flatart-icons-solid-flatarticons/128/external-ship-maritime-flatart-icons-solid-flatarticons.png", width=70)
st.sidebar.title("NAVIX™ Loadicator")
st.sidebar.caption("SISTEMA DE GESTIÓN INTEGRAL DE ESTABILIDAD v5.5")
st.sidebar.write("---")

modulo = st.sidebar.radio(
    "MÓDULO DE OPERACIÓN:",
    [
        "📊 [1] Ver Plano de Estiba Actual", 
        "💧 [2] Calcular Lastrado Automático", 
        "🌊 [3] Simular Derrota de Ruta (Ecuador)", 
        "📜 [4] Análisis de Ejes Críticos e Inercia"
    ]
)

st.sidebar.write("---")
tipo_buque = st.sidebar.selectbox(
    "Flota Activa:",
    ["Portacontenedores (Class-Max TEUs)", "Petrolero (Crude Oil)", "LNG Carrier (Spherical Tanks)"]
)

st.sidebar.info("**Terminal:** ESMENA-Ecuador\n\n**Estado:** Operación de Carga\n\n**Buque Escolar:** BAE Hualcopo / Adaptado")

# Configurar etiquetas dinámicas según el tipo de buque
if "Portacontenedores" in tipo_buque:
    unidad = "Contenedores (t)"
    tipo_carga = "Bahía de Contenedores"
elif "Petrolero" in tipo_buque:
    unidad = "Tanques de Crudo (t)"
    tipo_carga = "Sección de Tanques de Carga"
else:
    unidad = "Esferas de Gas (t)"
    tipo_carga = "Cúpulas de Almacenamiento"

# Estado de la matriz en memoria
if 'M_carga' not in st.session_state:
    st.session_state.M_carga = np.array([[45.0, 30.0, 15.0], [60.0, 40.0, 20.0], [80.0, 50.0, 35.0]])

# ==========================================
# MÓDULO 1: PLANO DE ESTIBA ACTUAL (MATRICES)
# ==========================================
if "Plano de Estiba" in modulo:
    st.title(f"📊 Distribución de Peso en la {tipo_carga}")
    st.write("Modifique el peso de las celdas matriciales en tiempo real para simular la estiba.")
    
    col_inputs, col_visual = st.columns([1, 1.2])
    
    with col_inputs:
        st.subheader("📋 Consola de Entrada de Datos")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown("### 🟦 Banda de Babor")
            ba = st.number_input(f"Alto / Cubierta - Babor ({unidad})", value=float(st.session_state.M_carga[0,0]), step=5.0, key="ba_in")
            bm = st.number_input(f"Medio / Entrepunte - Babor ({unidad})", value=float(st.session_state.M_carga[1,0]), step=5.0, key="bm_in")
            bb = st.number_input(f"Bajo / Plan - Babor ({unidad})", value=float(st.session_state.M_carga[2,0]), step=5.0, key="bb_in")
        with c2:
            st.markdown("### ⚓ Crujía / Centro")
            ca = st.number_input(f"Alto / Cubierta - Centro ({unidad})", value=float(st.session_state.M_carga[0,1]), step=5.0, key="ca_in")
            cm = st.number_input(f"Medio / Entrepunte - Centro ({unidad})", value=float(st.session_state.M_carga[1,1]), step=5.0, key="cm_in")
            cb = st.number_input(f"Bajo / Plan - Centro ({unidad})", value=float(st.session_state.M_carga[2,1]), step=5.0, key="cb_in")
        with c3:
            st.markdown("### 🟨 Banda de Estribor")
            ea = st.number_input(f"Alto / Cubierta - Estribor ({unidad})", value=float(st.session_state.M_carga[0,2]), step=5.0, key="ea_in")
            em = st.number_input(f"Medio / Entrepunte - Estribor ({unidad})", value=float(st.session_state.M_carga[1,2]), step=5.0, key="em_in")
            eb = st.number_input(f"Bajo / Plan - Estribor ({unidad})", value=float(st.session_state.M_carga[2,2]), step=5.0, key="eb_in")
            
        st.session_state.M_carga = np.array([[ba, ca, ea], [bm, cm, em], [bb, cb, eb]])
        M = st.session_state.M_carga
        
        st.write("#### Matriz Operacional Masas Activas $M$:")
        st.dataframe(M, use_container_width=True)
        
        pesos_banda = np.sum(M, axis=0)
        escora_val = pesos_banda[0] - pesos_banda[2]
        
        st.subheader("⚠️ Diagnóstico Hidrostático")
        if abs(escora_val) <= 20:
            st.success("✅ CONDICIÓN DE ESTIBA APRECIABLE: Parámetros dentro del margen de seguridad.")
        else:
            st.error(f"🚨 ALERTA DE ADRIZAMIENTO: Desbalance crítico por escora lateral ({abs(escora_val):.1f} t).")

    with col_visual:
        st.subheader("🚢 Terminal Visual (Sección Transversal del Casco)")
        fig, ax = plt.subplots(figsize=(6.5, 5.5), facecolor='#0B132B')
        ax.set_facecolor('#0B132B')
        ax.set_xlim(-0.5, 3.5)
        ax.set_ylim(-0.5, 4.5)
        
        for f in range(3):
            for c in range(3):
                peso = M[f, c]
                if peso > 75: color_bodega = '#EF4444'
                elif peso < 25: color_bodega = '#1E293B'
                else: color_bodega = '#0EA5E9'
                    
                rect = patches.Rectangle((c + 0.5, 2.5 - f), 0.9, 0.78, linewidth=1.5, edgecolor='#334155', facecolor=color_bodega)
                ax.add_patch(rect)
                ax.text(c + 0.95, 2.88 - f, f"{peso:.0f}", color='white', weight='bold', ha='center', va='center', fontsize=10)
        
        color_casco = '#64748B'
        ax.plot([0.2, 3.8], [0.3, 0.3], color=color_casco, linewidth=4)
        ax.plot([0.2, 0.2], [0.3, 3.5], color=color_casco, linewidth=4)
        ax.plot([3.8, 3.8], [0.3, 3.5], color=color_casco, linewidth=4)
        
        peso_total = np.sum(M)
        nivel_mar = 0.5 + (peso_total / 900) * 2.0
        nivel_mar = min(nivel_mar, 3.3)
        
        angulo_escora = (escora_val / 300) * 0.5
        ax.plot([-0.5, 4.0], [nivel_mar + angulo_escora, nivel_mar - angulo_escora], color='#38BDF8', linewidth=3, linestyle='--')
        ax.fill_between([-0.5, 4.0], [-0.5, -0.5], [nivel_mar + angulo_escora, nivel_mar - angulo_escora], color='#38BDF8', alpha=0.15)
        ax.axis('off')
        st.pyplot(fig)

# ==========================================
# MÓDULO 2: SISTEMAS DE ECUACIONES (LASTRE)
# ==========================================
elif "Calcular Lastrado" in modulo:
    st.title("💧 [Sistemas de Ecuaciones] Planta Automatizada de Lastre")
    M = st.session_state.M_carga
    pesos_banda = np.sum(M, axis=0)
    
    A = np.array([[1.0, 1.0, 1.0], [-4.5, 0.0, 4.5], [2.0, -1.0, 2.0]])
    
    col_lastre1, col_lastre2 = st.columns([1, 1])
    with col_lastre1:
        st.subheader("📥 Vector de Requerimientos Hidrostáticos ($b$)")
        b1 = st.number_input("Masa total de compensación líquida (b1)", value=140.0, step=10.0)
        sugerido_b2 = float((pesos_banda[2] - pesos_banda[0]) * 4.5)
        b2 = st.number_input("Momento de adrizamiento lateral requerido (b2)", value=sugerido_b2, step=10.0)
        b3 = st.number_input("Factor de corrección del centro de gravedad GM (b3)", value=95.0, step=5.0)
        b = np.array([b1, b2, b3])
        
        st.write("### Matriz de Coeficientes de Tanques $A$:")
        st.write(A)

    with col_lastre2:
        st.subheader("⚙️ Solución del Sistema ($A^{-1} \cdot b = x$)")
        det_A = np.linalg.det(A)
        
        if np.abs(det_A) > 1e-5:
            A_inv = np.linalg.inv(A)
            x = np.dot(A_inv, b)
            
            st.success("### Distribución Automática Calculada:")
            st.info(f"💧 **Tanque Babor (P):** {x[0]:.3f} t\n\n💧 **Tanque Central (C):** {x[1]:.3f} t\n\n💧 **Tanque Estribor (S):** {x[2]:.3f} t")
            
            fig_tq, ax_tq = plt.subplots(figsize=(5.5, 3), facecolor='#0B132B')
            ax_tq.set_facecolor('#1C2541')
            ax_tq.bar(["Tanque P", "Tanque C", "Tanque S"], x, color=['#38BDF8', '#0EA5E9', '#0284C7'], width=0.4)
            ax_tq.tick_params(colors='white')
            ax_tq.grid(axis='y', color='#334155', linestyle='--')
            st.pyplot(fig_tq)
        else:
            st.error("La matriz A no es regular (determinante cero).")

# ==========================================
# MÓDULO 3: SIMULACIÓN DE RUTA (ECUADOR)
# ==========================================
elif "Simular Derrota" in modulo:
    st.title("🌊 [Transformación Lineal] Simulación de Derrota y Cambio de Densidad")
    st.write("Trazado geométrico vectorial de trayectos marítimos y fluviales en el Ecuador.")

    puertos = {
        "Muelle de Esmeraldas": {"lat": 1.01, "lon": -79.65},
        "Muelle de Manta": {"lat": -0.94, "lon": -80.72},
        "Puerto de Guayaquil": {"lat": -2.28, "lon": -79.91},
        "Muelle de Puerto Bolívar": {"lat": -3.27, "lon": -80.00},
        "Muelle Galápagos (B. Moreno)": {"lat": -0.90, "lon": -89.61}
    }

    col_mapa, col_ruta_inputs = st.columns([1.3, 1])

    with col_ruta_inputs:
        st.subheader("⚓ Planificación de la Derrota")
        origen = st.selectbox("Muelle de Salida (Origen):", list(puertos.keys()), index=1)
        destino = st.selectbox("Muelle de Destino (Arribo):", list(puertos.keys()), index=2)
        
        st.write("---")
        st.subheader("📐 Parámetros de Calado Inicial en Mar")
        c_proa = st.slider("Calado Inicial de Proa (m)", 4.0, 16.0, 8.2)
        c_centro = st.slider("Calado Inicial de Centro (m)", 4.0, 16.0, 8.4)
        c_popa = st.slider("Calado Inicial de Popa (m)", 4.0, 16.0, 8.3)
        
        calados_mar = np.array([c_proa, c_centro, c_popa])

        if "Guayaquil" in destino:
            factor_escala = 1.025 / 1.000
            st.warning("⚠️ NOTA HIDROGRÁFICA: Ingreso detectado al Río Guayas (Agua Dulce). El buque perderá empuje y aumentará su calado.")
        else:
            factor_escala = 1.000

        T = np.array([[factor_escala, 0.0, 0.0], [0.0, factor_escala, 0.0], [0.0, 0.0, factor_escala]])
        calados_rio = np.dot(T, calados_mar)

        cm = st.number_input(f"Hold / Medio ({factor_escala})", value=float(c_centro))
        st.info(f"⚓ **Proa:** {calados_rio[0]:.3f} m | **Centro:** {calados_rio[1]:.3f} m | **Popa:** {calados_rio[2]:.3f} m")

    with col_mapa:
        st.subheader("🗺️ Carta Náutica Digital del Ecuador")
        
        fig_map, ax_map = plt.subplots(figsize=(7, 6), facecolor='#0B132B')
        ax_map.set_facecolor('#1C2541')
        
        costa_lon = [-80.1, -80.0, -80.4, -81.0, -80.8, -79.9, -80.0, -79.8, -80.1]
        costa_lat = [1.2, 0.8, 0.5, -2.2, -2.3, -2.3, -2.7, -3.2, -3.5]
        ax_map.fill(costa_lon, costa_lat, color='#1E293B', edgecolor='#475569', linewidth=1.5, label='Ecuador Continental')
        
        ax_map.add_patch(patches.Ellipse((-89.6, -0.9), 0.6, 0.4, color='#334155', edgecolor='#475569'))
        ax_map.text(-89.6, -0.4, "Región Insular", color='#94A3B8', fontsize=8, ha='center')

        for p_name, coords in puertos.items():
            if p_name == origen or p_name == destino:
                ax_map.plot(coords["lon"], coords["lat"], marker='o', color='#EF4444', markersize=11, zorder=5)
                ax_map.text(coords["lon"] + 0.15, coords["lat"], p_name, color='#F8FAFC', fontsize=9, weight='bold')
            else:
                ax_map.plot(coords["lon"], coords["lat"], marker='o', color='#0EA5E9', markersize=6, zorder=4)
                ax_map.text(coords["lon"] + 0.15, coords["lat"], p_name, color='#94A3B8', fontsize=8)

        lon_linea = [puertos[origen]["lon"], puertos[destino]["lon"]]
        lat_linea = [puertos[origen]["lat"], puertos[destino]["lat"]]
        ax_map.plot(lon_linea, lat_linea, color='#34D399', linestyle='--', linewidth=2.5, label='Línea de Navegación')
        
        ax_map.set_xlabel("Longitud (W)", color='#94A3B8')
        ax_map.set_ylabel("Latitud", color='#94A3B8')
        ax_map.tick_params(colors='#475569', labelsize=8)
        ax_map.grid(color='#334155', linestyle=':', alpha=0.5)
        ax_map.set_xlim(-91.0, -78.0)
        ax_map.set_ylim(-4.0, 2.0)
        
        st.pyplot(fig_map)

# ==========================================
# MÓDULO 4: VALORES Y VECTORES PROPIOS
# ==========================================
else:
    st.title("📜 [Valores Propios] Análisis Ejes Críticos de Inercia del Casco")
    st.write("Cálculo matricial de las frecuencias estructurales y estabilidad torsional.")
    
    I = np.array([[160.0, -25.0, 0.0], [-25.0, 120.0, 20.0], [0.0, 20.0, 85.0]])
    st.write("### Tensor de Rigidez / Inercia de la Estructura (Matriz $I$):")
    st.write(I)
    
    valores, vectores = np.linalg.eig(I)
    st.subheader("⚛️ Análisis de Frecuencias Propias")
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric(label="🧬 Lambda 1 (Eje Torsión X)", value=f"{valores[0]:.4f}")
    with c2:
        st.metric(label="🧬 Lambda 2 (Eje Flexión Y)", value=f"{valores[1]:.4f}")
    with c3:
        st.metric(label="🧬 Lambda 3 (Eje Cortante Z)", value=f"{valores[2]:.4f}")
        
    st.write("---")
    st.subheader("📐 Matriz Completa de Vectores Propios Asociados:")
    st.dataframe(vectores, use_container_width=True)
    st.info("💡 **Interpretación de Cátedra:** Estos vectores definen las direcciones principales de deformación del casco ante solicitaciones dinámicas.")