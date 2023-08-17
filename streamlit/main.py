import streamlit as st
import pandas as pd
import sqlite3
import tempfile

hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)


# Function to display SQLite database table as a dataframe
def display_table(conn, table_name):
    query = f"SELECT * FROM {table_name}"
    df = pd.read_sql(query, conn)
    return df

# Function to update data in the SQLite database
def update_data(conn, table_name, new_data):
    for index, row in new_data.iterrows():
        update_query = f"UPDATE {table_name} SET "
        updates = [f"{col} = ?" for col in new_data.columns]
        update_query += ", ".join(updates)
        update_query += f" WHERE id = ?"
        conn.execute(update_query, [row[col] for col in new_data.columns])
    conn.commit()

# Main function
def main():
    st.title("SQLite Database Editor")
    
    uploaded_file = st.file_uploader("Upload an SQLite database", type=["db"])
    
    if uploaded_file:
        temp_db_file = tempfile.NamedTemporaryFile(delete=False)
        temp_db_file.write(uploaded_file.read())
        temp_db_file.close()

        conn = sqlite3.connect(temp_db_file.name)
        
        table_list = conn.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
        table_names = [table[0] for table in table_list]
        
        selected_table = st.selectbox("Select a table to edit", table_names)
        
        st.write(f"Editing '{selected_table}' table")
        
        table_df = display_table(conn, selected_table)
        st.dataframe(table_df, height=500)
        
        st.write("Edit the table:")
        new_data = pd.DataFrame(columns=table_df.columns)
        for col in table_df.columns:
            if col != "id":
                new_data[col] = st.text_input(f"Enter new {col}", table_df[col].values, key=col)
        new_data["id"] = table_df["id"]
        
        if st.button("Update Data"):
            update_data(conn, selected_table, new_data)
            st.success("Data updated successfully!")
        
        conn.close()

if __name__ == "__main__":
    main()
