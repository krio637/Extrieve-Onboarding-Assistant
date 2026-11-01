
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, AIMessage


class Assistant:

    def __init__(
        self,
        system_prompt,
        llm,
        message_history=None,
        vector_store=None,
        employee_information=None,
    ):

        self.system_prompt = system_prompt
        self.llm = llm

        self.messages = (
            message_history if message_history is not None else []
        )

        self.vector_store = vector_store
        self.employee_information = employee_information

        self.chain = self._get_conversation_chain()

    # Convert chat history into LangChain message objects
    def format_history(self):

        history = []

        for message in self.messages:

            if message["role"] in ["user", "human"]:
                history.append(
                    HumanMessage(content=message["content"])
                )

            elif message["role"] in ["ai", "assistant"]:
                history.append(
                    AIMessage(content=message["content"])
                )

        return history

    # Generate response
    def get_response(self, user_input):

        return self.chain.stream({
            "user_input": user_input
        })

    # Build RAG conversation chain
    def _get_conversation_chain(self):

        prompt = ChatPromptTemplate.from_messages([

            ("system", self.system_prompt),

            MessagesPlaceholder(
                variable_name="conversation_history"
            ),

            ("human", "{user_input}"),

        ])

        # Format retrieved documents
        def format_docs(docs):

            if not docs:
                return "No relevant company information was found."

            return "\n\n".join(
                doc.page_content for doc in docs
            )

        # Retrieve company policy information
        def retrieve_policy_information(inputs):

            if self.vector_store is None:
                return "Company knowledge base is unavailable."

            retriever = self.vector_store.as_retriever(
                search_kwargs={"k": 4}
            )

            docs = retriever.invoke(
                inputs["user_input"]
            )

            return format_docs(docs)

        # Create chain
        chain = (

            {
                "retrieved_policy_information":
                    retrieve_policy_information,

                "employee_information":
                    lambda x: str(self.employee_information),

                "user_input":
                    lambda x: x["user_input"],

                "conversation_history":
                    lambda x: self.format_history(),
            }

            | prompt
            | self.llm
            | StrOutputParser()

        )

        return chain
