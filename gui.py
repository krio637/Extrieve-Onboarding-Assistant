
import streamlit as st

from prompts import WELCOME_MESSAGE


class AssistantGUI:

    def __init__(self, assistant):
        self.assistant = assistant
        self.messages = assistant.messages
        self.employee_information = assistant.employee_information

        self.logo_url = (
            "https://raw.githubusercontent.com/"
            "ExtrieveTechnologies/.github/main/Extrievelogo.png"
        )

    # ==========================================
    # EMPLOYEE INFORMATION
    # ==========================================

    def get_employee_value(self, key, default="Not available"):

        if isinstance(self.employee_information, dict):
            return self.employee_information.get(key, default)

        return getattr(self.employee_information, key, default)

    def render_employee_information(self):

        employee = self.employee_information

        name = self.get_employee_value("name")
        lastname = self.get_employee_value("lastname", "")

        full_name = f"{name} {lastname}".strip()

        st.markdown(f"### {full_name}")

        st.caption(
            self.get_employee_value("position")
        )

        st.divider()

        employee_fields = {
            "Employee ID": "employee_id",
            "Department": "department",
            "Location": "location",
            "Supervisor": "supervisor",
            "Hire Date": "hire_date",
        }

        for label, key in employee_fields.items():

            value = self.get_employee_value(key)

            st.markdown(f"**{label}**")
            st.caption(str(value))

        # Employee Skills
        st.divider()

        st.markdown("**Skills**")

        skills = self.get_employee_value("skills", [])

        if skills:

            for skill in skills:
                st.markdown(f"- {skill}")

        else:
            st.caption("No skills available.")

    # ==========================================
    # CHAT RESPONSE
    # ==========================================

    def get_response(self, user_input):
        return self.assistant.get_response(user_input)

    # ==========================================
    # RENDER CHAT HISTORY
    # ==========================================

    def render_messages(self):

        for message in self.messages:

            if message["role"] == "user":
                role = "user"

            elif message["role"] in ["ai", "assistant"]:
                role = "assistant"

            else:
                continue

            with st.chat_message(role):
                st.markdown(message["content"])

    # ==========================================
    # SESSION STATE
    # ==========================================

    def set_state(self, key, value):
        st.session_state[key] = value

    # ==========================================
    # USER CHAT INPUT
    # ==========================================

    def render_user_input(self):

        user_input = st.chat_input(
            "Ask something about Extrieve...",
            key="input"
        )

        if user_input:

            # Display user message
            st.chat_message("user").markdown(user_input)

            # Save user message
            self.messages.append({
                "role": "user",
                "content": user_input
            })

            # Generate AI response
            with st.chat_message("assistant"):

                response_placeholder = st.empty()
                full_response = ""

                try:

                    response_generator = self.get_response(user_input)

                    for chunk in response_generator:

                        full_response += chunk

                        response_placeholder.markdown(
                            full_response + "▌"
                        )

                    response_placeholder.markdown(full_response)

                    # Save AI response
                    self.messages.append({
                        "role": "ai",
                        "content": full_response
                    })

                except Exception as e:

                    st.error(
                        f"Error generating response: {str(e)}"
                    )

            self.set_state("messages", self.messages)

    # ==========================================
    # SIDEBAR
    # ==========================================

    def render_sidebar(self):

        with st.sidebar:

            # Company Logo
            st.image(
                self.logo_url,
                width=220
            )

            st.divider()

            st.subheader("Employee Profile")

            self.render_employee_information()

            st.divider()

            # Clear Chat
            if st.button(
                "Clear Chat",
                use_container_width=True,
                type="secondary"
            ):

                self.messages.clear()

                self.messages.append({
                    "role": "ai",
                    "content": WELCOME_MESSAGE
                })

                self.set_state("messages", self.messages)

                st.rerun()

    # ==========================================
    # MAIN CHAT INTERFACE
    # ==========================================

    def render_main_content(self):

        st.title("Extrieve Onboarding Assistant")

        st.caption(
            "Your assistant for company policies, employee onboarding, "
            "training, products, and HR processes."
        )

        st.divider()

        self.render_messages()

        self.render_user_input()

    # ==========================================
    # MAIN RENDER FUNCTION
    # ==========================================

    def render(self):

        self.render_sidebar()

        self.render_main_content()
