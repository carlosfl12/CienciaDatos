import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.DataFrame()

def load_dataframe(path):
    global df
    try:
        if path:
            df = pd.read_csv(path)
        else:
            df = pd.read_csv("C:/Users/carlo/Desktop/Urbalab/Proyecto/Meteorite_Landings.csv")

        df.drop(["Unnamed: 10"], axis=1, inplace=True)

        df = df.rename(columns={"name": "Nombre", "nametype": "Clase", "recclass": "Clasificación",
                                "mass (g)": "Masa (g)", "fall" : "Caída", "year": "Año", "reclat": "y", "reclong": "x"})

        # Crear columna hemisferio
        df["Hemisferio"] = df["y"] > 0

        # Cambiar los valores de True y False a Norte y Sur
        df["Hemisferio"] = df["Hemisferio"].map({True: "Norte", False: "Sur"})

        # Eliminar filas que no tienen localización
        df.dropna(subset=["y", "x"], inplace=True)
    
    except Exception as e:
        print(f"Error al leer el archivo: {e}")

# load_dataframe(None)
# Funciones para TKinter
def get_dataframe(): return df

def create_sum(dataframe: pd.DataFrame, x_value: str, qty = 5, ax = "", size=(9, 5) ):
    data = dataframe[x_value].value_counts().reset_index().sort_values(by="count", ascending=False)
    plt.figure(figsize=size)
    sns.barplot(x=data[x_value].head(qty), y=data["count"].head(qty), ax=ax)
    plt.ylabel("Cantidad")
     

def create_group(dataframe: pd.DataFrame, column_name1: str, column_name2: str, by_name: str, qty: int, size=(9, 5)):
    data = dataframe.groupby([column_name1, column_name2])[column_name1].value_counts().reset_index().sort_values(by="count", ascending=False)
    df_filter = data[data[column_name1] == by_name]
    plt.figure(figsize=size)
    sns.barplot(x=df_filter[column_name2].head(qty), y=df_filter["count"].head(qty))
    plt.title(f"{by_name} / {column_name2}")
    plt.ylabel("Cantidad")

def build_bar_by_group(dataframe: pd.DataFrame, column_name1: str, column_name2: str, by_name: str, qty: int, size = (9,5), ax=""):
    data = dataframe.groupby([column_name1, column_name2])[column_name1].value_counts().reset_index().sort_values(by="count", ascending=False)
    df_filter = data[data[column_name2] == by_name]
    create_bar(df_filter, column_name1, by_name, qty, size, ax=ax)


def create_bar(dataframe: pd.DataFrame, column_name: str, by_name: str, qty: int, size=(9, 5), ax=""):
    plt.figure(figsize=size)
    sns.barplot(x=dataframe[column_name].head(qty), y=dataframe["count"].head(qty), ax=ax)
    plt.title(f"{by_name} / {column_name}")
    plt.ylabel("Cantidad")

def get_group(dataframe: pd.DataFrame, column_name1: str, column_name2: str, by_name: str, qty: int, size = (9,5)):
    data = dataframe.groupby([column_name1, column_name2])[column_name1].value_counts().reset_index().sort_values(by="count", ascending=False)
    df_filter = data[data[column_name2] == by_name]
    return df_filter

def get_unique_from_column(dataframe: pd.DataFrame, column_name: str):
    return dataframe[column_name].unique()


def identify_meteorite(dataframe: pd.DataFrame, column1 = "", column2 = "", by_name1 = "", by_name2 = "", size = (9,5), ax = ""):
    plt.figure(figsize=size)
    data = dataframe.loc[(dataframe[column1] == by_name1) & (dataframe[column2] == by_name2)]
    sns.scatterplot(data = data, x= 'x', y= 'y', hue= 'Hemisferio', ax=ax)
    plt.title(f"Ubicación de: {by_name2} / {by_name1}")

