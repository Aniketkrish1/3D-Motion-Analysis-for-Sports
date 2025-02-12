from fpdf import FPDF

def generate_report(sport, landmarks_path, stats, recommendations, normal_animation_path, skeleton_animation_path, output_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Title
    pdf.cell(200, 10, f"##Analysis Report for {sport}", ln=True, align="C")
    pdf.ln(10)

    # Landmarks path
    pdf.cell(200, 10, f"Landmarks Data: {landmarks_path}", ln=True)
    pdf.ln(10)

    # Statistics
    pdf.multi_cell(0, 10, f"Statistics:\nKnee angle:{stats[0]}\nTorso angle:{stats[1]}\nAverage Speed:{stats[2]}")
    pdf.ln(10)

    # Recommendations
    pdf.cell(200, 10, "Recommendations:", ln=True)
    for rec in recommendations:
        pdf.multi_cell(0, 10, f"Frames {rec['frame_range']}: {rec['action']}")
    pdf.ln(10)

    # Animations
    pdf.cell(200, 10, "Normal Animation:", ln=True)
    pdf.cell(200, 10, f"File Path: {normal_animation_path}", ln=True)
    pdf.ln(10)

    pdf.cell(200, 10, "Skeleton Animation:", ln=True)
    pdf.cell(200, 10, f"File Path: {skeleton_animation_path}", ln=True)
    pdf.ln(10)

    pdf.output(output_path)
    print(f"Report generated and saved at: {output_path}")

