import streamlit as st
import xml.etree.ElementTree as ET
from xml.dom import minidom


hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)

import streamlit as st, ast, sqlite3
con=sqlite3.connect('db.db')
cur=con.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS db(name TEXT,  note TEXT)')

if st.button('Add New Row'):
  cur.execute('INSERT INTO db(name, note) VALUES(?,?)', ('',''))
  con.commit()

for row in cur.execute('SELECT rowid, name,  note FROM db ORDER BY name'):
  with st.expander(row[1]):
    with st.form(f'ID-{row[0]}'):
      name=st.text_input('Name', row[1])
      note=st.text_area('Note', row[2])
      if st.form_submit_button('Save'):
        cur.execute(
          'UPDATE db SET name=?, letters=?, note=? WHERE name=?;', 
          (name,  note, str(row[1]))
        )
        con.commit() ; st.experimental_rerun()
      if st.form_submit_button("Delete"):
        cur.execute(f'DELETE FROM db WHERE rowid="{row[0]}";')
        con.commit() ; st.experimental_rerun()


