import modal
from deepagents import create_deep_agent

from langchain_modal import ModalSandbox

from dotenv import load_dotenv

load_dotenv()

app = modal.App("deepagents-sandbox")

if __name__ == "__main__":
    with app.run():
        modal_sandbox = modal.Sandbox.create(app=app)
        backend = ModalSandbox(sandbox=modal_sandbox)

        agent = create_deep_agent(
            model="google_genai:gemini-2.5-flash",
            system_prompt="You are a coding assistant with sandbox access. You can create and run code in the sandbox.",
            backend=backend,
        )
        try:
            result = agent.invoke(
                {
                    "messages": [
                        {
                            "role": "user",
                            "content": "Install numpy and calculate pi",
                        }
                    ]
                }
            )
            print("=== Result ===")
            print(result["messages"][-1].content)
        finally:
            # Cleanup
            modal_sandbox.terminate()