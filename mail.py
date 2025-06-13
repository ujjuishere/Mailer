import smtplib
import pandas as pd
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import mimetypes
import os
import time 

# Zoho SMTP settings
smtp_server = 'smtppro.zoho.in'
port = 587  # Use port 587 for TLS
sender_email = 'pmshri@myaimate.com'  # Replace with your Zoho email
password = 'Pmshri@12'  # Replace with your app-specific password

def send_email(recipient_email, school_name, recipient_district, recipient_state, brochure_link):
    
    try:
        # Create the email content
        subject = "Call for Action: PM SHRI Services & ATL Infrastructure"
        body = f"""
        <html>
        <body>
        <p>To <br> The Principal</p>
        {school_name} <br>
        {recipient_district} <br>
        {recipient_state} <br>
        <p>I hope this email finds you well. At myAImate, led by innovators from IIT Bombay and AIT Pune, we are revolutionizing education through skill-based learning and cutting-edge solutions, fully aligned with NEP 2020 and the PM SHRI Yojana.</p>

        <p><strong>Key Offerings:</strong></p>
        <ul>
            <li><strong>Aptitude Tests for Career Counseling:</strong> Help students make informed career decisions with aptitude quizzes and career seminars tailored to various fields.</li>
            <li><strong>Skill Development & Vocational Courses:</strong> Equip students with future-ready skills in entrepreneurship, IT, AI, Machine Learning, Cybersecurity, and more.</li>
            <li><strong>Seminars for Career Awareness & Guidance:</strong> Inspire students with seminars on competitive exams, career exploration, and motivational talks by experts.</li>
            <li><strong>Project-Based Learning & Competitions:</strong> Foster hands-on learning through real-world projects, hackathons, and competitions to build problem-solving skills.</li>
            <li><strong>Teacher/Administrator Consultation & Training Programs:</strong> Provide expert training to help educators seamlessly integrate new and existing tools and courses into the curriculum.</li>
        </ul>

        <p><strong>Benefits for Your School:</strong></p>
        <ul>
            <li><strong>Compliance with PM SHRI and NEP Standards:</strong> Ensure your school meets educational reforms and creates a future-ready learning environment.</li>
            <li><strong>Empowered Students:</strong> Prepare students with essential skills in critical thinking, problem-solving, and emerging technologies for future success.</li>
            <li><strong>Advanced Teacher Training:</strong> Enable educators to adopt innovative teaching methods and cutting-edge pedagogy, transforming the classroom experience.</li>
            <li><strong>State-of-the-Art Infrastructure:</strong> Deliver safety, functionality, and aesthetic appeal to enhance the learning environment for students and teachers.</li>
        </ul>

        <p><strong>Why Us?</strong></p>
        <p>We have a proven track record of delivering impactful educational solutions, addressing challenges faced by schools, students, and educators. With personalized support, continuous assistance, and strategic frameworks, we ensure seamless implementation and sustained success.</p>

        <p>I would love to schedule a brief call to discuss how we can transform your school’s educational offerings. Please let me know a convenient time, and I’ll be happy to arrange it. 
        <br>
        <strong>Note:</strong> You can view the brochure with more details through the following link: 
        <a href="{brochure_link}" target="_blank">Brochure Link</a></p>

        <p>Looking forward to your response.</p>

        <p>For further queries or clarifications, please contact:</p>
        <p><a href="https://wa.me/7456840977" target="_blank"><img src="cid:whatsapp_icon" alt="WhatsApp" style="width: 50px; height: 50px;"></a></p>
        <strong>Email:</strong> pmshri@myaimate.com</p>
        <strong>Phone:</strong> +91 7456840977</p>

        <p>Best regards,<br>
        <strong>Team myAImate</strong></p>
        </body>
        </html>
        """

        # Set up the MIME structure
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'html'))

        # Attach WhatsApp icon
        image_path = 'WhatsApp.png'  # Path to your image
        mime_type, encoding = mimetypes.guess_type(image_path)
        if mime_type is None:
            mime_type = 'application/octet-stream'  # Fallback MIME type
        mime_type_main, mime_type_sub = mime_type.split('/')

        # Read the image and attach it
        with open(image_path, 'rb') as img_file:
            img = MIMEImage(img_file.read(), _subtype=mime_type_sub)
            img.add_header('Content-ID', '<whatsapp_icon>')
            msg.attach(img)

        # Connect to SMTP server using TLS
        server = smtplib.SMTP(smtp_server, port)
        server.starttls()  # Ensure TLS is initiated
        server.login(sender_email, password)  # Use your app-specific password
        server.sendmail(sender_email, recipient_email, msg.as_string())
        server.quit()
        print(f"Email sent to {recipient_email}")
    except Exception as e:
        print(f"Error while sending email to {recipient_email}: {e}")

# Read the Excel file
excel_file = 'email_list.xlsx'  # Replace with your file name
brochure_link = 'https://www.myaimate.com/_files/ugd/e9169b_4414cc86d15547cdafc613ba568c6fad.pdf'  # Replace with your actual Google Drive link
data = pd.read_excel(excel_file)

# Iterate through rows and send emails
for index, row in data.iterrows():
    try:
        # Extract and validate data
        recipient_email = row.get('hm_email', "").strip() if pd.notna(row.get('hm_email', "")) else None
        school_name = row.get('school_name', "").strip() if pd.notna(row.get('school_name', "")) else ""
        recipient_district = row.get('district_name', "").strip() if pd.notna(row.get('district_name', "")) else ""
        recipient_state = row.get('state_name', "").strip() if pd.notna(row.get('state_name', "")) else ""

        # Skip if the email is missing
        if not recipient_email:
            print(f"Skipping row {index}: Email is missing")
            continue

        # Send email
        send_email(recipient_email, school_name, recipient_district, recipient_state, brochure_link)
        time.sleep(10)
    except Exception as e:
        print(f"Error processing row {index}: {e}")
