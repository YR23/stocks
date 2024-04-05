import streamlit as st
import cv2
from streamlit_option_menu import option_menu
from screener import get_warren_screening
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap


def main():
    st.title("Simple Streamlit Example")

    selected2 = option_menu(None, ["Income Statement", "Balance Sheet", "Cash Flow"],
                            icons=['currency-dollar', 'bank', "piggy-bank"],
                            menu_icon="cast", default_index=0, orientation="horizontal")
    st.write(selected2)
    with st.spinner('Evaluating Warrent Buffet Screener'):
        df = get_warren_screening()

    # Heatmap with custom colormap
    cols = [col for col in df.columns if "score" in col]
    df_best = df.sort_values(by='total_score', ascending=False).iloc[:15]
    df_best.index = df_best["ticker"]
    total_color = "navy"
    plot = sns.heatmap(df_best[cols], annot=True, cmap=ListedColormap(
        ['skyblue', 'skyblue', 'mediumaquamarine', 'mediumaquamarine', 'green', 'green', total_color, total_color,
         total_color, total_color, total_color, total_color, total_color, total_color, total_color, total_color,
         total_color, total_color, total_color]), cbar=True)

    # Display the plot in Streamlit
    st.pyplot(plot.get_figure())

    with st.expander("Full Dataframe"):
        st.dataframe(df)


if __name__ == "__main__":
    main()
