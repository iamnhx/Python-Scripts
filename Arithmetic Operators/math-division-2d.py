from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
import random

def generate_division_problems(n=600):
    questions = []
    for i in range(n):
        a = random.randint(10, 99)
        b = random.randint(2, 9)  # Change range of b
        c = a / b
        while c % 1 != 0:  # check if c has a remainder
            a = random.randint(10, 99)
            b = random.randint(2, 9)
            c = a / b
        question = (f"   {a}   \n÷   {b}   \n-------\n\n", int(c))
        questions.append(question)
    return questions

questions_with_answers = generate_division_problems()

# Create PDF document with answers
doc = SimpleDocTemplate("division_worksheet_with_answers.pdf", pagesize=landscape(letter))
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
doc = SimpleDocTemplate("division_worksheet_without_answers.pdf", pagesize=landscape(letter))
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
