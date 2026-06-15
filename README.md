# 🚀 Z-Image Turbo by Gradio

A lightweight, portable web UI for generating images (Text-to-Image) using quantized GGUF models. It utilizes `stable-diffusion-cpp-python` to run diffusion models efficiently and provides a clean, user-friendly interface powered by Gradio.

## Features
- **Text-to-Image Generation**: Fast image generation with quantized GGUF models.
- **LoRA Support**: Drop your `.safetensors` LoRA files into the `loras/` folder and apply them via the UI.
- **Portable & Automated Setup**: One-click batch script for environment setup.

## 📋 Prerequisites
- **Python 3.10+**: Ensure Python is installed and added to your system PATH.

## 🛠️ Installation & Setup

We have provided a fully automated setup script for Windows. 

1. Clone or download this repository.
2. Double-click **`setup_and_run.bat`**.
3. The script will automatically:
   - Create a Python virtual environment (`venv`).
   - Install all required dependencies from `requirements.txt`.
   - Create the necessary folders for your models.
   - Pause and warn you if you are missing the required models.

## 📥 Required Models (Manual Download)

Because this project uses specific custom quantized models, you need to manually download them and place them in the generated folders. 

Please download the following models and place them in their respective directories:

1. **Z-Image Diffusion Model** (`z_image_turbo_Q6_K.gguf`)
   - Place it at: `models/zimage/z_image_turbo_Q6_K.gguf`
2. **LLM Text Encoder** (`Qwen3-4B-Instruct-2507-Q4_K_M.gguf`)
   - Place it at: `models/llm/Qwen3-4B-Instruct-2507-Q4_K_M.gguf`
3. **VAE Model** (`ae.safetensors`)
   - Place it at: `models/vae/ae.safetensors`

*(Note: If you have your own LoRA models, place the `.safetensors` files inside the `loras/` directory.)*

## 🚀 Running the Application

Once your models are in the correct folders, you can start the application at any time by double-clicking **`setup_and_run.bat`**. 

If your environment is already fully set up and you just want to launch the UI directly without the setup checks, you can use **`run.bat`**.

The web UI will automatically open in your default browser at `http://127.0.0.1:7860`.
