# from groq import Groq
# import os
# from mistralai import Mistral

# #Grop api
# client = Groq(
#     api_key=('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'),
# )
# mensaje = "Quien es el presidente actual de mexico"
# chat_completion = client.chat.completions.create(
#     messages=[
#         {
#             "role": "user",
#             "content": f"{mensaje}",
#         }
#     ],
#     model="llama-3.1-70b-versatile",
# )

# print(chat_completion.choices[0].message.content)




# #Mistral api
# api_key = "KhhF4A1wnkver9QUrSYAKimi15RKidXa"
# model = "mistral-large-2407"

# client = Mistral(api_key=api_key)

# chat_response = client.chat.complete(
#     model = model,
#     messages = [
#         {
#             "role": "user",
#             "content": "entiendes español?",
#         },
#     ]
# )

# print(chat_response.choices[0].message.content)


# import requests

# import requests

# url = "https://api.x.ai/v1/chat/completions"
# headers = {
#     "Content-Type": "application/json",
#     "Authorization": "Bearer xai-EVI5UJFng97w6DK2BEMh6uEh4UGeGbiWLn9jPxp3Utk61cNKyvSqwexS4VMuFDKAdaIjDNq3dngQgkxw"
# }
# data = {
#     "messages": [
#         {
#             "role": "system",
#             "content": "You are a test assistant."
#         },
#         {
#             "role": "user",
#             "content": "hola"
#         }
#     ],
#     "model": "grok-beta",
#     "stream": False,
#     "temperature": 0
# }

# response = requests.post(url, headers=headers, json=data)

# if response.status_code == 200:
#     content = response.json()["choices"][0]["message"]["content"]
#     print(content)  # Imprime solo el campo content
# else:
#     print(f"Error {response.status_code}: {response.text}")
