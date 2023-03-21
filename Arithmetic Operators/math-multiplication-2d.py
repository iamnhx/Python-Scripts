from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
import random

def generate_multiplication_problems(n=600):
    questions = []
    for i in range(n):
        a = random.randint(10, 99)
        b = random.randint(10, 99)
        c = a * b
        question = (f"   {a}   \nx {b}   \n-------\n\n", c)
        questions.append(question)
    return questions

questions_with_answers = generate_multiplication_problems()

# Create PDF document with answers
doc = SimpleDocTemplate("multiplication_worksheet_with_answers.pdf", pagesize=landscape(letter))
data = [[f"{problem}{answer}" for problem, answer in questions_with_answers[i:i+10]] for i in range(0, 600, 10)]
t = Table(data)
t.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,-1), colors.white),
                      ('TEXTCOLOR',(0,0),(-1,-1),colors.black),
                      ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
                      ('FONTSIZE', (0,0), (-1,-1), 16),
                      ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                      ('BOTTOMPADDING', (0,0), (-1,-1), 12),
                      ('BACKGROUND', (0,0), (-1,-1), colors.white),
                      ('GRID',(0,0),(-1,-1),1,colors.black),
                      ]))
doc.build([t])

# Create PDF document without answers
doc = SimpleDocTemplate("multiplication_worksheet_without_answers.pdf", pagesize=landscape(letter))
data = [[problem for problem, answer in questions_with_answers[i:i+10]] for i in range(0, 600, 10)]
t = Table(data)
t.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,-1), colors.white),
                      ('TEXTCOLOR',(0,0),(-1,-1),colors.black),
                      ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
                      ('FONTSIZE', (0,0), (-1,-1), 16),
                      ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                      ('BOTTOMPADDING', (0,0), (-1,-1), 12),
                      ('BACKGROUND', (0,-1), (-1,-1), colors.white),
                      ('GRID',(0,0),(-1,-1),1,colors.black),
                      ]))
doc.build([t])