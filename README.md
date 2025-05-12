# Healthcare Assistant

## Overview
This project is a virtual assistant for the healthcare sector. It is designed to:

- Respond to complex patient questions
- Provide basic medical advice
- Manage appointments
- Understand and generate contextual responses accurately and naturally

## Features

### High Priority
- Chat management with RAG (Retrieval-Augmented Generation) for contextual responses using MedQuAD and MIMIC-III datasets
- Accurate responses using RAG system
- Doctor recommendation based on patient needs
- Display available slots and book appointments

### Medium Priority
- Upload diagnostic/analysis images
- View appointment list
- Access chat history

### Low Priority (Optional)
- User login/registration
- Modify/cancel appointments
- Doctor interface for viewing patients/appointments
- Doctor preview page with patient problem details and chat history

### Additional AI Feature
- Medical image analysis using pre-trained models

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd healthcare_assistant
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate # Linux/macOS
   venv\Scripts\activate # Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Start backend:
   ```bash
   python api/app.py
   ```
   OR run a demo:
   ```bash
   python examples/run_demo.py
   ```

5. Start frontend:
   ```bash
   streamlit run frontend/app.py
   ```