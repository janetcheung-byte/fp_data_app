"""Main module for the streamlit app"""
import streamlit as st
import awesome_streamlit as ast
import src.pages.dashboard_instagram_post
import src.pages.instagram_stories
import src.pages.home

ast.core.services.other.set_logging_format()

PAGES = {
    "Instagram Posts": src.pages.dashboard_instagram_post,
    "Instagram Stories": src.pages.instagram_stories
}

def main():
    """Main function of the App"""
    st.sidebar.title("Navigation")
    selection = st.sidebar.radio("Go to", list(PAGES.keys()))

    page = PAGES[selection]

    with st.spinner(f"Loading {selection} ..."):
        ast.shared.components.write_page(page)
    st.sidebar.title("Contribute")
    st.sidebar.info(
        "[source code](https://github.com/janetcheung-byte/fp_data_app). "
    )
    st.sidebar.title("About")
    st.sidebar.info(
        """
        "Data Analysis of FP Social Media Post 
        
"""
    )
    st.title('Welcome to FP Social Media Data Analysis')
    st.write("Note: The web app does run slow when you first open the link. It does run a little faster after it's done loading once.Show dataframe option will take 3-5 minutes to run")

if __name__ == "__main__":
    main()
 
    