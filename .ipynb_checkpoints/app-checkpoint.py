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
        "Data Analysis of FP Social Media Post "
        "[source code](https://github.com/janetcheung-byte/data_app). "
    )
    st.sidebar.title("About")
    st.sidebar.info(
        """
        This app is maintained by Janet Cheung.
"""
    )


if __name__ == "__main__":
    main()
 
    