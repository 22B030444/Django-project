from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

def generate_pdf(request, template_name):
    """
    Generate a PDF file based on the provided HTML template and dynamic context.
    """
    # Extract data dynamically from the request or use defaults for demonstration
    context = {
        'name': request.GET.get('name', 'John Doe'),
        'email': request.GET.get('email', 'john.doe@example.com'),
        'skills': request.GET.getlist('skills', ['Python', 'Django', 'Machine Learning']),
        'experience': request.GET.getlist('experience', [
            'Software Engineer at ABC Corp',
            'Intern at XYZ Inc.'
        ]),
        'education': request.GET.getlist('education', [
            'BSc in Computer Science, MIT',
            'MSc in AI, Stanford'
        ]),
        # Additional fields can be added dynamically
    }

    # Load the specified template
    template = get_template(f'pdf_templates/{template_name}')
    html_content = template.render(context)

    # Generate PDF response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{template_name.split(".")[0]}.pdf"'

    # Generate PDF with xhtml2pdf
    pisa_status = pisa.CreatePDF(html_content, dest=response)
    if pisa_status.err:
        return HttpResponse('Error generating PDF', status=500)
    return response
