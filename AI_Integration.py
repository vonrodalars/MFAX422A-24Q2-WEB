import time
from openai import OpenAI

client = OpenAI()

assistant = client.beta.assistants.retrieve("asst_qCZJ7MU6b2arw4CQYD8b863C")
thread = client.beta.threads.create()


def get_category(complaint="Problem mit Toaster"):

    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=complaint,
    )

    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id,
    )

    while True:
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)

        if run.status == "completed":
            messages = client.beta.threads.messages.list(thread_id=thread.id)

            return messages.data[0].content[0].text.value
        else:
            time.sleep(2)
