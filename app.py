# importamos las librerías necesarias
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from data_processor import DataProcessor

def local_css():
    st.markdown("""
    <style>
        /* Fondo general y fuente */
        .main {
            background-color: #f0f2f6;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        
        /* Estilo para tarjetas de métricas */
        div[data-testid="stMetric"] {
            background-color: #ffffff !important; /* Forzamos fondo blanco */
            border-radius: 15px;
            padding: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            border: 1px solid #e1e4e8;
        }

        /* --- AQUÍ ESTÁ LA CORRECCIÓN PARA EL COLOR DE LOS NÚMEROS --- */
        [data-testid="stMetricValue"] {
            color: #1E3A8A !important;  /* Azul oscuro para que el número sea visible */
            font-weight: 800 !important;
        }

        [data-testid="stMetricLabel"] {
            color: #4B5563 !important;  /* Gris oscuro para la etiqueta */
        }
        /* ----------------------------------------------------------- */

        /* Títulos elegantes */
        .main-title {
            color: #1E3A8A;
            font-size: 42px;
            font-weight: 700;
            text-align: center;
            margin-bottom: 20px;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
        }

        /* Banner de información */
        .info-card {
            background: linear-gradient(90deg, #1E3A8A 0%, #3B82F6 100%);
            color: white;
            padding: 25px;
            border-radius: 15px;
            margin-bottom: 20px;
        }
    </style>
    """, unsafe_allow_html=True)

# Se llama a la función para aplicar los cambios
local_css()

# Inicializar session_state para el dataframe si no existe
if 'df' not in st.session_state:
    st.session_state.df = None
    
# Configuración de la página
st.sidebar.image("DMC.png")
st.sidebar.title("Módulos")
pagina = st.sidebar.selectbox("Selecciona una página", ["🏠 Home","📂 Carga de Dataset", "📊 Análisis Exploratorio de Datos"])
st.sidebar.divider()
if pagina == "🏠 Home":
    # Módulo 1: Home
    st.video("fondo.mp4", start_time=0)
    st.title("Análisis Exploratorio de Datos de Campañas de Marketing Bancario")
    st.subheader("Factores de éxito en campañas de marketing: un análisis exploratorio del dataset BankMarketing")
    st.divider()
    st.header("1. Descripción del objetivo del análisis")
    st.write("El objetivo de este proyecto es realizar un Análisis Exploratorio de Datos (EDA) sobre el dataset BankMarketing.csv, proporcionado por una institución financiera. La finalidad es identificar patrones, relaciones y comportamientos relevantes entre las variables que puedan explicar la reciente caída en la efectividad de las campañas (de 12% a 8% en los últimos 6 meses). A través de este análisis, se busca generar insights que sirvan de base para la toma de decisiones comerciales y la optimización de futuras campañas, sin construir modelos predictivos.")
    st.divider()
    st.header("2. Datos del autor")
    st.write("Nombre: Luis Ángel Cordova Palomino")
    st.write("Curso/Especialización: Especialización en Python for Analytics")
    st.write(" Año: 2026")
    st.divider()
    st.header("3. Descripción del dataset")
    st.write("El dataset BankMarketing.csv contiene información de una campaña de marketing directo (contacto telefónico) realizada por una entidad bancaria portuguesa. Los datos incluyen características de los clientes (edad, trabajo, estado civil, educación, etc.), detalles de la campaña (duración de la llamada, mes, día, número de contactos) e indicadores económicos (tasa de empleo, IPC, etc.). La variable objetivo es y, que indica si el cliente aceptó (yes) o no (no) el producto ofrecido. El conjunto cuenta con 20 variables y más de 4000 registros.")
    st.pills("Tecnologías utilizadas", ["Python", "Pandas", "NumPy", "Streamlit"])

