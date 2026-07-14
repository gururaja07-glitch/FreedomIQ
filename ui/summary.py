import streamlit as st


def show_summary(summary):

    st.divider()

    st.subheader("📊 Portfolio Summary")

    left, right = st.columns(2)

    with left:

        st.write(f'**Number of Stocks:** {summary["Number of Stocks"]}')
        st.write(f'**Number of Sectors:** {summary["Number of Sectors"]}')
        st.write(f'**Largest Holding:** {summary["Largest Holding"]}')

    with right:

        st.write(f'**Largest Weight:** {summary["Largest Weight"]:.2f}%')
        st.write(f'**Cash Weight:** {summary["Cash Weight"]:.2f}%')
        st.write(f'**Gold Weight:** {summary["Gold Weight"]:.2f}%')