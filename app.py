import gradio as gr
import os
import threading
from PIL import Image
import traceback
import time

# Optional imports. We handle missing dependencies gracefully.
try:
    from stable_diffusion_cpp import StableDiffusion
    SD_AVAILABLE = True
except ImportError:
    SD_AVAILABLE = False


# Paths
MODELS_DIR = "models"
LORAS_DIR = "loras"
OUTPUTS_DIR = "outputs"
os.makedirs(MODELS_DIR, exist_ok=True)
os.makedirs(LORAS_DIR, exist_ok=True)
os.makedirs(OUTPUTS_DIR, exist_ok=True)

DIFFUSION_MODEL_PATH = os.path.join(MODELS_DIR, "zimage", "z_image_turbo_Q6_K.gguf")
LLM_PATH = os.path.join(MODELS_DIR, "llm", "Qwen3-4B-Instruct-2507-Q4_K_M.gguf")
VAE_PATH = os.path.join(MODELS_DIR, "vae", "ae.safetensors")

# Global instances
sd_instance = None
model_lock = threading.Lock()

def get_lora_names():
    if not os.path.exists(LORAS_DIR):
        return []
    return [f.replace(".safetensors", "") for f in os.listdir(LORAS_DIR) if f.endswith(".safetensors")]

def load_sd():
    global sd_instance
    if not SD_AVAILABLE:
        raise RuntimeError("stable-diffusion-cpp-python is not installed.")
    
    if sd_instance is not None:
        return sd_instance

    if not os.path.exists(DIFFUSION_MODEL_PATH):
        raise FileNotFoundError(f"Diffusion model not found at {DIFFUSION_MODEL_PATH}")
    if not os.path.exists(LLM_PATH):
        raise FileNotFoundError(f"LLM text encoder not found at {LLM_PATH}")
    if not os.path.exists(VAE_PATH):
        raise FileNotFoundError(f"VAE not found at {VAE_PATH}")

    print("Loading Stable Diffusion Pipeline (GGUF)...")
    sd_instance = StableDiffusion(
        diffusion_model_path=DIFFUSION_MODEL_PATH,
        llm_path=LLM_PATH,
        vae_path=VAE_PATH,
        lora_model_dir=LORAS_DIR,
        offload_params_to_cpu=False,
        keep_clip_on_cpu=True,
        flash_attn=True,
        diffusion_flash_attn=True,
        enable_mmap=True
    )
    return sd_instance

def generate_text_to_image(prompt, negative_prompt, width, height, steps, cfg, lora_name, lora_weight):
    with model_lock:
        try:
            sd = load_sd()
            # Inject LoRA into prompt if selected
            final_prompt = prompt
            if lora_name and lora_name != "None":
                final_prompt += f" <lora:{lora_name}:{lora_weight}>"
            
            print(f"Generating T2I with prompt: {final_prompt}")
            images = sd.generate_image(
                prompt=final_prompt,
                negative_prompt=negative_prompt,
                width=int(width),
                height=int(height),
                sample_steps=int(steps),
                cfg_scale=float(cfg),
                sample_method='euler',
                vae_tiling=True,
            )
            image_out = images[0] if isinstance(images, list) else images
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            image_out.save(os.path.join(OUTPUTS_DIR, f"t2i_{timestamp}.png"))
            return image_out
        except Exception as e:
            traceback.print_exc()
            raise gr.Error(f"Generation failed: {str(e)}\n\nNote: LoRAs might not work natively with quantized GGUF models in python bindings yet.")



# ------------------- Gradio UI Construction -------------------

theme = gr.themes.Soft(
    primary_hue="indigo",
    secondary_hue="blue",
)

with gr.Blocks(theme=theme, title="Z-Image GGUF Interface") as demo:
    gr.Markdown("# 🚀 Z-Image GGUF Web UI")
    gr.Markdown("A unified interface for Text-to-Image and Image-to-Text using quantized models.")
    
    available_loras = ["None"] + get_lora_names()

    with gr.Tabs():
        # Text to Image Tab
        with gr.Tab("🖼️ Text to Image"):
            with gr.Row():
                with gr.Column(scale=2):
                    t2i_prompt = gr.Textbox(label="Prompt", lines=3, placeholder="A beautiful sunset over cyberpunk city...")
                    t2i_neg_prompt = gr.Textbox(label="Negative Prompt", lines=2, placeholder="ugly, blurry, low quality")
                    
                    with gr.Row():
                        t2i_width = gr.Slider(256, 2048, value=576, step=64, label="Width")
                        t2i_height = gr.Slider(256, 2048, value=576, step=64, label="Height")
                    
                    with gr.Row():
                        t2i_steps = gr.Slider(1, 100, value=8, step=1, label="Sampling Steps")
                        t2i_cfg = gr.Slider(1.0, 20.0, value=2.0, step=0.1, label="CFG Scale")
                        
                    with gr.Row():
                        t2i_lora = gr.Dropdown(choices=available_loras, value="None", label="LoRA")
                        t2i_lora_weight = gr.Slider(0.0, 2.0, value=1.0, step=0.05, label="LoRA Weight")
                        
                    t2i_btn = gr.Button("Generate", variant="primary")
                    
                with gr.Column(scale=3):
                    t2i_output = gr.Image(label="Generated Image", type="pil", interactive=False)
            
            t2i_btn.click(
                fn=generate_text_to_image,
                inputs=[t2i_prompt, t2i_neg_prompt, t2i_width, t2i_height, t2i_steps, t2i_cfg, t2i_lora, t2i_lora_weight],
                outputs=t2i_output
            )




if __name__ == "__main__":
    demo.launch(server_name="127.0.0.1", server_port=7860, inbrowser=True)