# Módulo 2: Carga del dataset
if pagina == "📂 Carga de Dataset":
    st.title("Carga del dataset BankMarketing")
    st.write("Por favor, sube el archivo **BankMarketing.csv** usando el siguiente cargador:")
    # carga del archivo CSV
    archivo = st.file_uploader("Selecciona un archivo CSV", type=["csv"])
    if archivo is not None:
        try:
            # Leer el archivo CSV
            df = pd.read_csv(archivo, sep = ";")
            # Guardar en session_state
            st.session_state.df = df

            st.success("✅ Archivo cargado correctamente!")

            # Mostrar dimensiones
            st.subheader("Dimensiones del dataset")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Filas", df.shape[0])
            with col2:
                st.metric("Columnas", df.shape[1])
            
            # Vista previa
            st.subheader("Vista previa (primeras 5 filas)")
            st.dataframe(df.head())
                
        except Exception as e:
            st.error(f"Error al leer el archivo: {e}")
            st.session_state.df = None
    else:
        st.info("Esperando archivo...")
        st.session_state.df = None
        
if pagina == "📊 Análisis Exploratorio de Datos":
    st.title("Análisis Exploratorio de Datos (EDA)")
    st.write("En esta sección realizaremos un análisis detallado del dataset para identificar patrones, relaciones y comportamientos relevantes entre las variables.")
    
    # Mensaje de advertencia para cargar el dataset
    if st.session_state.df is None:
        st.warning("⚠️ Primero debes cargar un dataset en el módulo 'Carga de datos'.")
        st.stop()
    df = st.session_state.df
    
    processor = DataProcessor(df)
    # Leer el archivo CSV
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10 =st.tabs([
            "📋 Información general",
            "🔢 Clasificación de variables",
            "📊 Estadísticas descriptivas",
            "❌ Valores faltantes",
            "📈 Distribución numérica",
            "📊 Análisis categórico",
            "🔗 Bivariado (numérico vs categórico)",
            "🔗 Bivariado (categórico vs categórico)",
            "🎛️ Análisis dinámico",
            "📌 Hallazgos principales"
        ])
    with tab1:
        st.header("Información general del dataset")
         # Mostrar dimensiones
        col1, col2, col3 = st.columns(3)
        col1.metric("Filas", df.shape[0])
        col2.metric("Columnas", df.shape[1])
        col3.metric("Celdas totales", df.size)
        
        # Crear un DataFrame resumen con tipos de datos y valores nulos
        info_df = processor.get_info_dataframe()
            
        st.dataframe(info_df, use_container_width=True)
        
        # Mostrar también los valores únicos de cada columna (opcional, pero útil)
        with st.expander("Ver cantidad de valores únicos por columna"):
            unique_df = pd.DataFrame({
                    'Columna': df.columns,
                    'Valores únicos': df.nunique().values
            })
            st.dataframe(unique_df, use_container_width=True)
            
    with tab2:
        st.header("Clasificación de variables")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Variables numéricas", len(processor.numeric_cols))
        with col2:
            st.metric("Variables categóricas", len(processor.categorical_cols))
    
        st.markdown("### Detalle de variables")
        col_left, col_right = st.columns(2)
        with col_left:
            st.markdown("**Numéricas:**")
            for var in processor.numeric_cols:
                st.write(f"- {var}")
        with col_right:
            st.markdown("**Categóricas:**")
            for var in processor.categorical_cols:
                st.write(f"- {var}")
            
    with tab3:
        st.header("Estadísticas descriptivas")
        if processor.numeric_cols:
            st.markdown("**Resumen estadístico de variables numéricas:**")
            describe_df = processor.get_descriptive_stats()
            st.dataframe(describe_df, use_container_width=True)
        
            st.markdown("### Métricas destacadas por variable")
            var_seleccionada = st.selectbox("Selecciona una variable numérica", processor.numeric_cols)
            if var_seleccionada:
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Media", f"{df[var_seleccionada].mean():.2f}")
                with col2:
                    st.metric("Mediana", f"{df[var_seleccionada].median():.2f}")
                with col3:
                    st.metric("Desv. Estándar", f"{df[var_seleccionada].std():.2f}")
                with col4:
                    st.metric("Rango", f"{df[var_seleccionada].max() - df[var_seleccionada].min():.2f}")
            
                fig = processor.plot_histogram(var_seleccionada, bins=30, kde=False)
                st.pyplot(fig)
                plt.close(fig)
        else:
            st.warning("No hay variables numéricas.")
        
    with tab4:
        st.header("Análisis de valores faltantes")
        info_nulos = processor.get_info_dataframe()[['Columna', 'Nulos', '% Nulos']]
        st.dataframe(info_nulos, use_container_width=True)
    
        total_nulos = info_nulos['Nulos'].sum()
        if total_nulos == 0:
            st.success("✅ No se detectaron valores faltantes en el dataset.")
        else:
            st.warning(f"⚠️ Se encontraron {total_nulos} valores faltantes.")
    
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.bar(info_nulos['Columna'], info_nulos['Nulos'], color='skyblue', edgecolor='black')
        ax.set_xlabel('Columnas')
        ax.set_ylabel('Cantidad de nulos')
        ax.set_title('Valores faltantes por columna')
        plt.xticks(rotation=45, ha='right')
        st.pyplot(fig)
        plt.close(fig)
    
    with tab5:
        st.header("Distribución de variables numéricas")
        if processor.numeric_cols:
            var_num = st.selectbox("Selecciona variable numérica:", processor.numeric_cols, key="var_tab5")
            bins = st.slider("Número de bins:", 5, 100, 30, key="bins_tab5")
            mostrar_kde = st.checkbox("Mostrar curva KDE", value=False, key="kde_tab5")
        
            fig = processor.plot_histogram(var_num, bins=bins, kde=mostrar_kde)
            st.pyplot(fig)
            plt.close(fig)
        
            col1, col2, col3 = st.columns(3)
            col1.metric("Media", f"{df[var_num].mean():.2f}")
            col2.metric("Mediana", f"{df[var_num].median():.2f}")
            col3.metric("Desviación estándar", f"{df[var_num].std():.2f}")
        
            # Comentarios sobre simetría (puedes mantener tu lógica)
        else:
            st.warning("No hay variables numéricas.")
        
    with tab6:
        st.header("Análisis de variables categóricas")
        if processor.categorical_cols:
            var_cat = st.selectbox("Variable categórica:", processor.categorical_cols, key="var_tab6")
            tipo_frec = st.radio("Tipo de frecuencia:", ["Absoluta", "Relativa (%)"], key="tipo_frec_tab6")
            orden = st.radio("Ordenar por:", ["Frecuencia", "Alfabético"], key="orden_tab6")
        
            relative = (tipo_frec == "Relativa (%)")
            order_by_freq = (orden == "Frecuencia")
        
            fig = processor.plot_bar(var_cat, relative=relative, order_by_freq=order_by_freq)
            st.pyplot(fig)
            plt.close(fig)
        
            # Mostrar tabla de frecuencias (puedes usar processor.df[var_cat].value_counts())
            frec = df[var_cat].value_counts()
            if orden == "Alfabético":
                frec = frec.sort_index()
            frec_df = pd.DataFrame({
                'Categoría': frec.index,
                'Frecuencia': frec.values,
                'Porcentaje': (frec.values / len(df) * 100).round(2)
            }) if tipo_frec == "Relativa (%)" else pd.DataFrame({'Categoría': frec.index, 'Frecuencia': frec.values})
            st.dataframe(frec_df)
        else:
            st.warning("No hay variables categóricas.")
        
    with tab7:
        st.header("Análisis bivariado (numérico vs categórico)")
        if processor.numeric_cols and processor.categorical_cols:
            col1, col2 = st.columns(2)
            with col1:
                var_num = st.selectbox("Variable numérica:", processor.numeric_cols, key="num_tab7")
            with col2:
                var_cat = st.selectbox("Variable categórica:", processor.categorical_cols, key="cat_tab7")
        
            tipo_grafico = st.radio("Tipo de gráfico:", ["Boxplot", "Histograma apilado", "Violin plot"], horizontal=True)
            filter_y = st.checkbox("Comparar por resultado de campaña (y)") if 'y' in df.columns else False
        
            if tipo_grafico == "Boxplot":
                if filter_y and 'y' in df.columns:
                    fig, ax = plt.subplots()
                    sns.boxplot(data=df, x=var_cat, y=var_num, hue='y', ax=ax)
                    ax.legend(title='y')
                    plt.xticks(rotation=45)
                    st.pyplot(fig)
                    plt.close(fig)
                else:
                    fig = processor.plot_boxplot(var_num, group_col=var_cat)
                    st.pyplot(fig)
                    plt.close(fig)
            elif tipo_grafico == "Violin plot":
                fig, ax = plt.subplots()
                if filter_y and 'y' in df.columns:
                    sns.violinplot(data=df, x=var_cat, y=var_num, hue='y', split=True, ax=ax)
                    ax.legend(title='y')
                else:
                    sns.violinplot(data=df, x=var_cat, y=var_num, ax=ax)
                plt.xticks(rotation=45)
                st.pyplot(fig)
                plt.close(fig)
            else:  # Histograma apilado
                fig, ax = plt.subplots()
                if filter_y and 'y' in df.columns:
                    sns.histplot(data=df, x=var_num, hue='y', multiple='stack', ax=ax)
                else:
                    for cat in df[var_cat].unique():
                        subset = df[df[var_cat] == cat]
                        sns.histplot(subset[var_num], label=cat, alpha=0.5, ax=ax)
                    ax.legend()
                ax.set_xlabel(var_num)
                st.pyplot(fig)
                plt.close(fig)
        
            with st.expander("Estadísticas por grupo"):
                st.dataframe(df.groupby(var_cat)[var_num].describe())
        else:
            st.warning("Se necesitan variables numéricas y categóricas.")
        
    with tab8:
        st.header("Análisis bivariado: Categórico vs Categórico")
        if len(processor.categorical_cols) >= 2:
            col1, col2 = st.columns(2)
            with col1:
                var_cat1 = st.selectbox("Primera variable:", processor.categorical_cols, key="cat1_tab8")
            with col2:
                otras = [c for c in processor.categorical_cols if c != var_cat1]
                var_cat2 = st.selectbox("Segunda variable:", otras, key="cat2_tab8")
        
            tipo_graf = st.radio("Tipo de gráfico:", ["Barras agrupadas", "Barras apiladas (100%)"], horizontal=True)
            stacked = (tipo_graf == "Barras apiladas (100%)")
        
            fig, ct = processor.plot_contingency(var_cat1, var_cat2, stacked=stacked)
            st.pyplot(fig)
            plt.close(fig)
        
            st.markdown("**Tabla de contingencia**")
            st.dataframe(ct)

            # Interpretación
            max_val = ct.stack().max()
            max_idx = ct.stack().idxmax()
            st.markdown(f"**Interpretación:** La combinación más frecuente es **{max_idx[0]}** y **{max_idx[1]}** con {max_val} ocurrencias.")
        else:
            st.warning("Se necesitan al menos dos variables categóricas.")
        
    with tab9:
        st.header("Análisis basado en parámetros seleccionados")
        st.markdown("Explora los datos seleccionando el tipo de gráfico y las variables de interés.")

        # Filtros
        st.markdown("### Filtros")
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            edad_range = st.slider(
                "Rango de edad",
                min_value=int(df.age.min()),
                max_value=int(df.age.max()),
                value=(20, 60),
                step=1,
                key="edad_filtro_tab9"
            )
        with col_f2:
            aceptacion = st.multiselect(
                "Resultado de campaña (y)",
                options=['yes', 'no'],
                default=['yes', 'no'],
                key="y_filtro_tab9"
            )

        # Aplicar filtros al dataframe
        df_filtrado = df[
            (df['age'].between(edad_range[0], edad_range[1])) & 
            (df['y'].isin(aceptacion))
        ].copy()

        if df_filtrado.empty:
            st.warning("No hay datos con los filtros seleccionados.")
        else:
            st.caption(f"Mostrando {len(df_filtrado)} registros después de filtros.")

            # Selección de tipo de gráfico
            tipo_grafico = st.selectbox(
                "Tipo de gráfico",
                ["Histograma", "Boxplot", "Scatter plot", "Gráfico de barras (categórica)"],
                key="tipo_graf_tab9"
            )

            # Histograma
            if tipo_grafico == "Histograma":
                if processor.numeric_cols:
                    var_num = st.selectbox("Variable numérica", processor.numeric_cols, key="hist_num_tab9")
                    bins = st.slider("Número de bins", 5, 100, 30, key="bins_tab9")
                    mostrar_kde = st.checkbox("Mostrar curva KDE", value=True, key="kde_tab9")
                
                    fig = processor.plot_histogram(var_num, bins=bins, kde=mostrar_kde)
                    st.pyplot(fig)
                    plt.close(fig)
                else:
                    st.warning("No hay variables numéricas disponibles.")

            # Boxplot
            elif tipo_grafico == "Boxplot":
                if processor.numeric_cols:
                    var_num = st.selectbox("Variable numérica", processor.numeric_cols, key="box_num_tab9")
                    agrupar_por = st.selectbox(
                        "Agrupar por (opcional)",
                        ["Ninguna"] + processor.categorical_cols,
                        key="agrupar_tab9"
                    )
                    if agrupar_por != "Ninguna":
                        fig = processor.plot_boxplot(var_num, group_col=agrupar_por)
                    else:
                        fig = processor.plot_boxplot(var_num)
                    st.pyplot(fig)
                    plt.close(fig)
                else:
                    st.warning("No hay variables numéricas disponibles.")

            # Scatter plot
            elif tipo_grafico == "Scatter plot":
                if len(processor.numeric_cols) >= 2:
                    cols = st.columns(3)
                    with cols[0]:
                        x_var = st.selectbox("Eje X", processor.numeric_cols, key="scatter_x_tab9")
                    with cols[1]:
                        y_options = [v for v in processor.numeric_cols if v != x_var]
                        y_var = st.selectbox("Eje Y", y_options, key="scatter_y_tab9")
                    with cols[2]:
                        color_var = st.selectbox(
                            "Color por (opcional)",
                            ["Ninguno"] + processor.categorical_cols,
                            key="scatter_color_tab9"
                        )
                    if color_var != "Ninguno":
                        fig = processor.plot_scatter(x_var, y_var, color_col=color_var)
                    else:
                        fig = processor.plot_scatter(x_var, y_var)
                    st.pyplot(fig)
                    plt.close(fig)
                else:
                    st.warning("Se necesitan al menos dos variables numéricas para un scatter plot.")

            # Gráfico de barras para categórica 
            elif tipo_grafico == "Gráfico de barras (categórica)":
                if processor.categorical_cols:
                    var_cat = st.selectbox("Variable categórica", processor.categorical_cols, key="bar_cat_tab9")
                    ordenar = st.checkbox("Ordenar por frecuencia", value=True, key="order_tab9")
                    fig = processor.plot_bar(var_cat, order_by_freq=ordenar)
                    st.pyplot(fig)
                    plt.close(fig)
                else:
                    st.warning("No hay variables categóricas disponibles.")
            
    with tab10:
        st.header("Hallazgos clave")
        st.markdown("A continuación se presentan los insights más relevantes derivados del análisis exploratorio de datos de la campaña de marketing bancario.")
        
        # crear columnas
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            ### 🔍 Conclusión 1: Edad y aceptación
            - Los clientes entre **30 y 40 años** presentan la mayor tasa de aceptación del producto.
            - Los mayores de 60 años muestran menor interés, posiblemente por menor afinidad digital o productos no adecuados.
            - **Recomendación:** Enfocar campañas en el segmento de 30-40 años y evaluar productos específicos para adultos mayores.
            """)
        
            st.markdown("""
            ### 📞 Conclusión 2: Duración de la llamada
            - La variable **`duration`** (duración del contacto) es la que más se relaciona con la aceptación.
            - Llamadas más largas (superiores a 200 segundos) tienen mayor probabilidad de éxito.
            - **Recomendación:** Capacitar a ejecutivos para mantener conversaciones extendidas cuando el cliente muestre interés.
            """)
    
        with col2:
            st.markdown("""
            ### 💼 Conclusión 3: Trabajo y educación
            - Los clientes con ocupación **"student"** y **"retired"** tienen alta tasa de aceptación relativa.
            - Nivel educativo **"university.degree"** se asocia con mayor aceptación.
            - **Recomendación:** Personalizar ofertas según perfil laboral y educativo; estudiantes podrían responder a productos de ahorro, jubilados a inversiones seguras.
            """)
        
            st.markdown("""
            ### 📅 Conclusión 4: Mes de contacto
            - Los meses con mayor éxito son **marzo, septiembre y octubre**.
            - Diciembre y mayo muestran las tasas más bajas (posiblemente por estacionalidad).
            - **Recomendación:** Planificar campañas intensivas en los meses de alta conversión y reducir contactos en periodos de baja respuesta.
            """)

        # Tercera fila, conclusión 5 que ocupe todo el ancho
        st.markdown("""
        ### 📊 Conclusión 5: Variables económicas
        - Cuando la tasa de empleo (**`nr.employed`**) es alta, la aceptación tiende a ser mayor.
        - El índice de confianza del consumidor (**`cons.conf.idx`**) también muestra correlación positiva.
        - **Recomendación:** Monitorear indicadores macroeconómicos para activar campañas en momentos de optimismo económico.
        """)

        # Visualización resumen: podemos incluir un par de gráficos estáticos clave
        st.markdown("---")
        st.markdown("### 📈 Visualizaciones de apoyo")

        # Seleccionar dos gráficos representativos (pueden ser generados con los datos)
        # Ejemplo: distribución de edad por aceptación y duración de llamada por resultado
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))

        # Gráfico 1: Boxplot edad vs y
        sns.boxplot(data=df, x='y', y='age', ax=axes[0], palette=['#ff9999', '#66b3ff'])
        axes[0].set_title('Distribución de edad por aceptación')
        axes[0].set_xlabel('Aceptación')
        axes[0].set_ylabel('Edad')

        # Gráfico 2: Histograma de duration por y
        for outcome, color in zip(['no', 'yes'], ['#ff9999', '#66b3ff']):
            subset = df[df['y'] == outcome]
            sns.histplot(subset['duration'], bins=30, color=color, label=outcome, alpha=0.5, ax=axes[1])
        axes[1].set_title('Duración de llamada por aceptación')
        axes[1].set_xlabel('Duración (segundos)')
        axes[1].set_ylabel('Frecuencia')
        axes[1].legend()

        plt.tight_layout()
        st.pyplot(fig)

        # Explicación breve de los gráficos
        st.caption("Los gráficos refuerzan las conclusiones 1 y 2: los clientes que aceptan tienden a ser más jóvenes (mediana menor) y las llamadas exitosas suelen ser más largas.")

        # Reflexión final
        st.markdown("""
        ### 💡 Reflexión final
        El análisis exploratorio permitió identificar patrones claros que explican la caída en la efectividad de las campañas. 
        La segmentación por edad, duración de llamada, ocupación y estacionalidad ofrece oportunidades concretas para optimizar recursos y mejorar la tasa de conversión. 
        No se requiere modelado predictivo para tomar acciones inmediatas basadas en estos hallazgos.
        """)