from django.shortcuts import render, get_object_or_404
from .models import CoverLetter, Optimization
from resumes.models import Resume
import openai
from django.conf import settings  # For accessing environment variables

# Set OpenAI API key from environment variables
openai.api_key = settings.OPENAI_API_KEY

# Helper function for making OpenAI chat requests using GPT-4
def openai_chat_request(messages, model="gpt-4", temperature=0.7, max_tokens=500, top_p=1):
    # Use the correct method for ChatCompletion in openai 1.52.0
    response = openai.ChatCompletion.create(  # Correct API method for chat completion
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p
    )
    return response.choices[0].message['content']  # Return the content of the AI's response
# Generate a cover letter using AI chatbot
def generate_cover_letter(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id)
    
    # Prompt for the AI to generate a cover letter
    prompt = f"""
    Write a professional cover letter based on the following resume:
    {resume.details}
    The cover letter should be formal, concise, and tailored to apply for a job in the same field as the resume.
    """
    
    messages = [
        {"role": "system", "content": "You are a professional assistant who writes cover letters."},
        {"role": "user", "content": prompt}
    ]
    
    # Get AI response for the cover letter
    cover_letter_content = openai_chat_request(messages)
    
    # Save the generated cover letter to the database
    cover_letter = CoverLetter.objects.create(resume=resume, content=cover_letter_content)
    
    return render(request, 'cover_letter.html', {'cover_letter': cover_letter})

# Optimize a resume using AI chatbot
def optimize_resume(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id)
    
    # Prompt for the AI to optimize the resume
    prompt = f"""
    Analyze and suggest improvements for the following resume:
    {resume.details}
    The suggestions should focus on clarity, formatting, and relevance to industry standards.
    """
    
    messages = [
        {"role": "system", "content": "You are a professional assistant who optimizes resumes."},
        {"role": "user", "content": prompt}
    ]
    
    # Get AI response for optimization suggestions
    optimization_suggestions = openai_chat_request(messages)
    
    # Save the suggestions in the database
    optimization = Optimization.objects.create(resume=resume, suggestions=optimization_suggestions)
    
    return render(request, 'optimize_resume.html', {'optimization': optimization})

# Chatbot interaction function
def chatbot_interaction(request):
    if request.method == 'POST':
        user_input = request.POST.get('user_input', '')
        
        # Build the conversation for the chatbot
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_input}
        ]
        
        # Get the AI's response
        ai_response = openai_chat_request(messages)
        
        return render(request, 'chatbot_interaction.html', {'user_input': user_input, 'ai_response': ai_response})
    
    return render(request, 'chatbot_interaction.html')
