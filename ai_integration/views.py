# from django.shortcuts import render, get_object_or_404
# from .models import CoverLetter, Optimization
# from resumes.models import Resume
# import os
# from openai import OpenAI
# from django.conf import settings  # For accessing environment variables
#
# # Initialize OpenAI client
# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
#
# # Helper function for making OpenAI chat requests using the OpenAI Python API
# def openai_chat_request(messages, model="gpt-4", temperature=0.7, max_tokens=500, top_p=1):
#     # Use the OpenAI API's chat completion method
#     response = client.chat.completions.create(
#         model=model,
#         messages=messages,
#         temperature=temperature,
#         max_tokens=max_tokens,
#         top_p=top_p
#     )
#
#     # Correctly access the 'content' attribute from the ChatCompletionMessage object
#     return response.choices[0].message.content
#
# # Generate a cover letter using AI chatbot
# def generate_cover_letter(request, resume_id):
#     resume = get_object_or_404(Resume, id=resume_id)
#
#     # Build a prompt for cover letter generation
#     prompt = f"""
#     Write a professional cover letter based on the following resume:
#     {resume.details}
#     The cover letter should be formal, concise, and tailored to apply for a job in the same field as the resume.
#     """
#
#     messages = [
#         {"role": "system", "content": "You are a professional assistant who writes cover letters."},
#         {"role": "user", "content": prompt}
#     ]
#
#     # Get AI response for the cover letter
#     cover_letter_content = openai_chat_request(messages)
#
#     # Save the generated cover letter in the database
#     cover_letter = CoverLetter.objects.create(resume=resume, content=cover_letter_content)
#
#     return render(request, 'cover_letter.html', {'cover_letter': cover_letter})
#
# # Optimize a resume using AI chatbot
# def optimize_resume(request, resume_id):
#     resume = get_object_or_404(Resume, id=resume_id)
#
#     # Build a prompt for resume optimization
#     prompt = f"""
#     Analyze and suggest improvements for the following resume:
#     {resume.details}
#     The suggestions should focus on clarity, formatting, and relevance to industry standards.
#     """
#
#     messages = [
#         {"role": "system", "content": "You are a professional assistant who optimizes resumes."},
#         {"role": "user", "content": prompt}
#     ]
#
#     # Get AI response for optimization suggestions
#     optimization_suggestions = openai_chat_request(messages)
#
#     # Save the suggestions in the database
#     optimization = Optimization.objects.create(resume=resume, suggestions=optimization_suggestions)
#
#     return render(request, 'optimize_resume.html', {'optimization': optimization})
#
# # Chatbot interaction function
# def chatbot_interaction(request):
#     if request.method == 'POST':
#         user_input = request.POST.get('user_input', '')
#
#         # Build the conversation messages for the chatbot
#         messages = [
#             {"role": "system", "content": "You are a helpful assistant."},
#             {"role": "user", "content": user_input}
#         ]
#
#         # Get the AI's response
#         ai_response = openai_chat_request(messages)
#
#         return render(request, 'chatbot_interaction.html', {'user_input': user_input, 'ai_response': ai_response})
#
#     return render(request, 'chatbot_interaction.html')
