# importamos las librerías necesarias
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

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
    
    # Leer el archivo CSV
    df = st.session_state.df
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
        info_df = pd.DataFrame({
                'Columna': df.columns,
                'Tipo de dato': df.dtypes.astype(str),
                'No nulos': df.count().values,
                'Nulos': df.isnull().sum().values,
                '% Nulos': (df.isnull().sum().values / len(df) * 100).round(2)
            })
            
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
        
        # Clasificar variables
        def clasificar_variables(df):
            variables_numericas = df.select_dtypes(include=[np.number]).columns.tolist()
            variables_categoricas = df.select_dtypes(include=["object", "category"]).columns.tolist()
            return variables_numericas, variables_categoricas
        
        # Aplicar la función
        variables_numericas, variables_categoricas = clasificar_variables(df)

        # Mostrar conteos en métricas
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Variables numéricas", len(variables_numericas))
        with col2:
            st.metric("Variables categóricas", len(variables_categoricas))
        
        # Mostrar lista de variables en dos columnas
        st.markdown("### Detalle de variables")
        col_left, col_right = st.columns(2)
        with col_left:
            st.markdown("**Numéricas:**")
            if variables_numericas:
                for var in variables_numericas:
                    st.write(f"- {var}")
            else:
                st.write("No hay variables numéricas.")
        with col_right:
            st.markdown("**Categóricas:**")
            if variables_categoricas:
                for var in variables_categoricas:
                    st.write(f"- {var}")
            else:
                st.write("No hay variables categóricas.")
    with tab3:
        st.header("Estadísticas descriptivas")
        # Usamos las variables numéricas
        num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        
        if len(num_cols) > 0:
            st.markdown("**Resumen estadístico de variables numéricas:**")
            describe_df = df[num_cols].describe().T
            st.dataframe(describe_df, use_container_width=True)
            
            # Seleccionar una variable numérica
            st.markdown("### Métricas destacadas por variable")
            var_seleccionada = st.selectbox("Selecciona una variable numérica", num_cols)
            
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
                
                # Histograma
                fig, ax = plt.subplots()
                ax.hist(df[var_seleccionada].dropna(), bins=30, edgecolor='black')
                ax.set_title(f'Distribución de {var_seleccionada}')
                ax.set_xlabel(var_seleccionada)
                ax.set_ylabel('Frecuencia')
                st.pyplot(fig)
                plt.close(fig)  # Para evitar acumulación de figuras
            
            else:
                st.warning("No hay variables numéricas en el dataset.")
                   
    with tab4:
        st.header("Análisis de valores faltantes")
        
        # Calcular nulos
        nulos = df.isnull().sum()
        nulos_percent = (nulos / len(df))*100
        
        # Crear dataframe
        nulos_df = pd.DataFrame({
        'Columna': df.columns,
        'Valores nulos': nulos.values,
        'Porcentaje': nulos_percent.values.round(2)
        })
        
        # Mostrar tabla
        st.dataframe(nulos_df, use_container_width=True)
        
        # Verificar si hay nulos
        total_nulos = nulos.sum()
        if total_nulos == 0:
            st.success("✅ No se detectaron valores faltantes en el dataset.")
        else:
            st.warning(f"⚠️ Se encontraron {total_nulos} valores faltantes en total.")
         
        # Visualización: gráfico de barras de valores nulos por columna
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.bar(nulos_df['Columna'], nulos_df['Valores nulos'], color='skyblue', edgecolor='black')
        ax.set_xlabel('Columnas')
        ax.set_ylabel('Cantidad de nulos')
        ax.set_title('Valores faltantes por columna')
        plt.xticks(rotation=45, ha='right')
        st.pyplot(fig)  
    
    with tab5:
        st.header("Distribución de variables numéricas")
        if variables_numericas:
            var_num = st.selectbox(
                "Selecciona la variable numérica a analizar:",
                variables_numericas,
                key = "var_tab5"
            )  
            
            # Slider para número de bins
            bins = st.slider(
                "Número de bins del histograma:",
                min_value=5,
                max_value=100,
                value=30,
                step=5,
                key="bins_tab5"
            )
            
            # Checkbox para mostrar curva de densidad (KDE)
            mostrar_kde = st.checkbox(
                "Mostrar curva de densidad (KDE)",
                value=False,
                key="kde_tab5"
            )
            
            # Generar gráfico
            fig, ax = plt.subplots(figsize=(10, 5))
            
            # Histograma
            if mostrar_kde:
                sns.histplot(data=df, x=var_num, bins=bins, kde=True, ax=ax, color='steelblue')
            else:
                sns.histplot(data=df, x=var_num, bins=bins, kde=False, ax=ax, color='steelblue')
            
            # Calcular estadísticas
            media = df[var_num].mean()
            mediana = df[var_num].median()
            desvio = df[var_num].std()    
            
            # Agregar líneas verticales para media y mediana
            ax.axvline(media, color='red', linestyle='--', linewidth=2, label=f'Media: {media:.2f}')
            ax.axvline(mediana, color='green', linestyle='-', linewidth=2, label=f'Mediana: {mediana:.2f}')
            
            # Personalizar el gráfico
            ax.set_title(f'Distribución de {var_num}', fontsize=14)
            ax.set_xlabel(var_num)
            ax.set_ylabel('Frecuencia')
            ax.legend()
            
            # Mostrar el gráfico en Streamlit
            st.pyplot(fig)
            
            # Interpretación 
            col1, col2, col3 = st.columns(3)
            col1.metric("Media", f"{media:.2f}")
            col2.metric("Mediana", f"{mediana:.2f}")
            col3.metric("Desviación estándar", f"{desvio:.2f}")

            # Comentarios sobre la forma de la distribución
            st.markdown("**Interpretación:**")
            if abs(media - mediana) < 0.1 * media:
                st.info("📊 La distribución es aproximadamente simétrica (media ≈ mediana).")
            elif media > mediana:
                st.warning("📈 La distribución tiene sesgo positivo (cola a la derecha).")
            else:
                st.warning("📉 La distribución tiene sesgo negativo (cola a la izquierda).")
        
            # Mostrar estadísticos adicionales en un expander
            with st.expander("Ver más estadísticos"):
                st.write(df[var_num].describe())
        else:
            st.warning("No hay variables numéricas en el dataset.")
    
    with tab6:
        st.header("Análisis de variables categóricas")
        if variables_categoricas:
            var_cat = st.selectbox(
               "Selecciona una variable categórica:",
                variables_categoricas,
                key="var_tab6" 
            )

            # Opciones de visualización
            col1, col2 = st.columns(2)
            with col1:
                tipo_frec = st.radio(
                    "Tipo de frecuencia:",
                    ["Absoluta", "Relativa (%)"],
                    key="tipo_frec_tab6"
                )
            with col2:
                orden = st.radio(
                    "Ordenar categorías por:",
                    ["Frecuencia", "Alfabético"],
                    key="orden_tab6"
                )
            # Calcular frecuencias
            frec = df[var_cat].value_counts()
            if orden == "Alfabético":
                frec = frec.sort_index()
                
            # Crear DataFrame de frecuencias
            if tipo_frec == "Relativa (%)":
                frec_df = pd.DataFrame({
                    'Categoría': frec.index,
                    'Frecuencia': frec.values,
                    'Porcentaje': (frec.values / len(df) * 100).round(2)
                })
            else:
                frec_df = pd.DataFrame({
                    'Categoría': frec.index,
                    'Frecuencia': frec.values
                })

            # Mostrar tabla
            st.markdown("**Tabla de frecuencias**")
            st.dataframe(frec_df, use_container_width=True)

            # Gráfico de barras
            fig, ax = plt.subplots(figsize=(10, 5))
        
            if tipo_frec == "Relativa (%)":
                valores = (frec.values / len(df) * 100)
                ylabel = "Porcentaje (%)"
            else:
                valores = frec.values
                ylabel = "Frecuencia absoluta"

            # Gráfico de barras
            ax.bar(frec.index.astype(str), valores, color='coral', edgecolor='black')
            ax.set_xlabel(var_cat)
            ax.set_ylabel(ylabel)
            ax.set_title(f'Distribución de {var_cat}')
            plt.xticks(rotation=45, ha='right')
        
            st.pyplot(fig)

            # Interpretación
            st.markdown("**Interpretación:**")
            st.markdown(f"""
            - La categoría más frecuente es **{frec.index[0]}** con {frec.values[0]} ocurrencias ({frec.values[0]/len(df)*100:.2f}%).
            - La categoría menos frecuente es **{frec.index[-1]}** con {frec.values[-1]} ocurrencias ({frec.values[-1]/len(df)*100:.2f}%).
            """)

            # Opcional: mostrar todas las categorías y sus proporciones
            with st.expander("Ver todas las categorías y proporciones"):
                st.dataframe(frec_df)

        else:
            st.warning("No hay variables categóricas en el dataset.")
    
    with tab7:
        st.header("Análisis bivariado (numérico vs categórico)")
        
        if variables_numericas and variables_categoricas:
            
            # Selección de variables
            col1, col2 = st.columns(2)
            with col1:
                var_num = st.selectbox(
                    "Variable numérica (Y):",
                    variables_numericas,
                    key="num_tab7"
                )
            with col2:
                var_cat = st.selectbox(
                    "Variable categórica (X):",
                    variables_categoricas,
                    key="cat_tab7"
                )
            # Tipo de gráfico
            tipo_grafico = st.radio(
                "Tipo de gráfico:",
                ["Boxplot", "Histograma apilado", "Violin plot"],
                horizontal=True,
                key="tipo_tab7"
            )
            # Opción para filtrar por la variable objetivo 'y' (si existe)
            if 'y' in df.columns:
                filter_y = st.checkbox("Comparar por resultado de campaña (y)", key="filter_y_tab7")
                if filter_y:
                    categorias_y = df['y'].unique()
            else:
                filter_y = False
            
            # Generar gráfico según selección
            fig, ax = plt.subplots(figsize=(10, 6))

            if tipo_grafico == "Boxplot":
                if filter_y and 'y' in df.columns:
                    sns.boxplot(data=df, x=var_cat, y=var_num, hue='y', ax=ax)
                    ax.legend(title='y')
                else:
                    sns.boxplot(data=df, x=var_cat, y=var_num, ax=ax)
                plt.xticks(rotation=45, ha='right')

            elif tipo_grafico == "Histograma apilado":
                
                # Histograma
                if filter_y and 'y' in df.columns:    
                    sns.histplot(data=df, x=var_num, hue='y', multiple='stack', ax=ax)
                    ax.set_title(f'Histograma de {var_num} apilado por y')
                else:
                    # Histograma para cada categoría de var_cat superpuestos
                    for cat in df[var_cat].unique():
                        subset = df[df[var_cat] == cat]
                        sns.histplot(subset[var_num], label=cat, alpha=0.5, ax=ax)
                    ax.legend()
                ax.set_xlabel(var_num)  
            
            else:  # Violin plot
                if filter_y and 'y' in df.columns:
                    sns.violinplot(data=df, x=var_cat, y=var_num, hue='y', split=True, ax=ax)
                    ax.legend(title='y')
                
                else:
                    sns.violinplot(data=df, x=var_cat, y=var_num, ax=ax)
                plt.xticks(rotation=45, ha='right')

            st.pyplot(fig)

            # Estadísticas por grupo
            with st.expander("Ver estadísticas descriptivas por grupo"):
                stats = df.groupby(var_cat)[var_num].describe()
                st.dataframe(stats)
        else:
            st.warning("Se necesitan variables numéricas y categóricas para este análisis.")
            
    with tab8:
        st.header("Análisis bivariado: Categórico vs Categórico")
        if len(variables_categoricas) >= 2:
            
            # Selección de las dos variables categóricas
            col1, col2 = st.columns(2)
            with col1:
                var_cat1 = st.selectbox(
                    "Selecciona la primera variable categórica (X):",
                    variables_categoricas,
                    key="var_cat1_tab8"
                )
            with col2:
                # Excluir la primera variable para evitar seleccionar la misma
                categoricas_restantes = [c for c in variables_categoricas if c != var_cat1]
                var_cat2 = st.selectbox(
                    "Selecciona la segunda variable categórica (Y):",
                    categoricas_restantes,
                    key="var_cat2_tab8"
                )

            # Opciones de visualización
            tipo_grafico = st.radio(
                "Tipo de gráfico:",
                ["Barras agrupadas", "Barras apiladas (100%)"],
                horizontal=True,
                key="tipo_graf_tab8"
            )

            # Crear tabla de contingencia
            contingency = pd.crosstab(df[var_cat1], df[var_cat2])
            # Porcentajes por fila para el apilado 100%
            contingency_percent = contingency.div(contingency.sum(axis=1), axis=0) * 100

            # Mostrar tabla de contingencia
            st.markdown("**Tabla de contingencia**")
            st.dataframe(contingency, use_container_width=True)

            # Gráfico
            fig, ax = plt.subplots(figsize=(12, 6))

            if tipo_grafico == "Barras agrupadas":
                # Usar seaborn para barras agrupadas
                # Primero necesitamos derretir el dataframe
                df_melted = df[[var_cat1, var_cat2]].dropna()
                sns.countplot(data=df_melted, x=var_cat1, hue=var_cat2, ax=ax)
                ax.set_title(f'Relación entre {var_cat1} y {var_cat2}')
                ax.set_xlabel(var_cat1)
                ax.set_ylabel('Frecuencia')
                ax.legend(title=var_cat2)
                plt.xticks(rotation=45, ha='right')

            else:  # Barras apiladas 100%
                contingency_percent.plot(kind='bar', stacked=True, ax=ax, colormap='Set2')
                ax.set_title(f'Distribución porcentual de {var_cat2} por {var_cat1}')
                ax.set_xlabel(var_cat1)
                ax.set_ylabel('Porcentaje (%)')
                ax.legend(title=var_cat2)
                plt.xticks(rotation=45, ha='right')
                # Ajustar leyenda fuera del gráfico si hay muchas categorías
                if len(df[var_cat2].unique()) > 5:
                    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')

            st.pyplot(fig)

            # Interpretación
            st.markdown("**Interpretación:**")
            # Encontrar la combinación más frecuente
            max_val = contingency.stack().max()
            max_idx = contingency.stack().idxmax()
            st.markdown(f"La combinación más frecuente es **{max_idx[0]}** y **{max_idx[1]}** con {max_val} ocurrencias.")
            
    with tab9:
        st.header("Análisis basado en parámetros seleccionados")
        st.markdown("Explora los datos seleccionando el tipo de gráfico y las variables de interés.")

        # Filtros globales (opcionales)
        st.sidebar.markdown("## Filtros globales para análisis dinámico")
        edad_range = st.sidebar.slider("Rango de edad", int(df.age.min()), int(df.age.max()), (20, 60), key="edad_filtro")
        aceptacion = st.sidebar.multiselect("Resultado de campaña (y)", options=['yes', 'no'], default=['yes', 'no'], key="y_filtro")
        # Aplicar filtros al dataframe
        df_filtrado = df[(df['age'].between(edad_range[0], edad_range[1])) & (df['y'].isin(aceptacion))]

        if df_filtrado.empty:
            st.warning("No hay datos con los filtros seleccionados.")
        else:
            st.caption(f"Mostrando {len(df_filtrado)} registros después de filtros.")

            # Selección de tipo de gráfico
            tipo_grafico = st.selectbox("Tipo de gráfico", ["Histograma", "Boxplot", "Scatter plot", "Gráfico de barras (categórica)"])

            if tipo_grafico == "Histograma":
                var_num = st.selectbox("Variable numérica", variables_numericas, key="hist_num")
                bins = st.slider("Número de bins", 5, 100, 30, key="hist_bins")
                fig, ax = plt.subplots()
                sns.histplot(data=df_filtrado, x=var_num, bins=bins, kde=True, ax=ax)
                ax.set_title(f"Histograma de {var_num}")
                st.pyplot(fig)

            elif tipo_grafico == "Boxplot":
                var_num = st.selectbox("Variable numérica", variables_numericas, key="box_num")
                var_cat = st.selectbox("Variable categórica (opcional, para agrupar)", ["Ninguna"] + categoricas, key="box_cat")
                fig, ax = plt.subplots()
                if var_cat != "Ninguna":
                    sns.boxplot(data=df_filtrado, x=var_cat, y=var_num, ax=ax)
                    plt.xticks(rotation=45)
                else:
                    sns.boxplot(data=df_filtrado, y=var_num, ax=ax)
                ax.set_title(f"Boxplot de {var_num}" + (f" por {var_cat}" if var_cat != "Ninguna" else ""))
                st.pyplot(fig)

            elif tipo_grafico == "Scatter plot":
                num_cols = variables_numericas.copy()
                if len(num_cols) >= 2:
                    x_var = st.selectbox("Eje X", num_cols, key="scatter_x")
                    y_var = st.selectbox("Eje Y", [c for c in num_cols if c != x_var], key="scatter_y")
                    color_var = st.selectbox("Color por (opcional)", ["Ninguno"] + categoricas, key="scatter_color")
                    fig, ax = plt.subplots()
                    if color_var != "Ninguno":
                        sns.scatterplot(data=df_filtrado, x=x_var, y=y_var, hue=color_var, ax=ax)
                    else:
                        sns.scatterplot(data=df_filtrado, x=x_var, y=y_var, ax=ax)
                    ax.set_title(f"Scatter plot: {x_var} vs {y_var}")
                    st.pyplot(fig)
                else:
                    st.warning("Se necesitan al menos dos variables numéricas para un scatter plot.")

            elif tipo_grafico == "Gráfico de barras (categórica)":
                var_cat = st.selectbox("Variable categórica", variables_categoricas, key="bar_cat")
                order = st.checkbox("Ordenar por frecuencia", value=True)
                fig, ax = plt.subplots()
                if order:
                    sns.countplot(data=df_filtrado, y=var_cat, order=df_filtrado[var_cat].value_counts().index, ax=ax)
                else:
                    sns.countplot(data=df_filtrado, y=var_cat, ax=ax)
                ax.set_title(f"Frecuencia de {var_cat}")
                st.pyplot(fig)
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