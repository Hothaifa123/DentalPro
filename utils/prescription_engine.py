from fpdf import FPDF
import os, datetime, base64
from config import get_doctor, ARIAL_FONT_PATH, CLINIC_LOGO_PATH

class A5Prescription(FPDF):
    def __init__(self, doctor=None):
        super().__init__(format='A5')
        self.doctor = doctor or get_doctor()
        if os.path.exists(ARIAL_FONT_PATH):
            self.add_font('Arial', '', ARIAL_FONT_PATH, uni=True)
            self.add_font('Arial', 'B', ARIAL_FONT_PATH, uni=True)
        self.set_auto_page_break(True, 20)

    def header(self):
        if os.path.exists(CLINIC_LOGO_PATH):
            self.image(CLINIC_LOGO_PATH, x=10, y=8, h=16)
        self.set_font('Arial', 'B', 13)
        self.cell(0, 7, self.doctor.get('name',''), ln=True, align='R')
        self.set_font('Arial', '', 9)
        self.cell(0, 5, f"Phone: {self.doctor.get('phone','')}  |  {self.doctor.get('specialty','')}", ln=True, align='R')
        self.ln(4)
        self.line(10, self.get_y(), 138, self.get_y())
        self.ln(4)

    def footer(self):
        self.set_y(-28)
        self.line(10, self.get_y(), 138, self.get_y())
        self.set_font('Arial', 'I', 9)
        self.cell(0, 8, "Doctor's Signature: __________________", ln=True, align='R')
        self.set_font('Arial', '', 7)
        self.cell(0, 5, f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}  |  {self.doctor.get('clinic','')}", ln=True, align='C')

def build_pdf(patient, drugs, diagnosis, notes="", doctor=None):
    pdf = A5Prescription(doctor)
    pdf.add_page()
    pdf.set_font('Arial', 'B', 11)
    pdf.cell(0, 7, "Patient Information", ln=True)
    pdf.set_font('Arial', '', 10)
    pdf.cell(0, 6, f"Name: {patient.get('name','')}    Age: {patient.get('age','')}    Gender: {patient.get('gender','')}", ln=True)
    if diagnosis: pdf.cell(0, 6, f"Diagnosis: {diagnosis}", ln=True)
    pdf.ln(5)
    pdf.set_font('Arial', 'B', 12)
    pdf.set_text_color(180,0,0)
    pdf.cell(0, 7, 'Rx:', ln=True)
    pdf.set_text_color(0,0,0)
    pdf.ln(2)
    pdf.set_font('Arial', '', 10)
    for d in drugs:
        line = f"- {d['drug_name']}  {d['dosage']}  {d['frequency']}"
        if d.get('duration'): line += f"  for {d['duration']}"
        pdf.multi_cell(0, 6, line)
    if notes:
        pdf.ln(4)
        pdf.set_font('Arial', 'I', 9)
        pdf.multi_cell(0, 5, f"Notes: {notes}")
    return pdf.output()
