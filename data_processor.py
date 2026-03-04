import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

class DataProcessor:
    """
    Clase para procesar y analizar el dataset BankMarketing.
    Encapsula clasificación de variables, estadísticas y visualizaciones.
    """
    
    def __init__(self, df):
        """
        Inicializa el procesador con un DataFrame.
        
        Parameters:
        -----------
        df : pandas.DataFrame
            Datos a analizar
        """
        self.df = df.copy()
        self.numeric_cols = []
        self.categorical_cols = []
        self._classify_variables()
    
    def _classify_variables(self):
        """Clasifica las columnas en numéricas y categóricas (método privado)."""
        self.numeric_cols = self.df.select_dtypes(include=[np.number]).columns.tolist()
        self.categorical_cols = self.df.select_dtypes(include=['object', 'category']).columns.tolist()
    
    # ------------------------------------------------------------
    # Estadísticas descriptivas
    # ------------------------------------------------------------
    def get_descriptive_stats(self, columns=None):
        """
        Retorna estadísticas descriptivas para las columnas numéricas.
        
        Parameters:
        -----------
        columns : list, optional
            Lista de columnas específicas. Si es None, usa todas las numéricas.
        
        Returns:
        --------
        pandas.DataFrame
        """
        if columns is None:
            columns = self.numeric_cols
        return self.df[columns].describe().T
    
    def get_info_dataframe(self):
        """
        Retorna un DataFrame con información general: tipo, nulos, % nulos.
        """
        info = pd.DataFrame({
            'Columna': self.df.columns,
            'Tipo de dato': self.df.dtypes.astype(str),
            'No nulos': self.df.count().values,
            'Nulos': self.df.isnull().sum().values,
            '% Nulos': (self.df.isnull().sum().values / len(self.df) * 100).round(2)
        })
        return info
    
    # ------------------------------------------------------------
    # Visualizaciones
    # ------------------------------------------------------------
    def plot_histogram(self, column, bins=30, kde=False, figsize=(10, 5)):
        """
        Genera un histograma para una columna numérica.
        
        Returns:
        --------
        matplotlib.figure.Figure
        """
        fig, ax = plt.subplots(figsize=figsize)
        sns.histplot(data=self.df, x=column, bins=bins, kde=kde, ax=ax, color='steelblue')
        
        # Líneas de media y mediana
        media = self.df[column].mean()
        mediana = self.df[column].median()
        ax.axvline(media, color='red', linestyle='--', linewidth=2, label=f'Media: {media:.2f}')
        ax.axvline(mediana, color='green', linestyle='-', linewidth=2, label=f'Mediana: {mediana:.2f}')
        ax.legend()
        ax.set_title(f'Distribución de {column}')
        ax.set_xlabel(column)
        ax.set_ylabel('Frecuencia')
        plt.tight_layout()
        return fig
    
    def plot_boxplot(self, column, group_col=None, figsize=(10, 5)):
        """
        Genera un boxplot de una variable numérica, opcionalmente agrupada.
        
        Parameters:
        -----------
        column : str
            Variable numérica
        group_col : str, optional
            Variable categórica para agrupar
        """
        fig, ax = plt.subplots(figsize=figsize)
        if group_col and group_col in self.categorical_cols:
            sns.boxplot(data=self.df, x=group_col, y=column, ax=ax)
            ax.set_title(f'{column} por {group_col}')
            plt.xticks(rotation=45)
        else:
            sns.boxplot(data=self.df, y=column, ax=ax)
            ax.set_title(f'Boxplot de {column}')
        plt.tight_layout()
        return fig
    
    def plot_bar(self, column, relative=False, order_by_freq=True, figsize=(10, 5)):
        """
        Genera un gráfico de barras para una variable categórica.
        
        Parameters:
        -----------
        column : str
            Variable categórica
        relative : bool
            Si True, muestra porcentajes en lugar de frecuencias absolutas
        order_by_freq : bool
            Si True, ordena las barras de mayor a menor frecuencia
        """
        fig, ax = plt.subplots(figsize=figsize)
        
        if relative:
            counts = self.df[column].value_counts(normalize=True) * 100
            ylabel = 'Porcentaje (%)'
        else:
            counts = self.df[column].value_counts()
            ylabel = 'Frecuencia absoluta'
        
        if order_by_freq:
            counts = counts.sort_values(ascending=False)
        
        ax.bar(counts.index.astype(str), counts.values, color='coral', edgecolor='black')
        ax.set_xlabel(column)
        ax.set_ylabel(ylabel)
        ax.set_title(f'Distribución de {column}')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        return fig
    
    def plot_scatter(self, x_col, y_col, color_col=None, figsize=(10, 5)):
        """
        Genera un scatter plot entre dos variables numéricas.
        
        Parameters:
        -----------
        x_col, y_col : str
            Variables numéricas para los ejes
        color_col : str, optional
            Variable categórica para colorear los puntos
        """
        fig, ax = plt.subplots(figsize=figsize)
        if color_col and color_col in self.categorical_cols:
            sns.scatterplot(data=self.df, x=x_col, y=y_col, hue=color_col, ax=ax)
        else:
            sns.scatterplot(data=self.df, x=x_col, y=y_col, ax=ax)
        ax.set_title(f'{x_col} vs {y_col}')
        plt.tight_layout()
        return fig
    
    def plot_contingency(self, col1, col2, stacked=False, figsize=(10, 5)):
        """
        Genera un gráfico de barras para dos variables categóricas.
        
        Parameters:
        -----------
        col1, col2 : str
            Variables categóricas
        stacked : bool
            Si True, barras apiladas al 100%
        """
        fig, ax = plt.subplots(figsize=figsize)
        if stacked:
            # Porcentajes por fila
            ct = pd.crosstab(self.df[col1], self.df[col2], normalize='index') * 100
            ct.plot(kind='bar', stacked=True, ax=ax, colormap='Set2')
            ax.set_ylabel('Porcentaje (%)')
        else:
            ct = pd.crosstab(self.df[col1], self.df[col2])
            ct.plot(kind='bar', ax=ax, colormap='Set2')
            ax.set_ylabel('Frecuencia absoluta')
        ax.set_title(f'Relación entre {col1} y {col2}')
        ax.set_xlabel(col1)
        plt.xticks(rotation=45, ha='right')
        if len(self.df[col2].unique()) > 5:
            plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()
        return fig, ct