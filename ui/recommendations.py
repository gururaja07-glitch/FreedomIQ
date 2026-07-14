import streamlit as st


def show_recommendations(actions):

    st.divider()

    st.subheader("📌 Today's Recommendations")

    if not actions:

        st.success("✅ Your portfolio is well balanced.")

    else:

        for action in actions:

            st.warning(
                f"""
**{action["Type"]} : {action["Name"]}**

Current Weight : **{action["Current Weight"]:.2f}%**

Target Weight : **{action["Target Weight"]:.2f}%**

Excess : **{action["Excess"]:.2f}%**
"""
            )