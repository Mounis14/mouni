# certificates/views.py

from django.shortcuts import render
from django.http import HttpResponse
from .forms import CertificateForm  # Import the form you've created
from PIL import Image, ImageDraw, ImageFont
import os
from io import BytesIO

def generate_certificate(name):
    """
    Generates a certificate image with the given name.
    """
    # Paths to your certificate template and font file
    certificate_path = "path/to/your/certificate_template.png"  # Update this path
    font_path = "path/to/your/font.ttf"  # Update this path

    # Open the certificate template image
    img = Image.open(certificate_path).convert("RGB")
    draw = ImageDraw.Draw(img)

    # Load the font
    font = ImageFont.truetype(font_path, 200)  # Set the font size as needed

    # Calculate text position to center the name
    text_width, text_height = draw.textbbox((0, 0), name, font=font)[2:4]
    image_width, image_height = img.size
    text_x_position = (image_width - text_width) / 2  # Center the text
    text_y_position = 700  # Adjust based on your certificate design

    # Draw the name on the certificate
    draw.text((text_x_position, text_y_position), name, font=font, fill="black")

    # Save the certificate to an in-memory file
    buffer = BytesIO()
    img.save(buffer, format="PNG")  # Save as PNG format
    buffer.seek(0)  # Reset the buffer pointer to the beginning

    return buffer

def certificate_view(request):
    """
    View to handle the certificate generation form and display.
    """
    if request.method == "POST":  # Check if the request is a POST
        form = CertificateForm(request.POST)  # Create a form instance with submitted data
        if form.is_valid():  # Validate the form
            name = form.cleaned_data["name"]  # Get the cleaned data (user's name)
            buffer = generate_certificate(name)  # Generate the certificate

            # Return the generated certificate as an image response
            response = HttpResponse(buffer, content_type="image/png")
            response["Content-Disposition"] = f"attachment; filename={name}_certificate.png"
            return response
    else:
        form = CertificateForm()  # If GET, instantiate an empty form

    # Render the form template
    return render(request, "certificates/certificate_form.html", {"form": form})
