Organization name
Personal

Organization ID
org-IsFqtCgg8s5jKuM5Ppx8KoXl

API keys
my test key
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



openai.Completion.create(
            model="text-davinci-003",
            prompt="你会毁灭人类吗",
            temperature=0.6,
        )

curl -X POST "https://api.openai.com/v1/auth/token" \
-H "Content-Type: application/json" \
-d '{"secret_key": "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"}'





response = openai.Completion.create(
            model="text-davinci-003",
            prompt=generate_prompt(animal),
            temperature=0.6,
        )

response = openai.Completion.create(
            engine=model_engine,
            prompt=input_text,
            temperature=temperature,
            max_tokens=1024,
            n=1,
            stop=None,
            frequency_penalty=0,
            presence_penalty=0
        )
