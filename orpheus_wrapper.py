#!/usr/bin/env python3
"""
Wrapper script for Orpheus TTS to enforce vLLM configuration.
"""
import os
import sys
import logging

# Set environment variables to control vLLM
os.environ["VLLM_MAX_MODEL_LEN"] = "10000000"
os.environ["VLLM_GPU_MEMORY_UTILIZATION"] = "0.9"
os.environ["VLLM_DISABLE_LOGGING"] = "1"

try:
    # Import the necessary modules
    from vllm.engine.arg_utils import EngineArgs
    from vllm.engine.async_llm_engine import AsyncLLMEngine
    from orpheus_tts.engine_class import OrpheusModel
    
    # Store the original from_engine_args method
    original_from_engine_args = AsyncLLMEngine.from_engine_args
    
    # Define a patched version that doesn't use disable_log_requests
    def patched_from_engine_args(engine_args, **kwargs):
        # Override the max_model_len in engine_args
        engine_args.max_model_len = 10000000
        engine_args.gpu_memory_utilization = 0.9
        
        print(f"Patched from_engine_args called with max_model_len={engine_args.max_model_len}")
        
        # Call the original without any extra kwargs
        return original_from_engine_args(engine_args)
    
    # Replace the class method
    AsyncLLMEngine.from_engine_args = staticmethod(patched_from_engine_args)
    print("Successfully patched AsyncLLMEngine.from_engine_args")
    
except Exception as e:
    print(f"Warning: Failed to patch AsyncLLMEngine: {e}")

# Now import and run the Orpheus app
print("Starting Orpheus TTS...")

# Import the Gradio app
import orpheus

# Actually run the Gradio app
if __name__ == "__main__":
    orpheus.demo.launch(share=True) 