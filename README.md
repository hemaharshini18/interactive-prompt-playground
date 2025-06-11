# 🧠 Interactive Prompt Playground

A sophisticated web application for experimenting with OpenAI models and fine-tuning parameters to create the perfect AI responses.

![Interactive Prompt Playground](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

## 📋 Overview

Interactive Prompt Playground provides a user-friendly interface to experiment with different OpenAI API parameters and see how they affect the output. Perfect for content creators, developers, and AI enthusiasts who want to fine-tune their prompts and understand parameter impacts.

## ✨ Features

- **Multiple Model Support**: Test across GPT-4, GPT-3.5-Turbo, and more
- **Pre-defined Assistant Roles**: Choose from Product Description Writer, Customer Support Agent, Technical Expert, and Creative Writer
- **Parameter Tuning**: Adjust temperature, max tokens, presence penalty, and frequency penalty
- **Batch Testing**: Compare multiple parameter combinations simultaneously
- **Beautiful UI**: Modern, responsive interface with professional design
- **Result Comparison**: Easily compare outputs from different parameter settings

## 🚀 Getting Started

### Prerequisites

- Python 3.7+
- OpenAI API key

### Installation

1. Clone this repository:
```bash
git clone https://github.com/hemaharshini18/interactive-prompt-playground.git
cd interactive-prompt-playground
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root and add your OpenAI API key:
```
OPENAI_API_KEY=your_openai_api_key_here
```

### Running the Application

Launch the application with:
```bash
streamlit run app.py
```

The application will be available at http://localhost:8501 in your web browser.

## 🔧 Usage

1. **Select a Model**: Choose the OpenAI model you want to use from the sidebar
2. **Choose an Assistant Role**: Select a predefined role or create a custom system prompt
3. **Enter Your Prompt**: Type your prompt in the input area or use a template
4. **Adjust Parameters**: Fine-tune temperature, max tokens, and other parameters
5. **Generate Response**: Click the "Generate Response" button to see the results
6. **Batch Testing**: Enable batch testing to compare multiple parameter combinations

## 📊 Parameter Guide

- **Temperature**: Controls randomness (0.0 = deterministic, 2.0 = very random)
- **Max Tokens**: Maximum length of the generated response
- **Presence Penalty**: Penalizes new tokens based on whether they appear in the text so far
- **Frequency Penalty**: Penalizes new tokens based on their frequency in the text so far
- **Stop Sequence**: The API will stop generating further tokens when this sequence is generated

Typography uses a combination of Inter (headings) and Source Serif Pro (body text) for a formal, professional appearance.

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgements

- [OpenAI](https://openai.com/) for providing the API
- [Streamlit](https://streamlit.io/) for the web framework

---

Made with ❤️ by AI Enthusiasts
